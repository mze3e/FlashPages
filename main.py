from fastapi import FastAPI, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
import os
import yaml
import secrets

from app.deps import get_templates, get_config, get_current_user
from app.public.routes import router as public_router
from app.cms.routes import router as cms_router

# Load configuration
config_path = Path("config.yaml")
if config_path.exists():
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
else:
    # Default configuration
    config = {
        'site': {
            'name': 'Content CMS',
            'base_url': 'http://localhost:5000',
            'theme': 'flatly'
        },
        'content': {
            'dir': 'content/pages',
            'data_dir': 'content/data',
            'static_dir': 'static'
        },
        'git': {
            'repo_path': '.',
            'default_branch': 'main',
            'author_from_user': True
        },
        'auth': {
            'mode': 'basic',
            'admins': ['admin@example.com']
        },
        'security': {
            'csp': "default-src 'self'; img-src 'self' data:; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net"
        }
    }

app = FastAPI(title=config['site']['name'])

# Add session middleware
secret_key = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
app.add_middleware(SessionMiddleware, secret_key=secret_key)

# Mount static files
static_dir = Path(config['content']['static_dir'])
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Initialize Jinja2 templates with filters
from app.deps import get_templates
templates = get_templates()

# Include routers
app.include_router(public_router)
app.include_router(cms_router)

# Health check endpoints
@app.get("/healthz")
async def health_check():
    return {"status": "healthy"}

@app.get("/readyz")
async def readiness_check():
    return {"status": "ready"}

# Basic auth login/logout
@app.get("/auth/login", response_class=HTMLResponse)
async def login_form(request: Request):
    tmpl = templates.get_template("cms/login.html")
    return tmpl.render(request=request, site=config['site'])

@app.post("/auth/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    # Simple authentication - in production, use proper password hashing
    if username == "admin" and password == "admin":
        request.session["user"] = {"username": username, "email": "admin@example.com"}
        return RedirectResponse(url="/cms", status_code=302)
    else:
        tmpl = templates.get_template("cms/login.html")
        return tmpl.render(request=request, site=config['site'], error="Invalid credentials")

@app.post("/auth/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=302)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
