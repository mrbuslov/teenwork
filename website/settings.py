from pathlib import Path
import os

import dotenv # чтобы можно было брать переменные из .env

if os.path.isfile(os.path.join(".env")):
    dotenv.load_dotenv(os.path.join(".env"))

# https://developer.mozilla.org/ru/docs/Learn/Server-side/Django/Deployment#%D1%87%D1%82%D0%BE_%D1%82%D0%B0%D0%BA%D0%BE%D0%B5_%D0%BE%D0%BA%D1%80%D1%83%D0%B6%D0%B5%D0%BD%D0%B8%D0%B5_%D1%80%D0%B0%D0%B7%D0%B2%D1%91%D1%80%D1%82%D1%8B%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = False


ALLOWED_HOSTS = ['*'] 
CSRF_TRUSTED_ORIGINS = ["teenwork.com.ua", "www.teenwork.com.ua"] # в django версии 4 добавь в начало https://

# http://127.0.0.1:8000/admin/sites/site
SITE_ID = 1

# Application definition

# pip freeze > requirements.txt      для того ,чтобы узнать, что установлено в проекте
INSTALLED_APPS = [
    'django.contrib.auth', # реализует подсистему разграничения доступа
    'modeltranslation',
    'django.contrib.admin',
    # 'django.contrib.admin.apps.SimpleAdminConfig',
    'django.contrib.contenttypes',
    'django.contrib.sessions', # подсистему, обслуживающую серверные сессии.
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    
    'chat',
    'board.apps.BoardConfig',
    'account',
    'telegram_filter',
    'website',
    
    'django_celery_beat', #celery (фоновые действия)
    'django_celery_results',
    'django_filters',
    'rosetta', # lang    https://djangopackages.org/grids/g/i18n/?python3=1
    # 'autotranslate', # lang
    # 'django_webp',
    # 'webp_converter',
    # https://overcoder.net/q/15876/%D0%BA%D0%B0%D0%BA-%D0%B7%D0%B0%D1%81%D1%82%D0%B0%D0%B2%D0%B8%D1%82%D1%8C-django-admin-%D1%83%D0%B4%D0%B0%D0%BB%D1%8F%D1%82%D1%8C-%D1%84%D0%B0%D0%B9%D0%BB%D1%8B-%D0%BF%D1%80%D0%B8-%D1%83%D0%B4%D0%B0%D0%BB%D0%B5%D0%BD%D0%B8%D0%B8-%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%D0%B0-%D0%B8%D0%B7-%D0%B1%D0%B0%D0%B7%D1%8B-%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85
    # 'django_cleanup', # для удаления изображений после удаления объекта
    'django_cleanup.apps.CleanupConfig',
]

AUTH_USER_MODEL = 'account.Account'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware', # lang
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'board.middleware.MyMiddleware', # логгер
]


ROOT_URLCONF = 'website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'django.template.context_processors.media',
                # 'django_webp.context_processors.webp',
                # 'webp_converter.context_processors.webp_support',
            ],
        },
    },
]

WSGI_APPLICATION = 'website.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',

        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'DB_NAME',
        'USER': 'YOUR_USERNAME', # postgres
        'PASSWORD': os.environ['PG_PASSWORD'],
        'HOST': 'YOUR_HOST',
        'PORT': 'YOUR_PORT',
        'ATOMIC_REQUESTS': True, # если у нас произошла ошибка при создании записи в БД, то она откатится (не создастся)  https://django.fun/docs/django/ru/3.2/topics/db/transactions/
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

# LANGUAGE_CODE = 'ru' # меняем с en-us на ru

TIME_ZONE = 'Europe/Kiev'
USE_I18N = True #будет активизирована встроенная в Dj ango система автоматического перевода на язык, записанный в параметре LANGUAGE CODE
USE_L10N = True # тrue, числа, значения даты и времени при выводе будут форматироваться по правилам языка из параметра LANGUAGE CODE


# import mimetypes
# mimetypes.add_type("text/javascript", ".js", True)
# mimetypes.add_type("text/html", ".html", True)
# mimetypes.add_type("text/css", ".css", True)

