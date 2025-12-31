from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# =====================
# SEGURANÇA
# =====================
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-dev")

DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    "https://*.onrender.com",
]

# =====================
# APLICAÇÕES
# =====================
INSTALLED_APPS = [
    "jazzmin",  # SEMPRE PRIMEIRO
    "cloudinary",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
]

# =====================
# MIDDLEWARE
# =====================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # logo após SecurityMiddleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# =====================
# URLS / WSGI
# =====================
ROOT_URLCONF = "setup.urls"

WSGI_APPLICATION = "setup.wsgi.application"

# =====================
# TEMPLATES
# =====================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,  # NECESSÁRIO para Jazzmin
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

# =====================
# BANCO DE DADOS
# =====================
DATABASES = {
    "default": dj_database_url.config(
        default="sqlite:///db.sqlite3",
        conn_max_age=600,
        ssl_require=False,
    )
}

# =====================
# SENHAS
# =====================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# =====================
# LOCALIZAÇÃO
# =====================
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Recife"
USE_I18N = True
USE_TZ = True

# =====================
# STATIC FILES (RENDER + JAZZMIN)
# =====================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# 👉 SÓ use isso se você realmente tiver uma pasta /static no projeto
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []

# =====================
# STORAGES (Django moderno – evita conflito)
# =====================
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# =====================
# MEDIA (Cloudinary)
# =====================
MEDIA_URL = "/media/"

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.environ.get("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": os.environ.get("CLOUDINARY_API_KEY"),
    "API_SECRET": os.environ.get("CLOUDINARY_API_SECRET"),
}

# =====================
# JAZZMIN
# =====================
JAZZMIN_SETTINGS = {
    "site_title": "Marcílio Moraes",
    "site_header": "Gestão Judô",
    "site_brand": "Marcílio Moraes",
    "welcome_sign": "Bem-vindo ao Painel",
    "copyright": "Associação Marcílio Moraes",
    "search_model": ["auth.User", "core.Atletas"],
    "show_ui_builder": True,
}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "dark_mode_theme": "darkly",
}

# =====================
# PADRÃO
# =====================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
