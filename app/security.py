from bleach.sanitizer import Cleaner
from pathlib import Path
import re

# HTML sanitizer configuration
cleaner = Cleaner(
    tags=[
        "a", "p", "ul", "ol", "li", "h1", "h2", "h3", "h4", "h5", "h6",
        "pre", "code", "blockquote", "em", "strong", "table", "thead",
        "tbody", "tr", "th", "td", "img", "hr", "br", "div", "span"
    ],
    attributes={
        "*": ["class", "id"],
        "a": ["href", "title", "target", "rel"],
        "img": ["src", "alt", "title"],
        "div": ["class", "id"],
        "span": ["class", "id"]
    },
    protocols=["http", "https", "mailto", "data"]
)

def sanitize_html(html_content: str) -> str:
    """Sanitize HTML content to prevent XSS"""
    return cleaner.clean(html_content)

def validate_file_path(file_path: str, allowed_roots: list) -> bool:
    """Validate file path to prevent directory traversal"""
    try:
        path = Path(file_path).resolve()
        for root in allowed_roots:
            root_path = Path(root).resolve()
            if str(path).startswith(str(root_path)):
                return True
        return False
    except Exception:
        return False

def is_safe_filename(filename: str) -> bool:
    """Check if filename is safe"""
    # Allow alphanumeric, dots, hyphens, underscores
    return bool(re.match(r'^[a-zA-Z0-9._-]+$', filename))

def validate_content_size(content: str, max_size_mb: int = 5) -> bool:
    """Validate content size"""
    content_size = len(content.encode('utf-8'))
    max_size_bytes = max_size_mb * 1024 * 1024
    return content_size <= max_size_bytes
