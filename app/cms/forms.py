from pydantic import BaseModel, validator
from typing import Optional
import re

class FileEditForm(BaseModel):
    path: str
    content: str
    message: str = "Edit via CMS"
    
    @validator('path')
    def validate_path(cls, v):
        # Basic path validation
        if '..' in v or v.startswith('/'):
            raise ValueError('Invalid path')
        return v
    
    @validator('content')
    def validate_content(cls, v):
        # Content size validation (5MB limit)
        if len(v.encode('utf-8')) > 5 * 1024 * 1024:
            raise ValueError('Content too large')
        return v

class SearchForm(BaseModel):
    query: str
    limit: Optional[int] = 10
    
    @validator('query')
    def validate_query(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('Query too short')
        return v.strip()
    
    @validator('limit')
    def validate_limit(cls, v):
        if v is not None and (v < 1 or v > 50):
            raise ValueError('Limit must be between 1 and 50')
        return v

class PreviewForm(BaseModel):
    content: str
    layout: str = "docs.html"
    
    @validator('layout')
    def validate_layout(cls, v):
        # Only allow certain layouts
        allowed_layouts = ['base.html', 'docs.html', 'landing.html']
        if v not in allowed_layouts:
            raise ValueError('Invalid layout')
        return v

class CommitForm(BaseModel):
    message: str
    files: list = []
    
    @validator('message')
    def validate_message(cls, v):
        if len(v.strip()) < 5:
            raise ValueError('Commit message too short')
        return v.strip()
