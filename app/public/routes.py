from fastapi import APIRouter, Request, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse
from typing import Optional

from app.deps import get_templates, get_config
from app.services.content_loader import ContentLoader
from app.services.nav import NavigationBuilder
from app.services.search import SimpleSearch
from app.services.markdown import render_markdown

router = APIRouter()

# Initialize services
content_loader = ContentLoader()
nav_builder = NavigationBuilder()
search = SimpleSearch()

@router.get("/", response_class=HTMLResponse)
@router.get("/{slug:path}", response_class=HTMLResponse)
async def render_page(request: Request, slug: str = ""):
    templates = get_templates()
    config = get_config()
    
    try:
        metadata, content = content_loader.load_page(slug)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Page not found")
    
    # Skip draft pages in production
    if metadata.get('draft', False) and not request.url.hostname in ['localhost', '127.0.0.1']:
        raise HTTPException(status_code=404, detail="Page not found")
    
    # Render markdown content
    content_html = render_markdown(content)
    
    # Get layout template
    layout = metadata.get('layout', 'docs.html')
    try:
        tmpl = templates.get_template(f"layouts/{layout}")
    except:
        # Fallback to docs layout
        tmpl = templates.get_template("layouts/docs.html")
    
    # Build navigation
    navigation = nav_builder.build_navigation()
    breadcrumbs = nav_builder.get_breadcrumbs(slug)
    
    return tmpl.render(
        request=request,
        content=content_html,
        page=metadata,
        site=config.get('site', {}),
        navigation=navigation,
        breadcrumbs=breadcrumbs
    )

@router.get("/api/search", response_class=JSONResponse)
async def search_content(query: str = Query(..., min_length=2), limit: int = Query(10, ge=1, le=50)):
    """Public search API endpoint"""
    try:
        results = search.search(query, limit)
        return {"results": results, "query": query, "total": len(results)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {e}")

@router.get("/api/suggestions", response_class=JSONResponse)
async def search_suggestions(query: str = Query(..., min_length=1), limit: int = Query(5, ge=1, le=10)):
    """Get search suggestions"""
    try:
        suggestions = search.get_search_suggestions(query, limit)
        return {"suggestions": suggestions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Suggestions error: {e}")

@router.get("/sitemap.xml", response_class=HTMLResponse)
async def sitemap():
    """Generate XML sitemap"""
    config = get_config()
    base_url = config.get('site', {}).get('base_url', 'http://localhost:5000')
    
    pages = content_loader.list_pages()
    
    sitemap_xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    sitemap_xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    for page in pages:
        # Skip draft pages
        try:
            metadata, _ = content_loader.load_page_by_path(page['file_path'])
            if metadata.get('draft', False):
                continue
            
            slug = metadata.get('slug', page.get('slug', ''))
            if slug:
                url = f"{base_url.rstrip('/')}{slug if slug.startswith('/') else '/' + slug}"
                sitemap_xml.append(f'  <url><loc>{url}</loc></url>')
        except:
            continue
    
    sitemap_xml.append('</urlset>')
    
    return HTMLResponse('\n'.join(sitemap_xml), media_type="application/xml")

@router.get("/robots.txt", response_class=HTMLResponse)
async def robots():
    """Generate robots.txt"""
    config = get_config()
    base_url = config.get('site', {}).get('base_url', 'http://localhost:5000')
    
    robots_txt = [
        "User-agent: *",
        "Allow: /",
        f"Sitemap: {base_url.rstrip('/')}/sitemap.xml"
    ]
    
    return HTMLResponse('\n'.join(robots_txt), media_type="text/plain")
