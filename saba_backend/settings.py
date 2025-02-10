import os
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Environment Configuration

DEBUG = config('DEBUG', cast=bool, default=False) # Set to False in Render Dashboard!
SECRET_KEY = config('SECRET_KEY')  # Set in Render Dashboard!

ALLOWED_HOSTS = []
RENDER_EXTERNAL_HOSTNAME = config('RENDER_EXTERNAL_HOSTNAME', default=None)
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
ALLOWED_HOSTS += ['127.0.0.1', 'localhost']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'class_management',
    'corsheaders',
]

REST_FRAMEWORK = {
'DEFAULT_AUTHENTICATION_CLASSES': [
    'rest_framework.authentication.TokenAuthentication',  # ✅ Use Token Authentication instead
    'rest_framework.authentication.BasicAuthentication',
],
'DEFAULT_PERMISSION_CLASSES': [
    'rest_framework.permissions.IsAuthenticated',  # ✅ Allows public API access (change for production)
]
}

AUTHENTICATION_BACKENDS = [
'django.contrib.auth.backends.ModelBackend',  # ✅ Ensure this is present
]
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # This should be at the top
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'saba_backend.urls'

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

WSGI_APPLICATION = 'saba_backend.wsgi.application'
AUTH_USER_MODEL = 'class_management.User'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='sabaDB'), # Set in Render Dashboard!
        'USER': config('DB_USER', default='postgres'), # Set in Render Dashboard!
        'PASSWORD': config('DB_PASSWORD', default='lier4638'), # Set in Render Dashboard!
        'HOST': config('DB_HOST', default='localhost'), # Set in Render Dashboard!
        'PORT': config('DB_PORT', default='7890'), # Set in Render Dashboard!
    }
}

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
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS Configuration (Production!)
CORS_ALLOW_ALL_ORIGINS = False  #  MUST be False in production
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',  # Replace with your frontend URL in production
    'http://127.0.0.1:3000',  # Replace with your frontend URL in production
]
CSRF_COOKIE_SECURE = True #ensure for production, should not be true in testing
CSRF_COOKIE_HTTPONLY = True #ensure for production
SESSION_COOKIE_SECURE = True #ensure for production