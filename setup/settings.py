from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------
# Ambiente / Render
# --------------------
ON_RENDER = bool(os.getenv("RENDER")) or bool(os.getenv("RENDER_EXTERNAL_HOSTNAME"))

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-dev-only")

# ✅ VOLTAMOS PARA A SEGURANÇA PADRÃO
# No Render, isso vai ser False automaticamente.
DEBUG = os.getenv("DEBUG", "0") == "1"
if ON_RENDER:
    DEBUG = False

# --------------------
# Hosts / CSRF
# --------------------
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

render_host = os.getenv("RENDER_EXTERNAL_HOSTNAME")
if render_host:
    ALLOWED_HOSTS.append(render_host)

# ✅ ADICIONADO: Domínio customizado (sem https)
# Isso permite que o Django aceite conexões vindas do seu domínio
ALLOWED_HOSTS.append("associacaomarciliomoraes.com.br")
ALLOWED_HOSTS.append("www.associacaomarciliomoraes.com.br")


CSRF_TRUSTED_ORIGINS = []
if render_host:
    CSRF_TRUSTED_ORIGINS.append(f"https://{render_host}")

# ✅ ADICIONADO: Domínio customizado (com https://)
# Isso permite fazer login e enviar formulários (evita erro de CSRF)
CSRF_TRUSTED_ORIGINS.append("https://associacaomarciliomoraes.com.br")
CSRF_TRUSTED_ORIGINS.append("https://www.associacaomarciliomoraes.com.br")

CSRF_TRUSTED_ORIGINS.append("https://*.onrender.com")

# --------------------
# Apps
# --------------------
INSTALLED_APPS = [
    "jazzmin",
    "cloudinary_storage", # Deve vir antes de staticfiles
    "django.contrib.staticfiles",
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

# Mantendo a configuração explícita que funcionou
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Whitenoise extra
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = DEBUG

# --------------------
# UPLOAD DE MÍDIA (FOTOS)
# --------------------
MEDIA_URL = "/media/"

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.getenv("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": os.getenv("CLOUDINARY_API_KEY"),
    "API_SECRET": os.getenv("CLOUDINARY_API_SECRET"),
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# --------------------
# Security (Produção)
# --------------------
if ON_RENDER:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

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
    "search_model": ["auth.User", "core.Atletas"],
    "show_ui_builder": True,
}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "dark_mode_theme": "darkly",
}