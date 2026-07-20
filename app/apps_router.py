from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
import importlib.util
from pathlib import Path

router = APIRouter()
APPS_DIR = Path("apps")

def load_app_module(app_name: str):
    file_path = APPS_DIR / f"{app_name}.py"
    if not file_path.exists() or app_name.startswith("_"):
        return None
        
    spec = importlib.util.spec_from_file_location(app_name, file_path)
    if not spec or not spec.loader:
        return None
        
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        import traceback
        print(f"Error loading {app_name}: {e}")
        traceback.print_exc()
        return None

@router.get("/apps", response_class=HTMLResponse)
@router.get("/apps/", response_class=HTMLResponse)
async def list_apps(request: Request):
    if not APPS_DIR.exists():
        return HTMLResponse(content="<h1>No apps directory found</h1>")
        
    apps = []
    for file_path in APPS_DIR.glob("*.py"):
        if not file_path.name.startswith("_"):
            app_name = file_path.stem
            apps.append(app_name)
            
    if not apps:
        return HTMLResponse(content="<h1>No apps found</h1>")
        
    html = "<h1>Available Apps</h1><ul>"
    for app_name in sorted(apps):
        html += f'<li><a href="/apps/{app_name}">{app_name}</a></li>'
    html += "</ul>"
    
    from app.deps import get_config, get_templates
    config = get_config()
    templates = get_templates()
    tmpl = templates.get_template("apps/app_layout.html")
    return tmpl.render(
        request=request,
        site=config.get('site', {}),
        page={"title": "Discovered Apps"},
        body_content=html
    )

@router.get("/apps/{app_name}", response_class=HTMLResponse)
async def render_app(request: Request, app_name: str):
    module = load_app_module(app_name)
    if not module:
        raise HTTPException(status_code=404, detail="App not found")
        
    if not hasattr(module, "build"):
        raise HTTPException(status_code=500, detail="App missing build() function")
        
    try:
        html_content = module.build(request)
        return HTMLResponse(content=html_content)
    except Exception as e:
        import traceback
        error_html = f"<h1>Error executing build()</h1><pre>{traceback.format_exc()}</pre>"
        return HTMLResponse(content=error_html, status_code=500)

@router.get("/api/apps/{app_name}/{query_name}")
async def handle_api(request: Request, app_name: str, query_name: str):
    module = load_app_module(app_name)
    if not module:
        raise HTTPException(status_code=404, detail="App not found")
        
    if not hasattr(module, "handle_api"):
        raise HTTPException(status_code=404, detail="App has no handle_api function")
        
    try:
        params = dict(request.query_params)
        result = module.handle_api(query_name, params)
        return JSONResponse(content=result)
    except Exception as e:
        import traceback
        print(f"Error in API: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
