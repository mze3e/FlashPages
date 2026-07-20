# FlashPages

FlashPages is a file-based Content Management System (CMS) built with FastAPI. It combines the simplicity of Markdown with Git version control, allowing you to create, edit, and manage content through a clean web interface while storing everything as Markdown files with YAML front-matter.

It is designed with a "Streamlit-but-FastAPI" approach, providing a simple yet powerful way to build content-driven websites without requiring a traditional database for content storage.

## ✨ Features

- **File-based Content**: Content is stored in `content/pages/` as Markdown files with YAML front-matter.
- **Git Version Control**: Revisions and updates to content are tracked automatically using Git.
- **CMS Dashboard**: A clean web-based dashboard for managing content creation and editing.
- **Component System**: Use shorthand Markdown notation (e.g., `[component param="value"]`) to render beautiful Bootstrap 5 UI components (hero sections, cards, forms).
- **Customizable Theming**: Uses Bootstrap 5 and Bootswatch themes.
- **Interactive Modals**: Form management backend using PostgreSQL for handling email signups, contact forms, etc.

## 📋 Prerequisites

- **Python 3.11+**
- **[uv](https://docs.astral.sh/uv/)** (Extremely fast Python package installer and resolver)

## 🚀 Installation

1. Navigate into the project directory:
   ```bash
   cd FlashPages
   ```

2. Install dependencies using `uv`:
   ```bash
   uv sync
   ```
   *Note: This creates an isolated virtual environment and installs all dependencies listed in `pyproject.toml` and `uv.lock`.*

## 💻 Running the Application

You can start the FastAPI server using `uv run`:

```bash
uv run python main.py
```

Alternatively, you can run it via `uvicorn` with hot-reloading enabled for development:
```bash
uv run uvicorn main:app --host 0.0.0.0 --port 5000 --reload
```

The application will be accessible at: [http://localhost:5000](http://localhost:5000)

## 🛠️ Usage

### Accessing the CMS Dashboard

1. Once the server is running, navigate to `http://localhost:5000/auth/login`
2. Log in using the default admin credentials:
   - **Username**: `admin`
   - **Password**: `admin`

*(Note: These are the default credentials configured in `main.py`. You should update these and implement proper password hashing for production deployments.)*

### Managing Content

- Use the CMS Dashboard to create **New Pages**. The system will automatically generate URL slugs.
- Edit existing pages using the built-in Markdown editor.
- The system supports hierarchical navigation and SEO metadata built into the page's YAML front-matter.

### Configuration

You can customize the site by editing `config.yaml` at the root of the project:
- **Site Name and Theme**: Customize the global site title and Bootstrap theme.
- **Directories**: Modify where content and static files are stored.
- **Git Settings**: Adjust the repository path and default branch.

## 📄 License
MIT License
