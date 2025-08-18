from pathlib import Path
import yaml
import os
from typing import Dict, Any, Tuple, Optional
from datetime import datetime

class ContentLoader:
    def __init__(self, content_dir: str = "content/pages"):
        self.content_dir = Path(content_dir)
        self.content_dir.mkdir(parents=True, exist_ok=True)
    
    def load_page(self, slug: str) -> Tuple[Dict[str, Any], str]:
        """Load a page by slug, returning metadata and content"""
        # Handle root/index page
        if slug in ("", "/"):
            slug = "index"
        
        # Convert slug to file path
        safe_slug = slug.strip('/').replace('/', '_')
        file_path = self.content_dir / f"{safe_slug}.md"
        
        if not file_path.exists():
            raise FileNotFoundError(f"Page not found: {slug}")
        
        return self._parse_markdown_file(file_path)
    
    def load_page_by_path(self, file_path: str) -> Tuple[Dict[str, Any], str]:
        """Load a page by file path"""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        return self._parse_markdown_file(path)
    
    def _parse_markdown_file(self, file_path: Path) -> Tuple[Dict[str, Any], str]:
        """Parse a markdown file with YAML front-matter"""
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            raise Exception(f"Error reading file {file_path}: {e}")
        
        # Split front-matter and content
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                front_matter = parts[1].strip()
                body = parts[2].strip()
                
                try:
                    metadata = yaml.safe_load(front_matter) or {}
                except yaml.YAMLError as e:
                    metadata = {}
                    print(f"YAML parsing error in {file_path}: {e}")
            else:
                metadata = {}
                body = content
        else:
            metadata = {}
            body = content
        
        # Add file metadata
        stat = file_path.stat()
        metadata.update({
            'file_path': str(file_path),
            'modified_time': datetime.fromtimestamp(stat.st_mtime),
            'file_size': stat.st_size
        })
        
        return metadata, body
    
    def save_page(self, file_path: str, content: str, metadata: Dict[str, Any] = None):
        """Save a page with optional metadata"""
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Combine metadata and content
        if metadata:
            # Remove file-specific metadata before saving
            clean_metadata = {k: v for k, v in metadata.items() 
                            if k not in ['file_path', 'modified_time', 'file_size']}
            
            front_matter = yaml.dump(clean_metadata, default_flow_style=False)
            full_content = f"---\n{front_matter}---\n{content}"
        else:
            full_content = content
        
        path.write_text(full_content, encoding='utf-8')
    
    def list_pages(self) -> list:
        """List all pages in the content directory"""
        pages = []
        for file_path in self.content_dir.glob("*.md"):
            try:
                metadata, _ = self._parse_markdown_file(file_path)
                slug = metadata.get('slug', file_path.stem)
                pages.append({
                    'file_path': str(file_path),
                    'slug': slug,
                    'title': metadata.get('title', file_path.stem),
                    'modified_time': metadata.get('modified_time'),
                    'draft': metadata.get('draft', False)
                })
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
        
        return sorted(pages, key=lambda x: x.get('modified_time', datetime.min), reverse=True)
    
    def delete_page(self, file_path: str):
        """Delete a page file"""
        path = Path(file_path)
        if path.exists():
            path.unlink()
