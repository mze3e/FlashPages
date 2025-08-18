import os
import re
from pathlib import Path
from typing import List, Dict, Any
from app.services.content_loader import ContentLoader

class SimpleSearch:
    def __init__(self, content_dir: str = "content/pages"):
        self.content_loader = ContentLoader(content_dir)
    
    def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Simple text search across all pages"""
        if not query or len(query.strip()) < 2:
            return []
        
        query = query.lower().strip()
        results = []
        
        # Get all pages
        pages = self.content_loader.list_pages()
        
        for page_info in pages:
            try:
                metadata, content = self.content_loader.load_page_by_path(page_info['file_path'])
                
                # Skip draft pages
                if metadata.get('draft', False):
                    continue
                
                # Search in title, description, and content
                searchable_text = ' '.join([
                    metadata.get('title', ''),
                    metadata.get('description', ''),
                    content
                ]).lower()
                
                # Simple keyword matching
                if query in searchable_text:
                    # Calculate relevance score (simple)
                    score = 0
                    
                    # Title match is most important
                    if query in metadata.get('title', '').lower():
                        score += 10
                    
                    # Description match
                    if query in metadata.get('description', '').lower():
                        score += 5
                    
                    # Content match
                    content_matches = searchable_text.count(query)
                    score += content_matches
                    
                    # Extract snippet around match
                    snippet = self._extract_snippet(content, query)
                    
                    results.append({
                        'title': metadata.get('title', page_info.get('slug', 'Untitled')),
                        'slug': metadata.get('slug', page_info.get('slug')),
                        'description': metadata.get('description', ''),
                        'snippet': snippet,
                        'score': score,
                        'file_path': page_info['file_path']
                    })
            except Exception as e:
                print(f"Error searching page {page_info['file_path']}: {e}")
                continue
        
        # Sort by relevance score and limit results
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:limit]
    
    def _extract_snippet(self, content: str, query: str, snippet_length: int = 150) -> str:
        """Extract a snippet around the search query"""
        content_lower = content.lower()
        query_lower = query.lower()
        
        # Find the first occurrence of the query
        index = content_lower.find(query_lower)
        if index == -1:
            # If not found, return the first part of content
            return content[:snippet_length] + "..." if len(content) > snippet_length else content
        
        # Calculate snippet boundaries
        start = max(0, index - snippet_length // 2)
        end = min(len(content), index + len(query) + snippet_length // 2)
        
        snippet = content[start:end]
        
        # Add ellipsis if needed
        if start > 0:
            snippet = "..." + snippet
        if end < len(content):
            snippet = snippet + "..."
        
        return snippet

    def get_search_suggestions(self, query: str, limit: int = 5) -> List[str]:
        """Get search suggestions based on existing content"""
        if not query or len(query.strip()) < 2:
            return []
        
        suggestions = set()
        pages = self.content_loader.list_pages()
        
        for page_info in pages[:20]:  # Limit to recent pages for performance
            try:
                metadata, content = self.content_loader.load_page_by_path(page_info['file_path'])
                
                # Extract words from title and content
                title = metadata.get('title', '')
                words = re.findall(r'\b\w{3,}\b', (title + ' ' + content).lower())
                
                for word in words:
                    if query.lower() in word and word not in suggestions:
                        suggestions.add(word)
                        if len(suggestions) >= limit:
                            break
                            
            except Exception:
                continue
        
        return list(suggestions)[:limit]
