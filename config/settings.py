import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Clave secreta: se lee desde variable de entorno.
# En producción debes definir DJANGO_SECRET_KEY con una clave real.
# La clave temporal de acá solo sirve para desarrollo local.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-clave-temporal-solo-para-desarrollo')

# Modo DEBUG: solo se activa si la variable DJANGO_DEBUG es exactamente "True".
# Si no está definida, DEBUG queda en False (seguro para producción).
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

# Hosts permitidos: en desarrollo acepta cualquiera.
# En producción se lee de la variable DJANGO_ALLOWED_HOSTS (varios separados por coma).
ALLOWED_HOSTS = ['*'] if DEBUG else os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'pacientes',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'es-CO'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

# Carpeta donde tenemos los archivos estáticos (CSS, JS, imágenes)
STATICFILES_DIRS = [BASE_DIR / 'static']

# Carpeta donde se copian al hacer collectstatic (para producción)
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/admin/login/'
