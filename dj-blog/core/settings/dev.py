from .base import *
import os

DEBUG = True

ALLOWED_HOSTS = ["*"]

# Use PostgreSQL for development to match production
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME"),  # Or use an environment variable
        "USER": os.environ.get("DB_USER"),  # Or use an environment variable
        "PASSWORD": os.environ.get("DB_PASSWORD"),  # Or use an environment variable - use a secure password
        "HOST": os.environ.get("DB_HOST"),  # Or use an environment variable
        "PORT": os.environ.get("DB_PORT"),  # Or use an environment variable
    }
}