STATIC_URL = '/static/'
# STATIC_URL = '/board/static/'
STATIC_ROOT = "/ABSOLUTE/PATH/TO/STATIC_PARENT_FLD"
# STATICFILES_DIRS = (
# )
# STATICFILES_DIRS = (
#   os.path.join(BASE_DIR, 'board/static'),
# )
# STATICFILES_FINDERS = (
#     'django.contrib.staticfiles.finders.FileSystemFinder',
# )
MEDIA_URL='/'
MEDIA_ROOT = '/ABSOLUTE/PATH/TO/MEDIA_FLD/'

LOGIN_URL="/account/login/" # перенаправление на страницу, при попытке авторизоваться в админке
LOGIN_REDIRECT_URL="/account/" # перенаправление на адрес после успешной попытки входа на сайт
LOGOUT_REDIRECT_URL = '/'
# PASSWORD_RESET_TIMEOUT_DAYS - число дней, когда будет доступна ссылка пользователю по сбросу пароля в e-mail  

# SMTP Configuration
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'VPS.PROVIDER.SMTP.SERVER'
EMAIL_USE_SSL = True
#EMAIL_USE_TLS = True
EMAIL_PORT = 465 # 2525
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
SERVER_EMAIL = os.environ['EMAIL_HOST_USER']
DEFAULT_FROM_EMAIL = os.environ['EMAIL_HOST_USER']



# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
]


DEFAULT_AUTO_FIELD = 'django.db.models.AutoField' # для того, чтобы не появлялось "HINT: Configure the DEFAULT_AUTO_FIELD", когда запускаешь сервер или делаешь миграции

# telegram bot
TOKEN = os.environ['TELEGRAM_TOKEN']
PROXY_URL = 'https://telegg.ru/orig/bot' # для обхода блокировок Телеграма

# lang
from django.utils.translation import gettext_lazy as _
LANGUAGE_CODE = 'ru'

# rosetta
# http://127.0.0.1:8000/rosetta/files/project/
# python manage.py makemessages --all   (python manage.py makemessages --locale uk)
# python manage.py compilemessages 
LANGUAGES = (
    ('ru', _('Russian')),
    ('uk', _('Ukrainian'))
)
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

MODELTRANSLATION_LANGUAGES = ('ru', 'uk')
MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'

# Celery settings

# board/tasks.py
# website/celery.py

CELERY_TIMEZONE = "Europe/Kiev"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_BROKER_URL='redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'django-db' # admin celery tasks
CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = TIME_ZONE
# CELERYD_PREFETCH_MULTIPLIER


DATA_UPLOAD_MAX_NUMBER_FIELDS = 1500 # default 1000
# rosetta сколько может быть для перевода
ROSETTA_MESSAGES_PER_PAGE = 50


# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
# CONN_MAX_AGE = 0



# Логгирование ошибок
'''
Во views или middleware
logger = logging.getLogger(__name__)
logger.error(exception)
'''

'''
DEBUG: Системная информация низкого уровня для отладки.
INFO: Общая информация о системе
WARNING: Информация, описывающая возникшую незначительную проблему.
ERROR: Информация, описывающая возникшую серьезную проблему.
CRITICAL: Информация, описывающая возникшую критическую проблему.
'''

'''
ADMINS = [
    ('Dmitry' , 'buslovdmitrij0@gmail.com'),
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False, # для того , чтобы встроенные инструменты логгирования не отключались
    'formatters':{
        'extended': {
            'format': ' Time: {asctime}\n Filename:{filename} ({name} --- {pathname})\n Function:{funcName}\n Level:{levelname} (lvlnum:{levelno})\n Line:{lineno}\n Msg:{message}\n', #  {msg} - если хотим показать ошибку Exception`a
            'style': '{',
        },
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },  
    'loggers': {
        # 'board': {
        #     'handlers': ['file'],
        #     'level': 'WARNING', # все вместе : WARNING, ERROR, CRITICAL; DEBUG будет игнорироваться
        #     'propagate': True,
        # },
        'board': {
            'handlers': ['console', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True, # Если propagate установлен в False, то записи журнала не будут передаваться обработчикам.
        }
    },  
    'handlers': {
        # 'file': {
        #     'level': 'WARNING', # уровни логгирования 
        #     'class': 'logging.FileHandler',
        #     'filename': f'{BASE_DIR}/log.log',
        #     'formatter':'simple',
        # },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'extended',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'extended',
        },
    },
} 
'''