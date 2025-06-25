import os
from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _

load_dotenv("./.env")
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("BASE_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.humanize",
    "users",
    "blog",
    "theme",
    "whoosh",
    "tailwind",
    "crispy_forms",
    "crispy_tailwind",
    "mptt",
    "taggit",
    "django_social_share",
    "django_browser_reload",
    "social_django",
    "django_ratelimit",
]

INSTALLED_APPS += ("django_summernote",)

INTERNAL_IPS = [
    "127.0.0.1",
]

SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    # django-ratelimit middleware should be placed after CsrfViewMiddleware and AuthenticationMiddleware
    # if you are using features that depend on request.user or CSRF tokens.
    # However, for general IP-based rate limiting, it can be higher.
    # For login attempts, it should be after AuthenticationMiddleware if using user-based keys.
    # Let's place it generally for now, can be adjusted.
    "django_ratelimit.middleware.RatelimitMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",
]


# Use the database-backed session engine
SESSION_ENGINE = "django.contrib.sessions.backends.db"

# Set a reasonable session cookie age (e.g., 1209600 seconds for 2 weeks)
SESSION_COOKIE_AGE = int(os.getenv("COOKIE_AGE"))


ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",

                'social_django.context_processors.backends',  # <--
                'social_django.context_processors.login_redirect', # <--
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators


AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "social_core.backends.github.GithubOAuth2",
    "social_core.backends.twitter.TwitterOAuth",
    "social_core.backends.facebook.FacebookOAuth2",
)


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

LANGUAGES = [
    ("en", _("English")),
    # Add other languages as needed
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, "locale"),
]


TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

TAILWIND_APP_NAME = "theme"


STATIC_URL = "static/"
MEDIA_URL = "/media/"

# CRISPY_TEMPLATE_PACK = "bootstrap5"


SOCIAL_AUTH_LOGIN_ERROR_URL = "users:settings"
SOCIAL_AUTH_LOGIN_REDIRECT_URL = "blog:articles"
SOCIAL_AUTH_RAISE_EXCEPTIONS = False

# Ensure these environment variables are set in your .env file
SOCIAL_AUTH_GITHUB_KEY = os.environ.get("GITHUB_CLIENT_ID")
SOCIAL_AUTH_GITHUB_SECRET = os.environ.get("GITHUB_CLIENT_SECRET")

# Example for Twitter (ensure you have python-social-auth[twitter] or similar)
# SOCIAL_AUTH_TWITTER_KEY = os.environ.get("SOCIAL_AUTH_TWITTER_KEY")
# SOCIAL_AUTH_TWITTER_SECRET = os.environ.get("SOCIAL_AUTH_TWITTER_SECRET")

# Example for Facebook (ensure you have python-social-auth[facebook] or similar)
# SOCIAL_AUTH_FACEBOOK_KEY = os.environ.get("SOCIAL_AUTH_FACEBOOK_KEY")
# SOCIAL_AUTH_FACEBOOK_SECRET = os.environ.get("SOCIAL_AUTH_FACEBOOK_SECRET")

X_FRAME_OPTIONS = "SAMEORIGIN"

LOGIN_REDIRECT_URL = "blog:articles"
LOGIN_URL = "users:login"

MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

AUTH_USER_MODEL = "users.CustomUser"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("HOST")
EMAIL_PORT = os.getenv("PORT", 587)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_USERNAME")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("MAIL_FROM")

SITE_TITLE = os.getenv("SITE_TITLE")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SUMMERNOTE_THEME = "bs4"
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"

CRISPY_TEMPLATE_PACK = "tailwind"

SUMMERNOTE_CONFIG = {
    "iframe": True,
    "summernote": {
        "width": "600",
        "height": "400",
        "styleTags": [
            "p",
            {
                "title": "Blockquote",
                "tag": "blockquote",
                "className": "blockquote",
                "value": "blockquote",
            },
            {
                "title": "Code Block",
                "tag": "pre",
                "className": "prettyprint lang-java",
                "value": "pre",
            },
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
        ],
        "airMode": False,
        "toolbar": [
            ["style", ["style"]],
            ["font", ["bold", "underline", "clear"]],
            ["color", ["color"]],
            ["para", ["ul", "ol", "paragraph"]],
            ["table", ["table"]],
            ["insert", ["link", "picture", "code"]],
            ["view", ["fullscreen", "codeview", "help"]],
        ],
    },
    "codemirror": {
        "mode": "htmlmixed",
        "lineNumbers": "true",
        "theme": "monokai",
    },
    "css": (
        "//cdnjs.cloudflare.com/ajax/libs/codemirror/5.29.0/theme/monokai.min.css",
    ),
    "attachment_require_authentication": True,
    "attachment_upload_to": "uploads/django-summernote",
    "attachment_absolute_uri": False,
}


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",  # Use database 1 for cache
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
        }
    }
}


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
}
