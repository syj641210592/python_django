"""
Django settings for main project.

Generated by 'django-admin startproject' using Django 3.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
import sys
import datetime
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-nofn%73bj=wb)ns$t#x4u#ul-pr0=qqz)pe#h*k+$*xh%6w!h)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# 允许用户访问web服务的ip或者域名, 默认只允许127.0.0.1或者localhost
ALLOWED_HOST = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin', 'django.contrib.auth',
    'django.contrib.contenttypes', 'django.contrib.sessions',
    'django.contrib.messages', 'django.contrib.staticfiles', 'projects',
    'interfaces', 'configures', 'debugtalks', 'envs', 'reports', 'testcases',
    'testsuites', 'users', 'rest_framework', 'corsheaders'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # 新增 ✔
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 指定允许跨域访问的ip
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = [
    # ‘<YOUR_DOMAIN>[:PORT]‘,
    'http://192.168.0.114:8080'
]

ROOT_URLCONF = 'main.urls'

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

WSGI_APPLICATION = 'main.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DATABASES = {
    # default为sql数据库在Django中的实例名, 可修改, 但必须至少存在一个default
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 数据库引擎
        'NAME': 'test_developer',  # 数据库名
        'USER': 'sunwang',  # 账号
        'PASSWORD': '334498Sun',  # 密码
        'HOST': 'rm-bp13q283436v06427zo.mysql.rds.aliyuncs.com',  # HOST
        'POST': 3306,  # 端口
    }
}

# 修改REST_FRAMEWORK全局默认配置
REST_FRAMEWORK = {
    # 渲染器
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",  # Json数据渲染器
        "rest_framework.renderers.BrowsableAPIRenderer"  # 网页数据渲染器
    ],
    # 过滤器
    "DEFAULT_FILTER_BACKENDS": [
        "rest_framework.filters.SearchFilter",  # 搜索过滤器
        "rest_framework.filters.OrderingFilter",  # 排序过滤器
    ],
    # 搜索关键字
    "SEARCH_PARAM":
    "search",
    # 排序关键字
    "ordering_PARAM":
    "ordering",
    # 分页引擎
    "DEFAULT_PAGINATION_CLASS":
    "utils.pagination.PageNumberPagination",
    # 分页关键字
    "Pagination_PARAM":
    "page",
    # 分页数据量
    "PAGE_SIZE":
    6,
    "DEFAULT_SCHEMA_CLASS":
    "rest_framework.schemas.coreapi.AutoSchema",
    # 在setting.py文件REST_FRAMEWORK中 修改全局认证类与授权类信息
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',  # 会话认证
        'rest_framework.authentication.BasicAuthentication'
        # 'rest_framework.authentication.BaseJSONWebTokenAuthentication',
    ],
    # # 指定全局权限[一般作为局部添加权限机制]
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAdminUser',  # 所有权限
    # ],
    # 时间格式
    'DATETIME_FORMAT':
    "%Y-%m-%d %H:%M:%S",
}

# 日志配置
LOGGING = {
    'version': 1,  # 使用的python内置的logging模块，那么python可能会对它进行升级，所以需要写一个版本号，目前就是1版本
    'disable_existing_loggers': False,  # 是否去掉目前项目中其他地方中以及使用的日志功能，但是将来我们可能会引入第三方的模块，里面可能内置了日志功能，所以尽量不要关闭。
    'formatters': {  # 日志记录格式
        'verbose': {  # levelname等级，asctime记录时间，module表示日志发生的文件名称，lineno行号，message错误信息
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {  # 过滤器：可以对日志进行输出时的过滤用的
        'require_debug_true': {  # 在debug=True下产生的一些日志信息，要不要记录日志，需要的话就在handlers中加上这个过滤器，不需要就不加
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {  # 和上面相反
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {  # 日志处理方式，日志实例
        'console': {  # 在控制台输出时的实例
            'level': 'DEBUG',  # 日志等级；debug是最低等级，那么只要比它高等级的信息都会被记录
            'filters': ['require_debug_true'],  # 在debug=True下才会打印在控制台
            'class': 'logging.StreamHandler',  # 使用的python的logging模块中的StreamHandler来进行输出
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            # 日志位置,日志文件名,日志保存目录必须手动创建
            'filename': os.path.join(BASE_DIR, "logs/luffy.log"),  # 注意，你的文件应该有读写权限。
            # 日志文件的最大值,这里我们设置300M
            'maxBytes': 300 * 1024 * 1024,
            # 日志文件的数量,设置最大日志数量为10
            'backupCount': 10,
            # 日志格式:详细格式
            'formatter': 'verbose',
            'encoding': 'utf-8',  # 设置默认编码，否则打印出来汉字乱码
        },
    },
    # 日志对象
    'loggers': {
        'django': {  # 和django结合起来使用，将django中之前的日志输出内容的时候，按照我们的日志配置进行输出，
            'handlers': ['console', 'file'],  # 将来项目上线，把console去掉
            'propagate': True,  # 冒泡：是否将日志信息记录冒泡给其他的日志处理系统，工作中都是True，不然django这个日志系统捕获到日志信息之后，其他模块中可能也有日志记录功能的模块，就获取不到这个日志信息了
        },
    }
}

# AUTH_USER_MODEL = "users.UserModelSeralizer"  # 子应用名. 模型序列化器名

JWT_AUTH = {
    # JWT关键字
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    # 过期时间 seconds秒 hours小时 days天 minutes分
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=300),
    # 定义Token返回时包含的信息
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'utils.jwt.jwt_response_payload_handler',
}
