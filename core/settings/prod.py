from .base import BASE_DIR
import os

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", False)
DJANGO_LOG_LEVEL = os.environ.get("DJANGO_LOG_LEVEL", default="WARNING")

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
