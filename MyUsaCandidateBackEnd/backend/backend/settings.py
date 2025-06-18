# settings.py

from pathlib import Path
import os
import environ

# ─── BASE DIR ─────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# ─── ENVIRONMENT ──────────────────────────────────────────────────
env = environ.Env(
    # set casting and default values
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
)

# read .env file at project root
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# ─── SECURITY ─────────────────────────────────────────────────────
SECRET_KEY = env("SECRET_KEY")
DEBUG      = env("DEBUG")
ALLOWED_HOSTS = env("ALLOWED_HOSTS")

# ─── APPLICATION DEFINITION ───────────────────────────────────────
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "django_filters",
    "corsheaders",
    "candidates",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"

# ─── DATABASE ─────────────────────────────────────────────────────
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ─── REST FRAMEWORK & CORS ───────────────────────────────────────
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 25,
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
    ),
}

CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])
CORS_ALLOW_ALL_ORIGINS = env.bool("CORS_ALLOW_ALL_ORIGINS", default=False)

# ─── PASSWORD VALIDATION ─────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

# ─── INTERNATIONALIZATION ────────────────────────────────────────
LANGUAGE_CODE = "en-us"
TIME_ZONE     = "UTC"
USE_I18N      = True
USE_TZ        = True

# ─── STATIC & MEDIA ──────────────────────────────────────────────
STATIC_URL = "/static/"
MEDIA_URL  = "/media/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
MEDIA_ROOT  = os.path.join(BASE_DIR, "media")

# ─── EXTERNAL ENDPOINTS ──────────────────────────────────────────
WIKIDATA_SPARQL_ENDPOINT = env(
    "WIKIDATA_SPARQL_ENDPOINT",
    default="https://query.wikidata.org/sparql",
)

# ─── DEFAULT PK FIELD TYPE ───────────────────────────────────────
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
