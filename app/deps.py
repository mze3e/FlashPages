from fastapi import Request, HTTPException, Depends
from jinja2 import Environment, FileSystemLoader, select_autoescape
import yaml
from pathlib import Path
import os

def get_config():
    """Load application configuration"""
    config_path = Path("config.yaml")
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    return {}

def get_templates():
    """Get Jinja2 templates environment"""
    templates = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=select_autoescape(["html", "xml"])
    )
    
    # Add custom filters
    def markdown_filter(text):
        from app.services.markdown import render_markdown
        return render_markdown(text)

    def datefmt_filter(date, format='%Y-%m-%d'):
        return date.strftime(format) if date else ''

    def strftime_filter(date_str, format='%Y-%m-%d'):
        from datetime import datetime
        if date_str == "now":
            return datetime.now().strftime(format)
        return date_str

    def slugify_filter(text):
        import re
        return re.sub(r'[^\w\s-]', '', text).strip().lower().replace(' ', '-')

    templates.filters['md'] = markdown_filter
    templates.filters['datefmt'] = datefmt_filter
    templates.filters['strftime'] = strftime_filter
    templates.filters['slugify'] = slugify_filter
    
    return templates

def get_current_user(request: Request):
    """Get current authenticated user from session"""
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user

def require_auth(request: Request):
    """Require authentication for protected routes"""
    return get_current_user(request)

def get_csrf_token(request: Request):
    """Generate or get CSRF token"""
    if "csrf_token" not in request.session:
        import secrets
        request.session["csrf_token"] = secrets.token_urlsafe(32)
    return request.session["csrf_token"]

def verify_csrf_token(request: Request, token: str):
    """Verify CSRF token"""
    session_token = request.session.get("csrf_token")
    if not session_token or session_token != token:
        raise HTTPException(status_code=403, detail="Invalid CSRF token")
    return True
