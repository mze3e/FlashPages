import markdown
from markdown.extensions import codehilite, fenced_code, tables, toc, attr_list
from app.security import sanitize_html

# Configure markdown processor
md = markdown.Markdown(extensions=[
    'fenced_code',
    'tables', 
    'toc',
    'attr_list',
    'codehilite'
], extension_configs={
    'codehilite': {
        'css_class': 'highlight',
        'use_pygments': True
    },
    'toc': {
        'permalink': True,
        'permalink_class': 'headerlink',
        'permalink_title': 'Permanent link'
    }
})

def render_markdown(text: str) -> str:
    """Render markdown text to HTML with sanitization"""
    if not text:
        return ""
    
    # Convert markdown to HTML
    html = md.convert(text)
    
    # Sanitize the HTML
    safe_html = sanitize_html(html)
    
    # Reset the markdown processor for next use
    md.reset()
    
    return safe_html

def extract_toc(text: str) -> str:
    """Extract table of contents from markdown"""
    if not text:
        return ""
    
    # Convert markdown to get TOC
    md.convert(text)
    toc = getattr(md, 'toc', '')
    
    # Reset for next use
    md.reset()
    
    return toc
