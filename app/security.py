from bleach.sanitizer import Cleaner
from pathlib import Path
import re

# HTML sanitizer configuration - Allow Bootstrap components
cleaner = Cleaner(
    tags=[
        "a", "p", "ul", "ol", "li", "h1", "h2", "h3", "h4", "h5", "h6",
        "pre", "code", "blockquote", "em", "strong", "table", "thead",
        "tbody", "tr", "th", "td", "img", "hr", "br", "div", "span", 
        "section", "header", "footer", "nav", "article", "aside", "main",
        "button", "form", "input", "textarea", "label", "select", "option",
        "small", "mark", "del", "ins", "sub", "sup", "i", "b", "u",
        "figure", "figcaption", "time", "address", "cite", "q", "abbr",
        "dfn", "kbd", "samp", "var", "s", "wbr"
    ],
    attributes={
        "*": ["class", "id", "style", "title", "role", "aria-*", "data-*"],
        "a": ["href", "title", "target", "rel", "data-bs-toggle", "data-bs-target", "data-bs-dismiss"],
        "img": ["src", "alt", "title", "width", "height", "loading"],
        "div": ["class", "id", "style", "role", "aria-*", "data-*"],
        "span": ["class", "id", "style", "role", "aria-*", "data-*"],
        "button": ["type", "class", "id", "data-bs-toggle", "data-bs-target", "data-bs-dismiss", "aria-*"],
        "form": ["method", "action", "class", "id", "role"],
        "input": ["type", "name", "value", "placeholder", "required", "class", "id", "aria-*"],
        "textarea": ["name", "placeholder", "required", "class", "id", "rows", "cols"],
        "label": ["for", "class", "id"],
        "select": ["name", "class", "id", "required"],
        "option": ["value", "selected"],
        "i": ["class", "aria-hidden"],
        "section": ["class", "id", "style"],
        "header": ["class", "id"],
        "footer": ["class", "id"],
        "nav": ["class", "id", "role", "aria-*"],
        "table": ["class", "id", "role"],
        "th": ["scope", "class", "id"],
        "td": ["class", "id", "colspan", "rowspan"],
        "figure": ["class", "id"],
        "time": ["datetime", "class", "id"]
    },
    protocols=["http", "https", "mailto", "data", "tel"]
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
