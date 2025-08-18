---
title: Getting Started
slug: /getting-started
layout: docs.html
draft: false
nav_order: 10
description: Learn how to use the Content CMS to manage your content
section: Documentation
---

# Getting Started with Content CMS

Welcome to Content CMS! This guide will help you get up and running quickly.

## What is Content CMS?

Content CMS is a file-based content management system that combines:

- **Markdown** for content creation
- **YAML front-matter** for metadata
- **Git** for version control
- **Jinja2** for templating
- **Bootstrap** for styling

## First Steps

### 1. Login to the CMS

Visit `/auth/login` and use the default credentials:
- Username: `admin`
- Password: `admin`

> **Security Note**: Change these credentials in production!

### 2. Understanding the Interface

The CMS dashboard provides:

- **Pages overview**: See all your content files
- **Recent activity**: Git commit history
- **Quick actions**: Create new pages, view changes

### 3. Creating Your First Page

1. Click "New Page" from the dashboard
2. Choose a filename (e.g., `my-first-page.md`)
3. Add content with front-matter:

```markdown
---
title: My First Page
slug: /my-first-page
layout: docs.html
draft: false
nav_order: 20
description: This is my first page
---

# My First Page

Welcome to my new page! This content is written in **Markdown**.

## Features

- Easy to write
- Version controlled
- Responsive design
