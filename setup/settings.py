from pathlib import Path
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- SEGURANÇA ---
# Em produção (Render), a chave deve vir das variáveis de ambiente.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-chave-padrao-desenvolvimento')

# DEBUG: False em produção (se a variável RENDER existir), True localmente.
DEBUG = 'RENDER' not in os.environ

ALLOWED_HOSTS = ['*']

# IMPORTANTE PARA ONLINE: Permite o login via HTTPS no Render
# Substitua pelo seu domínio real se tiver um personalizado, ou mantenha o onrender.com
CSRF_TRUSTED_ORIGINS = ['https://*.onrender.com']

# Application definition

INSTALLED_APPS = [
    # 1. JAZZMIN (Tem que ser o primeiro da lista!)
    'jazzmin',

    # 2. Apps do Cloudinary
    'cloudinary_storage',
    'cloudinary',

    # 3. Apps Padrão do Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 4. Seu app principal
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware", # O Whitenoise fica aqui (Crucial para o CSS online)
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'setup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'setup.wsgi.application'


# --- BANCO DE DADOS ---
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}


# --- VALIDAÇÃO DE SENHA ---
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# --- INTERNACIONALIZAÇÃO ---
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Recife'
USE_I18N = True
USE_TZ = True


# --- ARQUIVOS ESTÁTICOS (CSS, JS) ---
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Essa configuração garante que o Whitenoise sirva os arquivos de forma otimizada e comprimida
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# --- ARQUIVOS DE MÍDIA (FOTOS) ---
MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dwt6fblk4',
    'API_KEY': '168731212392565',
    'API_SECRET': 'EtYahWFSKxdy37YqOAnZonGVhgQ'
}


# --- CONFIGURAÇÃO JAZZMIN (Visual do Admin) ---
JAZZMIN_SETTINGS = {
    "site_title": "Marcílio Moraes Admin",
    "site_header": "Gestão Judô",
    "site_brand": "Marcílio Moraes",
    "welcome_sign": "Painel Administrativo",
    "copyright": "Associação Marcílio Moraes",
    "search_model": ["auth.User", "core.Atletas"], # Barra de busca no topo

    # Ícones do Menu Lateral (FontAwesome)
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "core.Atletas": "fas fa-user-ninja",
        "core.Eventos": "fas fa-calendar-alt",
        "core.Contatos": "fas fa-address-book",
    },
    
    "show_ui_builder": True, # Botão para personalizar cores
}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly", # Tema moderno (azul e branco)
    "dark_mode_theme": "darkly",
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'