"""
Django settings for bnlipsum project.
"""

from urlparse import urlparse
import os
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
DEBUG = os.getenv('DEBUG', False) and True or False
ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bnlipsum.lyrics'
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bnlipsum.urls'

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

WSGI_APPLICATION = 'bnlipsum.wsgi.application'

# Database
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///%s' % os.path.join(BASE_DIR, 'db.sqlite')
    )
}

if not DEBUG:
    DATABASES['default']['ENGINE'] = 'django_postgrespool'

# Honour the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Password validation
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
    }
]

# Internationalization
LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'Europe/London'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Cloud storage
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_S3_BUCKET')
AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_S3_CUSTOM_DOMAIN')
AWS_PRELOAD_METADATA = True
S3DIRECT_REGION = 'eu-west-1'

if not DEBUG:
    DEFAULT_FILE_STORAGE = 'screen.s3.MediaRootS3BotoStorage'
    STATICFILES_STORAGE = 'screen.s3.StaticRootS3BotoStorage'

MEDIA_URL = DEBUG and '/media/' or '//%s/media/' % AWS_S3_CUSTOM_DOMAIN
STATIC_URL = DEBUG and '/static/' or '//%s/static/' % AWS_S3_CUSTOM_DOMAIN

# Redis
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
REDIS_PROTOCOL, REDIS_HOST = tuple(urlparse(REDIS_URL))[:2]
REDIS_HOST, REDIS_PORT = REDIS_HOST.split(':')

# Sessions
SESSION_ENGINE = 'redis_sessions.session'

# Caching
def get_cache():
    try:
        os.environ['MEMCACHE_SERVERS'] = \
            os.environ['MEMCACHEDCLOUD_SERVERS'].replace(',', ';')

        os.environ['MEMCACHE_USERNAME'] = os.environ['MEMCACHEDCLOUD_USERNAME']
        os.environ['MEMCACHE_PASSWORD'] = os.environ['MEMCACHEDCLOUD_PASSWORD']

        return {
            'default': {
                'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
                'TIMEOUT': 500,
                'BINARY': True,
                'OPTIONS': {
                    'tcp_nodelay': True
                }
            }
        }
    except:
        return {
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
            }
        }

CACHES = get_cache()