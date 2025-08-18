from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from pathlib import Path
from typing import Optional
import os

from app.deps import get_templates, get_config, require_auth, get_csrf_token, verify_csrf_token
from app.services.content_loader import ContentLoader
from app.services.git_repo import GitRepo
from app.services.search import SimpleSearch
from app.services.markdown import render_markdown
from app.security import validate_file_path, is_safe_filename, validate_content_size

router = APIRouter(prefix="/cms", tags=["cms"])

# Initialize services
content_loader = ContentLoader()
git_repo = GitRepo()
search = SimpleSearch()

@router.get("", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse)
async def cms_dashboard(request: Request, user = Depends(require_auth)):
    templates = get_templates()
    config = get_config()
    
    # Get recent pages
    pages = content_loader.list_pages()[:10]
    
    # Get git status
    git_status = git_repo.get_status()
    
    # Get recent commits
    recent_commits = git_repo.get_commit_history(limit=5)
    
    tmpl = templates.get_template("cms/index.html")
    return tmpl.render(
        request=request,
        user=user,
        pages=pages,
        git_status=git_status,
        recent_commits=recent_commits,
        site=config.get('site', {}),
        csrf_token=get_csrf_token(request)
    )

@router.get("/files", response_class=JSONResponse)
async def list_files(request: Request, root: str = "content", user = Depends(require_auth)):
    """List files in content or templates directory"""
    allowed_roots = ["content", "templates"]
    if root not in allowed_roots:
        raise HTTPException(status_code=400, detail="Invalid root directory")
    
    try:
        root_path = Path(root)
        files = []
        
        if root_path.exists():
            for file_path in root_path.rglob("*"):
                if file_path.is_file():
                    stat = file_path.stat()
                    files.append({
                        "path": str(file_path),
                        "name": file_path.name,
                        "size": stat.st_size,
                        "modified": stat.st_mtime,
                        "type": file_path.suffix
                    })
        
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/file", response_class=HTMLResponse)
async def edit_file(request: Request, path: str, user = Depends(require_auth)):
    """Edit file form"""
    templates = get_templates()
    config = get_config()
    
    # Validate file path
    if not validate_file_path(path, ["content", "templates"]):
        raise HTTPException(status_code=400, detail="Invalid file path")
    
    file_path = Path(path)
    content = ""
    metadata = {}
    
    if file_path.exists():
        if file_path.suffix == '.md':
            try:
                metadata, content = content_loader.load_page_by_path(path)
            except Exception as e:
                content = file_path.read_text(encoding='utf-8')
        else:
            content = file_path.read_text(encoding='utf-8')
    
    tmpl = templates.get_template("cms/editor.html")
    return tmpl.render(
        request=request,
        user=user,
        file_path=path,
        content=content,
        metadata=metadata,
        site=config.get('site', {}),
        csrf_token=get_csrf_token(request)
    )

@router.post("/file")
async def save_file(
    request: Request,
    path: str = Form(...),
    content: str = Form(...),
    message: str = Form("Edit via CMS"),
    csrf_token: str = Form(...),
    user = Depends(require_auth)
):
    """Save file content"""
    verify_csrf_token(request, csrf_token)
    
    # Validate inputs
    if not validate_file_path(path, ["content", "templates"]):
        raise HTTPException(status_code=400, detail="Invalid file path")
    
    if not validate_content_size(content):
        raise HTTPException(status_code=400, detail="Content too large")
    
    try:
        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save the file
        file_path.write_text(content, encoding='utf-8')
        
        # Git operations
        git_repo.add_file(path)
        
        # Format commit message
        commit_msg = f"{message} ({path}) by {user['username']}"
        git_repo.commit(commit_msg, user.get('username'), user.get('email'))
        
        return RedirectResponse(url=f"/cms/file?path={path}", status_code=302)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {e}")

@router.post("/preview")
async def preview_content(
    request: Request,
    content: str = Form(...),
    layout: str = Form("docs.html"),
    csrf_token: str = Form(...),
    user = Depends(require_auth)
):
    """Preview markdown content"""
    verify_csrf_token(request, csrf_token)
    templates = get_templates()
    config = get_config()
    
    # Render markdown
    html_content = render_markdown(content)
    
    # Create preview context
    preview_context = {
        'request': request,
        'content': html_content,
        'page': {'title': 'Preview'},
        'site': config.get('site', {}),
        'is_preview': True
    }
    
    # Render with specified layout
    try:
        tmpl = templates.get_template(f"layouts/{layout}")
        preview_html = tmpl.render(**preview_context)
        
        tmpl = templates.get_template("cms/preview.html")
        return tmpl.render(
            request=request,
            preview_html=preview_html,
            user=user,
            site=config.get('site', {}),
            csrf_token=get_csrf_token(request)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Preview error: {e}")

@router.get("/diff")
async def view_diff(
    request: Request,
    path: str,
    rev: str = "HEAD~1",
    user = Depends(require_auth)
):
    """View file diff"""
    templates = get_templates()
    config = get_config()
    
    if not validate_file_path(path, ["content", "templates"]):
        raise HTTPException(status_code=400, detail="Invalid file path")
    
    diff_content = git_repo.get_file_diff(path, rev)
    
    tmpl = templates.get_template("cms/diff.html")
    return tmpl.render(
        request=request,
        user=user,
        file_path=path,
        diff_content=diff_content,
        revision=rev,
        site=config.get('site', {})
    )

@router.post("/delete")
async def delete_file(
    request: Request,
    path: str = Form(...),
    message: str = Form("Delete file via CMS"),
    csrf_token: str = Form(...),
    user = Depends(require_auth)
):
    """Delete a file"""
    verify_csrf_token(request, csrf_token)
    
    if not validate_file_path(path, ["content", "templates"]):
        raise HTTPException(status_code=400, detail="Invalid file path")
    
    try:
        file_path = Path(path)
        if file_path.exists():
            git_repo.remove_file(path)
            commit_msg = f"{message} ({path}) by {user['username']}"
            git_repo.commit(commit_msg, user.get('username'), user.get('email'))
        
        return RedirectResponse(url="/cms", status_code=302)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {e}")

@router.get("/logs")
async def view_logs(request: Request, user = Depends(require_auth)):
    """View commit logs"""
    templates = get_templates()
    config = get_config()
    
    commits = git_repo.get_commit_history(limit=20)
    
    tmpl = templates.get_template("cms/index.html")  # Reuse dashboard template
    return tmpl.render(
        request=request,
        user=user,
        commits=commits,
        site=config.get('site', {}),
        show_logs=True
    )

@router.post("/search")
async def cms_search(
    request: Request,
    query: str = Form(...),
    csrf_token: str = Form(...),
    user = Depends(require_auth)
):
    """Search content from CMS"""
    verify_csrf_token(request, csrf_token)
    
    results = search.search(query, limit=20)
    return JSONResponse({"results": results})
