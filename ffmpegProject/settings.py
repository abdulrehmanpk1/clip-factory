import os

from pathlib import Path

import dj_database_url
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-rq#r6z%86k3yyd&==23hwusw6s86w(yahsz4f91rmwnvy&n+#0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)

#CORS_ALLOWED_ORIGINS = [
#    "https://clipfactorypro.forbmax.ai",
#    "http://192.168.18.171:9999",
#]

# CORS_ALLOW_HEADERS = (
#     "accept",
#     "authorization",
#     "content-type",
#     "user-agent",
#     "x-csrftoken",
#     "x-requested-with",
# )

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ffmpegProject.urls'

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

WSGI_APPLICATION = 'ffmpegProject.wsgi.application'


# CORS_ALLOWED_ORIGINS = [
#     "http://192.168.18.67:9909",  # Add your frontend domain here
#     "http://58.65.176.166:9909",
#     "http://192.168.18.67:6173",
#     "http://192.168.18.67:19006",
#     "http://192.168.18.233:8000",
#     "http://192.168.18.67:5174",
#     "http://192.168.18.67:5173",
#     "http://192.168.18.67:5175",
#     "http://192.168.18.67:5176",
#     "http://192.168.18.67:7179",
#     'http://192.168.18.67:5179',
#     'http://192.168.18.67:5180',
#     'http://192.168.18.67:5177',
#     'http://192.168.18.67:5178',
#     'http://192.168.18.79',
#     "http://localhost:8000",
#     "http://192.168.18.67:7173",
#     "http://192.168.18.67:8173",
#     "http://192.168.18.67:8082",
#     "http://127.0.0.1:5500",
#     'http://192.168.18.67:6174',
#     'http://192.168.18.67:9999',
# ]

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# Database
#DATABASES = {
#    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL', 'postgres://root:mark12@db/markdb'))
#}
# Database
DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL', 'postgres://root:mark12@db:5432/markdb'))
}
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql',
#        'NAME': os.environ.get('POSTGRES_DB', 'markdb'),  # Database name
#        'USER': os.environ.get('POSTGRES_USER', 'root'),  # Database user
#        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'mark12'),  # Database password
#        'HOST': 'db',  # This matches the service name in docker-compose
#        'PORT': '5432',  # Default PostgreSQL port
#    }
#}
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
