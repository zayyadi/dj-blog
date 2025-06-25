from .base import BASE_DIR
import os

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t") # Ensure DEBUG is False in prod
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "yourdomain.com,www.yourdomain.com").split(",") # Must be set in production!

DJANGO_LOG_LEVEL = os.environ.get("DJANGO_LOG_LEVEL", default="WARNING")

# HTTPS Settings (essential for production)
# Ensure your reverse proxy (e.g., Nginx) is configured to send these headers.
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https") # Uncomment and adjust if your proxy sends this
# SECURE_SSL_REDIRECT = os.getenv("DJANGO_SECURE_SSL_REDIRECT", "True").lower() == "true" # Set to True in production
# SESSION_COOKIE_SECURE = os.getenv("DJANGO_SESSION_COOKIE_SECURE", "True").lower() == "true" # Set to True in production
# CSRF_COOKIE_SECURE = os.getenv("DJANGO_CSRF_COOKIE_SECURE", "True").lower() == "true" # Set to True in production
# SECURE_HSTS_SECONDS = 31536000  # 1 year. Only if you are sure all content is served via HTTPS.
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True


DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DATABASE_ENGINE"),
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("POSTGRES_PORT"),
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
    },
    "handlers": {
        "default": {
            "level": DJANGO_LOG_LEVEL,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(str(BASE_DIR), "logs/app.log"),
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 5,
            "formatter": "standard",
        },
        "request_handler": {
            "level": DJANGO_LOG_LEVEL,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(str(BASE_DIR), "logs/django.log"),
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 5,
            "formatter": "standard",
        },
    },
    "loggers": {
        "": {"handlers": ["default"], "level": DJANGO_LOG_LEVEL, "propagate": True},
        "django.request": {
            "handlers": ["request_handler"],
            "level": DJANGO_LOG_LEVEL,
            "propagate": False,
        },
    },
}
