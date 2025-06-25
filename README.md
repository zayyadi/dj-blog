# Django Blog Project

This is a Django-based blog application.

## Project Overview

This project aims to provide a full-featured blog platform including:

*   Full CRUD functionality for posts.
*   User authentication (including social login).
*   Comment system.
*   SEO optimization (meta tags, sitemaps).
*   Responsive, accessible templates using Tailwind CSS.
*   Security hardening.

## Setup Instructions

### Prerequisites

*   Python 3.x
*   PostgreSQL
*   Git

### Local Development Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up PostgreSQL:**
    *   Ensure PostgreSQL is installed and running.
    *   Create a database (e.g., `blog_dev`).
    *   Create a PostgreSQL user with privileges to access the database.
    *   Update database credentials in `core/settings/dev.py` or use environment variables.
        *   For development, you might need to set environment variables like `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `POSTGRES_PORT` if `core/settings/dev.py` is configured to use them.
        *   The current `core/settings/dev.py` has been updated to use:
            *   `NAME: "blog_dev"`
            *   `USER: "postgres"`
            *   `PASSWORD: "password"` (Please change this to a secure password)
            *   `HOST: "localhost"`
            *   `PORT: "5432"`

5.  **Set up environment variables:**
    *   Copy `.env.example` (if provided) to `.env` and fill in the necessary values.
    *   Required variables typically include `BASE_SECRET_KEY`, database credentials (if not hardcoded for dev), email settings, etc.
    *   The `core/settings/base.py` loads variables from a `.env` file in the project root.
    *   Key environment variables used:
        *   `BASE_SECRET_KEY`: Django secret key.
        *   `COOKIE_AGE`: Session cookie age in seconds.
        *   `ADMIN_INTERNAL_URL`: URL for the admin interface.
        *   `CLIENT_ID`, `CLIENT_SECRET`: For social auth (e.g., GitHub).
        *   `HOST`, `PORT`, `USERNAME`, `PASSWORD`, `MAIL_FROM`: For email configuration.
        *   `SITE_TITLE`: Title for the site.
        *   For production (`core/settings/prod.py`):
            *   `SECRET_KEY`
            *   `DEBUG` (set to `False`)
            *   `DATABASE_ENGINE`
            *   `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `POSTGRES_PORT`

6.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

7.  **Create a superuser (optional):**
    ```bash
    python manage.py createsuperuser
    ```

8.  **Load initial data (if fixtures are provided):**
    ```bash
    python manage.py load_fixtures
    ```
    *(Note: A `load_fixtures` custom command exists in `blog/management/commands/`)*

9.  **Compile Tailwind CSS (if needed):**
    *   The project uses `django-tailwind`. Ensure Node.js and npm are installed.
    *   Navigate to the `theme/static_src/` directory (or wherever your Tailwind `package.json` is located).
    *   Install Node.js dependencies:
        ```bash
        npm install
        ```
    *   Run the Tailwind build process (check `package.json` for scripts, often `npm run build` or `npm run watch`):
        ```bash
        # Example, might vary based on django-tailwind setup
        python manage.py tailwind install
        python manage.py tailwind build
        # or to watch for changes during development
        python manage.py tailwind start
        ```

10. **Run the development server:**
    ```bash
    python manage.py runserver
    ```

    The application should now be accessible at `http://127.0.0.1:8000/`.

### Running Tests

To run the test suite:

```bash
pytest
```

To get a coverage report:

```bash
pytest --cov=.
```

## Deployment

*(Details to be added later, typically involves configuring a production server like Gunicorn/uWSGI, Nginx, and setting up environment variables for production settings in `core/settings/prod.py`)*

## Contributing

*(Guidelines for contributing to the project - to be added if applicable)*
