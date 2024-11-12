from pathlib import Path

from django.utils.translation import gettext_lazy as _
from environs import Env

env = Env()
env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env.str(
    'DJANGO_SECRET_KEY',
    default='XXXXXX',
)

ALLOWED_HOSTS = env.list(
    'DJANGO_ALLOWED_HOSTS',
    default=['*'],
)

DEBUG = env.bool(
    'DJANGO_DEBUG',
    default=False,
)

raw_value = env.str(
    'DJANGO_ALLOW_REVERSE',
    default='',
)
ALLOW_REVERSE = raw_value.lower() in ('', 'true', 'yes', '1', 'y')

MAIL = env.str(
    'DJANGO_MAIL',
    default='no-reply@djangex-market.ru',
)

INSTALLED_APPS = [
    'about.apps.AboutConfig',
    'catalog.apps.CatalogConfig',
    'core.apps.CoreConfig',
    'download.apps.DownloadConfig',
    'feedback.apps.FeedbackConfig',
    'homepage.apps.HomepageConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'sorl.thumbnail',
    'tinymce',
    'django_cleanup.apps.CleanupConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'lyceum.middleware.ReverseMiddleware',
]

if DEBUG:
    INTERNAL_IPS = [
        '127.0.0.1',
    ]
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

ROOT_URLCONF = 'lyceum.urls'

TEMPLATES_DIRS = [BASE_DIR / 'templates']

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': TEMPLATES_DIRS,
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

WSGI_APPLICATION = 'lyceum.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation'
            '.UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.MinimumLengthValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.NumericPasswordValidator'
        ),
    },
]

LANGUAGES = [
    ('ru', _('Russian')),
    ('en', _('English')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

LANGUAGE_CODE = 'ru-RU'

TEMPLATE_CONTEXT_PROCESSORS = ('django.core.context_processors.i18n',)

TIME_ZONE = 'Asia/Novosibirsk'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static_dev',
]

STATIC_ROOT = 'static'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = 'media/'

MEDIA_ROOT = BASE_DIR / 'media'

FIXTURE_DIRS = [
    BASE_DIR / 'fixtures',
]

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / 'send_mail'
