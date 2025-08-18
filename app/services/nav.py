from typing import List, Dict, Any, Optional
from app.services.content_loader import ContentLoader

class NavigationBuilder:
    def __init__(self, content_dir: str = "content/pages"):
        self.content_loader = ContentLoader(content_dir)
    
    def build_navigation(self) -> List[Dict[str, Any]]:
        """Build navigation structure from page metadata"""
        pages = self.content_loader.list_pages()
        nav_items = []
        
        for page_info in pages:
            try:
                metadata, _ = self.content_loader.load_page_by_path(page_info['file_path'])
                
                # Skip draft pages and pages without nav_order
                if metadata.get('draft', False):
                    continue
                
                nav_order = metadata.get('nav_order')
                if nav_order is None:
                    continue
                
                nav_items.append({
                    'title': metadata.get('title', page_info.get('slug', 'Untitled')),
                    'slug': metadata.get('slug', page_info.get('slug', '/')),
                    'nav_order': nav_order,
                    'parent': metadata.get('parent'),
                    'section': metadata.get('section'),
                    'description': metadata.get('description', '')
                })
            except Exception as e:
                print(f"Error processing navigation for {page_info['file_path']}: {e}")
                continue
        
        # Sort by nav_order
        nav_items.sort(key=lambda x: x['nav_order'])
        
        # Build hierarchical structure
        return self._build_hierarchy(nav_items)
    
    def _build_hierarchy(self, nav_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Build hierarchical navigation structure"""
        # Group by section first
        sections = {}
        root_items = []
        
        for item in nav_items:
            section = item.get('section')
            if section:
                if section not in sections:
                    sections[section] = []
                sections[section].append(item)
            else:
                root_items.append(item)
        
        # Build final structure
        navigation = []
        
        # Add root items first
        for item in root_items:
            navigation.append({
                'title': item['title'],
                'slug': item['slug'],
                'description': item.get('description', ''),
                'children': []
            })
        
        # Add sections
        for section_name, section_items in sections.items():
            section_nav = {
                'title': section_name,
                'slug': None,  # Sections don't have direct URLs
                'description': '',
                'children': []
            }
            
            for item in section_items:
                section_nav['children'].append({
                    'title': item['title'],
                    'slug': item['slug'],
                    'description': item.get('description', ''),
                    'children': []
                })
            
            navigation.append(section_nav)
        
        return navigation
    
    def get_breadcrumbs(self, current_slug: str) -> List[Dict[str, str]]:
        """Get breadcrumb navigation for current page"""
        breadcrumbs = [{'title': 'Home', 'slug': '/'}]
        
        try:
            # Load current page metadata
            content_loader = ContentLoader()
            metadata, _ = content_loader.load_page(current_slug)
            
            # Add parent pages if specified
            parent = metadata.get('parent')
            if parent:
                breadcrumbs.append({'title': parent, 'slug': f'/{parent.lower().replace(" ", "-")}'})
            
            # Add current page
            if current_slug not in ('', '/'):
                breadcrumbs.append({
                    'title': metadata.get('title', current_slug),
                    'slug': current_slug
                })
        except Exception:
            # Fallback breadcrumb
            if current_slug not in ('', '/'):
                breadcrumbs.append({'title': current_slug.replace('-', ' ').title(), 'slug': current_slug})
        
        return breadcrumbs
