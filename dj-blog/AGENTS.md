# Agent Guidelines for Django Blog Project

This document provides guidelines and tips for AI agents working on this Django blog project.

## Project Structure Overview

*   **`blog/`**: Contains the core blog application logic, including models (`models.py`), views (`views.py`), forms (`forms.py`), URLs (`urls.py`), and templates related to blog posts and categories.
*   **`users/`**: Manages user authentication, custom user model (`models.py`), and related views/forms.
*   **`core/`**: Houses project-level settings (`settings/`), main URL configuration (`urls.py`), and WSGI/ASGI configurations.
    *   `core/settings/base.py`: Base settings applicable to all environments.
    *   `core/settings/dev.py`: Development-specific settings (e.g., SQLite, DEBUG=True).
    *   `core/settings/prod.py`: Production-specific settings (e.g., PostgreSQL, DEBUG=False, security settings).
*   **`templates/`**: Global templates and templates for apps that don't have their own `templates` directory. Overridden by app-specific templates.
*   **`theme/`**: Django app for Tailwind CSS integration.
    *   `theme/static_src/`: Contains Tailwind CSS source files (`styles.css`), `tailwind.config.js`, and `package.json`.
    *   `theme/static/`: Contains compiled CSS output.
    *   `theme/templates/`: May contain base templates or Tailwind-specific template tags/filters.
*   **`requirements.txt`**: Lists Python package dependencies.
*   **`manage.py`**: Django's command-line utility.
*   **`pytest.ini`**: Configuration for pytest.
*   **`conftest.py`**: Pytest fixtures and plugins.

## Development Workflow

1.  **Understand the Task**: Thoroughly read the user's request and any relevant context.
2.  **Explore**: Use tools like `ls`, `read_files`, and `grep` to understand the relevant parts of the codebase.
3.  **Plan**: Create a detailed, step-by-step plan using `set_plan`. Ensure the plan addresses all aspects of the request.
4.  **Implement**:
    *   Follow Test-Driven Development (TDD) where practical: write tests first, then write the code to make them pass.
    *   Write clean, Pythonic, and Django-idiomatic code.
    *   Adhere to PEP 8 for Python code style.
    *   Make small, incremental changes.
5.  **Test**:
    *   Run `pytest` frequently to ensure your changes pass all tests.
    *   Aim for high test coverage (>=90% as per project requirements).
    *   Add new tests for any new functionality or bug fixes.
6.  **Review**: Before submitting, review your changes to ensure they are correct, efficient, and meet all requirements.
7.  **Submit**: Use `submit` with a clear branch name and a conventional commit message.

## Key Technologies & Conventions

*   **Django**: Version 5.0.1. Follow Django best practices.
*   **PostgreSQL**: The target database for production and development.
*   **Tailwind CSS**: Used for styling.
    *   Modify Tailwind styles in `theme/static_src/src/styles.css` or by adding/changing utility classes in templates.
    *   Rebuild CSS using `python manage.py tailwind build` or `python manage.py tailwind start` for live reloading.
*   **Pytest**: For testing. Write tests in the `tests/` directory of the relevant app (e.g., `blog/tests/test_article.py`).
*   **Environment Variables**: Settings in `core/settings/prod.py` and potentially `dev.py` are configured using environment variables (loaded from a `.env` file in the root via `python-dotenv`). Ensure any new sensitive configurations also use environment variables.
*   **Git Branching**: Use descriptive branch names (e.g., `feature/add-comments`, `fix/login-bug`).
*   **Commit Messages**: Follow conventional commit message format (e.g., `feat: Add comment editing functionality`).

## Specific Instructions

*   **Database Migrations**: If you change any models (`models.py`), you **must** create new migration files:
    ```bash
    python manage.py makemigrations <app_name>
    ```
    And then (conceptually, as you don't run `migrate` directly unless testing):
    ```bash
    python manage.py migrate
    ```
    The `submit` tool will handle the application of migrations.
*   **Static Files**:
    *   Place app-specific static files in `<app_name>/static/`.
    *   Global static files can be in a top-level `static/` directory if configured in `STATICFILES_DIRS`.
    *   Run `python manage.py collectstatic` (conceptually) when new static files are added or changed for production.
*   **Templates**:
    *   Prefer app-specific template directories: `<app_name>/templates/<app_name>/template.html`.
    *   Global templates are in `templates/`.
*   **Security**:
    *   Always be mindful of security best practices (XSS, CSRF, SQL injection, etc.).
    *   Use Django's built-in security features.
*   **Accessibility (WCAG 2.1 AA)**: Ensure frontend changes meet these standards. Use semantic HTML, ensure good color contrast, keyboard navigability, and ARIA attributes where appropriate.
*   **Performance**: Aim for Lighthouse scores >=90. Optimize queries, consider caching, and ensure efficient template rendering.

## What Not To Do

*   Do not commit sensitive information (API keys, passwords) directly into the code. Use environment variables.
*   Do not make large, monolithic changes. Break down tasks into smaller, manageable steps.
*   Do not skip writing tests.

By following these guidelines, you will help maintain the quality and consistency of the codebase.
