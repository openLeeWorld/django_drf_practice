import os
from datetime import timedelta
from pathlib import Path
from typing import List

import django_stubs_ext  # 타입 힌팅 패키지

django_stubs_ext.monkeypatch()  # 타입 정보를 동적으로 수정하는 monkey patching

# try: import pymysql 은 생략 (DB는 sqlite 기본 씀)

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-8z%ipi9j4wg6+56@n%u@hr4*t^y#i8h+)9k45+z@j@)gfi**$_'

DEBUG = True

ALLOWED_HOSTS: List[str] = ["*"]

# Application Definition
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "rest_framework",
    "django_extensions",
    "drf_spectacular",
    "django_filters",
    "channels",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "ninja",
    # your apps
    "authentication",
    "users",
    "stores",
    "orders",
    "products",
    #"django_ninja_sample"
]

AUTH_USER_MODEL = "users.User"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "config.urls"  # config.urls.py가 기본임

REST_FRAMEWORK = {  # 프로젝트 내 DRF 관련 공통 Config
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",  # DRF의 DateTimeField는 이 포맷으로 직렬화
    "DATE_FORMAT": "%Y-%m-%d",  # DateField 직렬화
    "PAGE_SIZE": 100,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework_simplejwt.authentication.JWTStatelessUserAuthentication",
        # "rest_framework_simplejwt.authentication.JWTAuthentication", 가 기본
        # "rest_framework.authentication.SessionAuthentication", 대신 jwt 사용
    ],
}

SPECTACULAR_SETTINGS = {  # DRF-spectacular : OPENAPI 문서 자동 생성
    # General schema metadata. Refer to spec for valid inputs
    # https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#openapi-object
    "TITLE": "백엔드 개발을 위한 핸즈온 장고 학습예제 API 문서",
    "DESCRIPTION": "출처: https://github.com/KimSoungRyoul/backend-handson-django",
    "CONTACT": {"name": "kimsoungryoul", "url": "http://www.example.com/support", "email": "KimSoungRyoul@gmail.com"},
    "SWAGGER_UI_SETTINGS": {  # Swagger UI를 편리하게 사용하기 위한 기본 옵션 수정
        "dom_id": "#swagger-ui",  # required(default)
        "layout": "BaseLayout",  # required(default)
        "deepLinking": True,  # API를 클릭할 때마다 SwaggerUI의 URL이 변경됨
        "persistAuthorization": True,  # Authorize에 입력된 정보가 새로고침을 하더라도 초기화x
        "displayOperationId": True,  # API의 urlId값을 노출합니다. 보통 DRF api name과 일치함
        "filter": True,  # Swagger UI 에서 'Filter by Tag' 검색이 가능함
    },
    "LICENSE": {  # name 필수
        "name": "MIT License",
        "url": "https://github.com/KimSoungRyoul/DjangoBackendProgramming/blob/django-backend-starter/LICENSE",
    },
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,  # OAS3 Meta 정보 API를 비노출
    "SWAGGER_UI_DIST": "//unpkg.com/swagger-ui-dist@4.19.0",  # Swagger UI 버전 조절
}

# Database
DATABASES = {
    # # sqlite sample
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR.parent / "db.sqlite3",
    },

    # postgres sample
    # "default": {
    #     "ENGINE": "django.db.backends.postgresql",
    #     "NAME": "django_db",
    #     "USER": "postgres",
    #     "PASSWORD": "1234",
    #     "HOST": "127.0.0.1",
    #     "PORT": "5432",
    # },

    # mysql sample
    # "default": {
    #     "ENGINE": "django.db.backends.mysql",
    #     "NAME": "django_db",
    #     "USER": "root",
    #     "PASSWORD": "password",
    #     "HOST": "127.0.0.1",
    #     "PORT": 3306,
    # },
}
# Session 방식 사용
# SESSION_COOKIE_AGE = 60 * 60 * 24 # 1 day
# SESSION_ENGINE = "django.contrib.session.backends.db" # rdb를 세션 저장소로
# SESSION_ENGINE = "django.contrib.session.backends.cached_db" # 메모리 DB(redis)를 세션 저장소로


# Redis 캐시 사용
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
    }
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],  # template directory는 BASE_DIR에 근거해서 등록
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

# WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# CHANNEL
# CHANNEL_LAYERS = {
# "default": {"BACKEND": "channels.layers.InMemoryChannelLayer"},
# you can use RedisChannelLayer after compose up "docker compose -f docker/compose.yaml up -d"
# "default": {"BACKEND": "channels_redis.core.RedisChannelLayer", "CONFIG": {"hosts": [("127.0.0.1", 6379)]}},
#}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "ko-KR"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images) (swagger, redoc static file)
STATIC_URL = "static/"
STATIC_ROOT = os.getenv("STATIC_ROOT", default=os.path.join(BASE_DIR.parent, STATIC_URL))

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        # 학습 목적으로 제가 임의로 정의한 log 포맷입니다.
        "common": {
            "format": "{levelname} {asctime} 로그 찍은 곳: {name} pid: {process:d} thread-id: {thread:d} \n  --> {message}\n",
            "style": "{",
        },
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "common",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "INFO",
        },
        # ---sql 로그를 보고싶지 않다면 "django.db.backends" 항목을 주석처리하세요---
        # "django.db.backends": {
        #     "handlers": ["console"],
        #     "level": "DEBUG",
        # },
        # --------------------------------------------------------------
    },
}

AES256_ENCRYPTION_KEY = b"d40e150996e5e6c10f08ba4efab746a3"
SEED256_ENCRYPTION_KEY = b"bd9fc900714c1f94"

# 장고 스토리지: FileSystemStorage
# DEFAULT_FILE_STORAGE = "django.core.files.storages.FileSystemStorage"
# MEDIA_URL = "/media/" # 업로드되는 파일을 조회할 경로를 선언
# MEDIA_ROOT = os.path.join(BASE_DIR, "media") # 장고에게 실제 파일 위치 알려주기

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.token.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "TOKEN_OBTAIN_SERIALIZER": "authentication.serializers.AuthTokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializer.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "authentication.serializers.AuthTokenBlacklistSerializer",
}
