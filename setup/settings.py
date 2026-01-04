from pathlib import Path
import os
import dj_database_url
import sys

BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------
# Ambiente / Render
# --------------------
ON_RENDER = bool(os.getenv("RENDER")) or bool(os.getenv("RENDER_EXTERNAL_HOSTNAME"))

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-dev-only")

# --- MODO DE DEBUG FORÇADO (Para descobrirmos o erro) ---
# Depois que resolvermos, você volta para False.
DEBUG = True 

ALLOWED_HOSTS = ["*"] # Liberando tudo temporariamente para evitar erro de host

# --------------------
# Apps
# --------------------
INSTALLED_APPS = [
    "jazzmin",
    "cloudinary_storage", # Deve estar ANTES do staticfiles
    "django.contrib.staticfiles", # Deve estar DEPOIS do cloudinary_storage
    "cloudinary",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "setup.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "setup.wsgi.application"

# --------------------
# Database
# --------------------
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        ssl_require=ON_RENDER,
    )
}

# --------------------
# Password validators
# --------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Recife"
USE_I18N = True
USE_TZ = True

# --------------------
# ARQUIVOS ESTÁTICOS (CSS, JS)
# --------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

_static_dir = BASE_DIR / "static"
STATICFILES_DIRS = []
if _static_dir.exists():
    STATICFILES_DIRS.append(_static_dir)

# Essa configuração é OBRIGATÓRIA para o whitenoise funcionar sem o erro "AttributeError"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# --------------------
# UPLOAD DE MÍDIA (FOTOS)
# --------------------
MEDIA_URL = "/media/"

# Configuração do Cloudinary
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.getenv("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": os.getenv("CLOUDINARY_API_KEY"),
    "API_SECRET": os.getenv("CLOUDINARY_API_SECRET"),
}

# Essa configuração diz pro Django salvar os uploads na nuvem
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# --------------------
# Configurações Finais
# --------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

JAZZMIN_SETTINGS = {
    "site_title": "Gestão Judô",
    "site_header": "Gestão Judô",
    "site_brand": "Painel",
    "welcome_sign": "Bem-vindo",
    "copyright": "Associação Marcílio Moraes",
}