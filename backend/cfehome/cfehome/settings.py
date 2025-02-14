"""
Django settings for cfehome project.

Generated by 'django-admin startproject' using Django 4.0.10.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-n*vih_u71os_@$9+y_p3i5o59!j4tm+a2y4xp%%_bv78b+ge4r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # this party api services,
    'algoliasearch_django',#ALGOLIA

    # third party libraries
    'rest_framework',
    'rest_framework.authtoken',

    'rest_framework_simplejwt',

    "corsheaders",


    #internal api 
    'api',
    'product',
    'search',
]

# auth_classes = [
#         #DECLARING AUTHENTICATION PATH
#         'rest_framework.authentication.SessionAuthentication',
#         'api.authentication.TokenAuthentication',
#         'rest_framework_simplejwt.authentication.JWTAuthentication'

# ] if DEBUG else [
#     'api.authentication.TokenAuthentication'
# ]


# print(auth_classes)
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',

        # 'api.authentication.TokenAuthentication',

    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly' # Get only is opened
    ],
    #paginate according to number of items offset style
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 5,
    #last settings overrides the previous one in case they are the same
    # paginate according to number of pages style
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 3,

}

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # new added cors before common midleware

    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
#
# CORS_URLS_REGEX=r"^^/api/.*"
'''
ERROR just by adding trailing slash, why ?
as he considered as a path not a domain
In CORS settings, the CORS_ALLOWED_ORIGINS should contain origins (i.e., the base URLs) without any path component. 
The origins should include the scheme (http or https), domain name, and port if not the default (80 for http, 443 for https
'''
CORS_ALLOWED_ORIGINS = [
    'http://0.0.0.0:8111', #this one doesn't work
    'http://localhost:8111',
    'http://127.0.0.0:8111',
    'null'

]
CSRF_TRUSTED_ORIGINS = [
    'http://0.0.0.0:8111', #this one doesn't work
    'http://localhost:8111',
    'http://127.0.0.0:8111',
]

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)
CORS_ALLOW_HEADERS = (
    "accept",
    "authorization",
    "Authorization",
    "Content-Type"
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
)

ROOT_URLCONF = 'cfehome.urls'

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

WSGI_APPLICATION = 'cfehome.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'auth.User'

ALGOLIA = {
    'APPLICATION_ID': 'OA3G9W9VR1',
    'API_KEY': 'e40aebb0dcc5f191242a0843e9bc09dc',
    'INDEX_PREFIX': 'al_search',
    # e40aebb0dcc5f191242a0843e9bc09dc # admin api key
    # 71d305dc9a7d6a156a89269df28f5c3a # usage api key
}

from datetime import timedelta
SIMPLE_JWT = {
    "AUTH_HEADER_NAME": "Authorization",
    "AUTH_HEADER_TYPES": ("Bearer",),

    "ACCESS_TOKEN_LIFETIME": timedelta(seconds=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    # "ROTATE_REFRESH_TOKENS": False,
    # "BLACKLIST_AFTER_ROTATION": False,
    # "UPDATE_LAST_LOGIN": False,

    # "ALGORITHM": "HS256",
    # "SIGNING_KEY": SECRET_KEY,
    # "VERIFYING_KEY": "",
    # "AUDIENCE": None,
    # "ISSUER": None,
    # "JSON_ENCODER": None,
    # "JWK_URL": None,
    # "LEEWAY": 0,
    # '''
        # very weird issue when i add AUTH_HEADER_NAME, the authentication doesn't work
    # '''
    #it's solved after changing the order of authentication middlewares above
    # "USER_ID_FIELD": "id",
    # "USER_ID_CLAIM": "user_id",
    # "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    # "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    # "TOKEN_TYPE_CLAIM": "token_type",
    # "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    # "JTI_CLAIM": "jti",

    # "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    # "SLIDING_TOKEN_LIFETIME": timedelta(minutes=30),
    # "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    # "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    # "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    # "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    # "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    # "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    # "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}
