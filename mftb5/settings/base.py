from os import path

BASE_DIR = path.dirname(path.dirname(__file__))

DEBUG = False
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.messages',

    'pipeline',

    'mftb5',
    'mftb5.apps.music',
    'mftb5.apps.news',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'mftb5.urls'

WSGI_APPLICATION = 'mftb5.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': path.join(BASE_DIR, 'db.sqlite3'),
    }
}

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

USE_TZ = True

TEMPLATE_DIRS = (
    path.join(BASE_DIR, 'templates'),
)

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
)

MEDIA_URL = '/media/'
MEDIA_ROOT = path.join(BASE_DIR, 'media')
STATIC_URL = '/static/'
STATICFILES_DIRS = (path.join(BASE_DIR, 'static'),)
STATIC_ROOT = path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

PIPELINE_COMPILERS = ('pipeline.compilers.less.LessCompiler',)
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.slimit.SlimItCompressor'

PIPELINE_CSS = {
    'base': {
        'source_filenames': [
            'less/style.less',
        ],
        'output_filename': 'css/style.css',
    },
}

PIPELINE_JS = {
    'base': {
        'source_filenames': [
            'js/libs/pjax/jquery.pjax.js',
            'js/libs/handlebars/handlebars-v1.1.2.js',
            'js/libs/sticky/jquery.sticky.js',
            'js/libs/cookie/jquery.cookie.js',
            'js/libs/shuffle/jquery-shuffle.js',
            'js/libs/spin/spin.js',
            'js/libs/fastclick/fastclick.js',
            'js/script.js',
            'js/playlist.js',
        ],
        'output_filename': 'js/min/script.js',
    },
}
