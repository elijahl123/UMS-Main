"""
Django settings for UMSMain project.

Generated by 'django-admin startproject' using Django 3.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-zan^-=q)&l#lm%^wgsc+jss4lgk6!2!l=wtf4jg=qhjafd6=c-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['client.untitledmanagementsoftware.com']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    'storages',
    'rest_framework',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    'users',
    'payments',
    'school',
    'courses',
    'class_calendar',
    'homework',
    'notes'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'base.middleware.BaseMiddleware'
]

ROOT_URLCONF = 'UMSMain.urls'

AUTH_USER_MODEL = 'users.Account'

SITE_ID = 1

ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_AUTHENTICATION_METHOD = 'email'

ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': '9730399367-hikc9cjjco8kpn750po400dmo4ke3uhu.apps.googleusercontent.com',
            'secret': 'OunQv9kY3lmfXdaRGBOuo6JH'
        }
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

WSGI_APPLICATION = 'UMSMain.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'umsdb',
        'USER': 'umsmain',
        'PASSWORD': '%%55JUde',
        'HOST': 'ums-database-do-user-7877358-0.b.db.ondigitalocean.com',
        'PORT': '25060',
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Hawaii'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

ADMINS = [
    ('Elijah Lopez', 'elijah.kane.1972@gmail.com')
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AWS_ACCESS_KEY_ID = 'JN732ZR5XW57CYVFKORZ'
AWS_SECRET_ACCESS_KEY = 'BM8s92CyspOg7kCW1gOH4uYFuOIM4ip3dMeczKzXDVc'
AWS_STORAGE_BUCKET_NAME = 'umstatic'
AWS_S3_ENDPOINT_URL = 'https://sfo3.digitaloceanspaces.com/'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'
AWS_DEFAULT_ACL = 'public-read'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'media')
]

STATICFILES_STORAGE = 'custom_storages.StaticStorage'
DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'

# Use AWS_S3_ENDPOINT_URL here if you haven't enabled the CDN and got a custom domain.
STATIC_URL = '{}/{}/'.format(AWS_S3_ENDPOINT_URL, 'static')
# STATIC_ROOT = 'static/'

MEDIA_URL = '{}/{}/'.format(AWS_S3_ENDPOINT_URL, 'media')
# MEDIA_ROOT = 'media/'

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST_USER = 'untitledmanagementsoftware@gmail.com'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_PASSWORD = "%%55JUde"

ADMIN_EMAIL = "Untitled Management Software <untitledmanagementsoftware@gmail.com>"
DEFAULT_FROM_EMAIL = ADMIN_EMAIL
SERVER_EMAIL = ADMIN_EMAIL

GOOGLE_API_SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/calendar.calendars',
    'https://www.googleapis.com/auth/calendar.events'
]

GOOGLE_API_CREDENTIALS = {
    "web": {
        "client_id": "9730399367-hikc9cjjco8kpn750po400dmo4ke3uhu.apps.googleusercontent.com",
        "project_id": "untitled-management-software",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "OunQv9kY3lmfXdaRGBOuo6JH",
        "redirect_uris": ["http://localhost/accounts/google/login/callback/",
                          "https://client.untitledmanagementsoftware.com/accounts/google/login/callback/",
                          "http://localhost/calendar/save-google-credentials/",
                          "https://client.untitledmanagementsoftware.com/calendar/save-google-credentials/",
                          "http://localhost/", "http://localhost/calendar/",
                          "https://client.untitledmanagementsoftware.com/calendar/"]
    }
}

RECAPTCHA_SITE_KEY = '6Le2Y4UcAAAAAOMRr_KcOWTH77zZ_915Z4LA4zPn'
RECAPTCHA_SECRET_KEY = '6Le2Y4UcAAAAAI-Zz6P9_OziS1WSWXdn3TRqOXRg'

STRIPE_API_KEY = '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'
STRIPE_PUBLIC_KEY = 'pk_live_51Ja9LKHqoFWABg3Gc6XbaoIjXFGzhHOSU9wtqra5QqMtG8KtrL05kzoWl2ttizSJRKS8FNZtkOzWzP2hw4DDRUiU00tQ7CsGKG'
STRIPE_SUBSCRIPTION_PRICE_ID_MONTHLY = 'price_1JuwRaHqoFWABg3GZ5CLu0xE'
STRIPE_SUBSCRIPTION_PRICE_ID_YEARLY = 'price_1JuwQeHqoFWABg3GKWYDaboy'
STRIPE_WEBHOOK_SECRET = 'we_1JuTWFHqoFWABg3G7BbREyuG'
