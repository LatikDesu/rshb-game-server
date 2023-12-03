from os import getenv, path
from pathlib import Path

import dotenv
from django.core.management.utils import get_random_secret_key

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_file = BASE_DIR / ".env"

if path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

DEVELOPMENT_MODE = getenv("DEVELOPMENT_MODE", "False") == "True"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv("DJANGO_SECRET_KEY", get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getenv("DJANGO_DEBUG", False) == "True"

ALLOWED_HOSTS = getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "api",
]

MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "server.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "server.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if DEVELOPMENT_MODE is True:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "sql_db/db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": getenv("SQL_ENGINE", "django.db.backends.postgresql_psycopg2"),
            "NAME": getenv("SQL_DATABASE", "game_db"),
            "USER": getenv("SQL_USER", "postgres"),
            "PASSWORD": getenv("SQL_PASSWORD", "postgres"),
            "HOST": getenv("SQL_HOST", "db"),
            "PORT": getenv("SQL_PORT", "5432"),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Настройки Whitenoise
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "defaultModelsExpandDepth": -1,
        "defaultModelExpandDepth": 3,
    },
    "SHOW_REQUEST_BODY": True,
    "SHOW_RESPONSE_BODY": True,
    "DEFAULT_MODEL_DEPTH": None,
    "SERVE_INCLUDE_SCHEMA": False,
    "DISABLE_CACHE": True,
    "SCHEMA_PATH_PREFIX": "/api/v1",
    "TITLE": "Game API",
    "DESCRIPTION": "API игры для банка РСХБ, которую можно интегрировать в API на сайте банка. Цель игры - увеличить осведомленность пользователей о современных технологиях в сельском хозяйстве и вызвать у них интерес к участию в этой области.",
    "VERSION": "1.0.0",
    "CONTACT": {"name": "РСХБ в цифре", "url": "https://rshbdigital.ru/"},
    "TAGS": [
        {
            "name": "Player",
            "description": "Работа с моделями класса Игрок",
        },
        {
            "name": "Liderboard",
            "description": "Работа с рейтингом игроков",
        },
        {
            "name": "Statistics",
            "description": "Общая статистика",
        },
        {
            "name": "Equipment",
            "description": "Работа с моделями класса Оборудование",
        },
        {
            "name": "Harvest",
            "description": "Работа с моделями класса Урожай",
        },
        {
            "name": "Minigame",
            "description": "Работа с моделями класса Миниигры",
        },
    ],
}

# Domain names
DOMAIN = getenv("DOMAIN")
SITE_NAME = "Game"

CORS_ALLOWED_ORIGINS = getenv(
    "CORS_ALLOWED_ORIGINS", "http://127.0.0.1:8000,http://localhost:8000"
).split(",")
CORS_ALLOW_CREDENTIALS = True
