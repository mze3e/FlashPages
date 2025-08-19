# Overview

This is a file-based Content Management System (CMS) built with FastAPI that combines the simplicity of Markdown with Git version control. The system allows users to create, edit, and manage content through a web interface while storing everything as Markdown files with YAML front-matter. It features a clean CMS dashboard for content management and a public-facing website that renders the content with customizable Bootstrap themes.

The system is designed as a "Streamlit-but-FastAPI" approach, providing a simple yet powerful way to build content-driven websites without requiring a traditional database for content storage.

## Recent Updates (August 19, 2025)
- ✅ Resolved authentication route issues by fixing router order (auth routes must be before public catch-all routes)
- ✅ Fixed Jinja2 template filter issues (strftime, markdown, slugify filters now working properly)
- ✅ Complete application is fully functional with login (admin/admin), CMS dashboard, and content management
- ✅ All core features tested and working: file editing, Git integration, search, navigation, theming

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Template Engine**: Jinja2 with reusable macros and components
- **Styling**: Bootstrap 5 with Bootswatch theme support for easy customization
- **JavaScript**: jQuery for progressive enhancement and interactive features
- **Layout System**: Multiple layout templates (base, docs, landing) with component-based architecture
- **Responsive Design**: Mobile-first approach with Bootstrap's responsive utilities

## Backend Architecture
- **Web Framework**: FastAPI with session-based authentication
- **Content Processing**: Python-Markdown with extensions (fenced_code, tables, toc, attr_list, codehilite)
- **Security**: HTML sanitization using Bleach, CSRF protection, path validation
- **File Management**: File-based content storage with YAML front-matter parsing
- **Routing**: Modular router structure separating public and CMS functionality

## Content Management
- **File Structure**: Markdown files with YAML front-matter stored in `content/pages/`
- **Version Control**: Git integration for tracking all content changes with commit history
- **Content Model**: Pages support metadata like title, slug, layout, navigation order, and SEO data
- **Navigation**: Automatic navigation generation from page metadata with hierarchical support

## Authentication & Security
- **Authentication**: Session-based authentication with configurable modes
- **Authorization**: Role-based access control for CMS functionality
- **Security Measures**: CSRF token validation, HTML sanitization, file path validation, content size limits
- **XSS Prevention**: Comprehensive input sanitization and safe HTML rendering

## Service Layer
- **Content Loader**: Handles Markdown file parsing and metadata extraction
- **Git Repository**: Manages version control operations (commits, history, status)
- **Search Service**: Simple text-based search across all content
- **Navigation Builder**: Constructs hierarchical navigation from page metadata

# External Dependencies

## Core Framework Dependencies
- **FastAPI**: Web framework and API development
- **Jinja2**: Template engine for HTML rendering
- **Uvicorn/Gunicorn**: ASGI server for production deployment

## Content Processing
- **python-markdown**: Markdown to HTML conversion with extensions
- **PyYAML**: YAML front-matter parsing and configuration
- **bleach**: HTML sanitization and XSS prevention

## Version Control
- **Git**: Version control system (via subprocess calls)
- **pygit2**: Alternative Git integration library (mentioned in specs)

## Frontend Assets (CDN)
- **Bootstrap 5**: CSS framework via CDN
- **Bootswatch**: Bootstrap theme variations
- **Font Awesome**: Icon library
- **jQuery**: JavaScript enhancement library
- **Highlight.js**: Code syntax highlighting

## Development & Security
- **Pydantic**: Data validation and form handling
- **python-multipart**: Form data processing
- **starlette.sessions**: Session management
- **passlib**: Password hashing (referenced in specs)

## Optional Integrations
- **SQLite**: Optional database for user management and logging
- **Authlib**: OAuth integration for alternative authentication
- **Pygments**: Enhanced code syntax highlighting