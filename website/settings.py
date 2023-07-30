from pathlib import Path
import os

from django.utils.translation import gettext_lazy as _
import dotenv # чтобы можно было брать переменные из .env

if os.path.isfile(os.path.join(".env")):
    dotenv.load_dotenv(os.path.join(".env"))


BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = True
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'board/static')
MEDIA_URL = '/images/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'images')
CKEDITOR_UPLOAD_PATH = 'images/blog'
# telegram bot
TOKEN = os.environ['TELEGRAM_TOKEN']
NP_KEY = os.environ['NP_KEY']

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ["teenwork.com.ua", "www.teenwork.com.ua"] # в django версии 4 добавь в начало https://

# http://127.0.0.1:8000/admin/sites/site
SITE_ID = 1


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
    
    'django_extensions',
    'django_filters',
    'rosetta', # lang 
    'django_cleanup.apps.CleanupConfig', # для удаления изображений после удаления объекта
    
    'ckeditor',
    'ckeditor_uploader',
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

    # 'board.middleware.MyMiddleware', # логгер
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
            ],
        },
    },
]

WSGI_APPLICATION = 'website.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        ### Running POSTGRESQL db for production dev
        # "ENGINE": os.environ.get("POSTGRES_ENGINE", "django.db.backends.sqlite3"),
        # "NAME": os.environ.get("POSTGRES_DATABASE", BASE_DIR / "db.sqlite3"),
        # "USER": os.environ.get("POSTGRES_USER", "user"),
        # "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "password"),
        # "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        # "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        # 'ATOMIC_REQUESTS': True, 

        ### Running SQLite db for local dev
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.join(BASE_DIR, 'db.sqlite3')),
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

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

TIME_ZONE = 'Europe/Kiev'
USE_I18N = True # будет активизирована встроенная в Dj ango система автоматического перевода на язык, записанный в параметре LANGUAGE CODE
USE_L10N = True # тrue, числа, значения даты и времени при выводе будут форматироваться по правилам языка из параметра LANGUAGE CODE

LOGIN_URL="/login/" # перенаправление на страницу, при попытке авторизоваться в админке
LOGIN_REDIRECT_URL="/account/" # перенаправление на адрес после успешной попытки входа на сайт
LOGOUT_REDIRECT_URL = '/'
# PASSWORD_RESET_TIMEOUT_DAYS - число дней, когда будет доступна ссылка пользователю по сбросу пароля в e-mail  

# # SMTP Configuration
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_USE_SSL = True
# #EMAIL_USE_TLS = True
# EMAIL_PORT = 465 # 2525
# EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
# EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
# SERVER_EMAIL = os.environ['EMAIL_HOST_USER']
# DEFAULT_FROM_EMAIL = os.environ['EMAIL_HOST_USER']

EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', None)
EMAIL_HOST = os.environ.get('EMAIL_HOST', None)
EMAIL_PORT = os.environ.get('EMAIL_PORT', None)
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', None)
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', None)
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', None)

# rosetta
# http://127.0.0.1/rosetta/files/project/
# python manage.py makemessages --all   (python manage.py makemessages --locale uk)
# python manage.py compilemessages 
LANGUAGE_CODE = 'uk'
LANGUAGES = (
    ('en', _('English')),
    # ('ru', _('Russian')),
    ('uk', _('Ukrainian'))
)
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# MODELTRANSLATION_LANGUAGES = ('ru', 'uk')
MODELTRANSLATION_LANGUAGES = ('en', 'uk')
MODELTRANSLATION_DEFAULT_LANGUAGE = 'uk'

DATA_UPLOAD_MAX_NUMBER_FIELDS = 1500 # default 1000
# rosetta сколько может быть для перевода
ROSETTA_MESSAGES_PER_PAGE = 50
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField' # для того, чтобы не появлялось "HINT: Configure the DEFAULT_AUTO_FIELD", когда запускаешь сервер или делаешь миграции


# https://django-ckeditor.readthedocs.io/en/latest/
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList', '-', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['Image']
            # ['RemoveFormat', 'Source']
        ],
        'extraPlugins': ','.join([
            # 'codesnippet',
        ]),
        'extraAllowedContent':'iframe[*]',
        'allowedContent ':'iframe[*]',
    },
}




# https://www.youtube.com/watch?v=yvf_J225iM8&ab_channel=VeryAcademy
# after install Graphviz - pip install --global-option=build_ext --global-option="-IC:\Program Files\Graphviz\include" --global-option="-LC:\Program Files\Graphviz\lib" pygraphviz
# make image - https://django-extensions.readthedocs.io/en/latest/graph_models.html
# python manage.py graph_models --pygraphviz -a -g -o graph.png
GRAPH_MODELS = {
  'all_applications': True,
  'group_models': True,
}