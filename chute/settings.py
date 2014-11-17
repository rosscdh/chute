"""
Django settings for chute project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

IS_TESTING = False
for test_app in ['testserver','test', 'jenkins']:
    if test_app in sys.argv[1:2]:
        IS_TESTING = True

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/
SITE_ID = 1

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_e@t%7j9xw4u-=1u-&#3=w(fj=e6z1!!_7bcg!ui=-omw&9k5='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
)

PROJECT_APPS = (
    'chute.apps.me',  # base user extended objects
    'chute.apps.client',  # base user client objects
    'chute.apps.project',  # container for playlists
    'chute.apps.feed',  # container for playlists
    'chute.apps.playlist',  # composed of various feed sequences
    'chute.apps.public',  # public views
    #'chute.apps.box',  # the individual box endpoints (clients)
)

DJANGO_CMS_APPS = (
)

HELPER_APPS = (
    'rest_framework',
    'rest_framework.authtoken',

    'sorl',
    'payments',
    'braces',

    'social.apps.django_app.default',

    'parsley',
    'crispy_forms',
    'templatetag_handlebars',

    # Asset pipeline
    'pipeline',
)


INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + HELPER_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'chute.urls'

WSGI_APPLICATION = 'chute.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)


AUTHENTICATION_BACKENDS = (
    'chute.auth_backends.EmailBackend',
    'social.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',

    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)


SOCIAL_AUTH_FACEBOOK_KEY = '317444045109900'
SOCIAL_AUTH_FACEBOOK_SECRET = '453cb652cff25fca613c2cfe1adebf21'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

PIPELINE_CSS = {
    'base': {
        'source_filenames': (
            'bootstrap/css/bootstrap.min.css',
            'css/sidebar.css',
        ),
        'output_filename': 'js/dist/base.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    }
}

PIPELINE_JS = {
    'base_ie_only': {
        'source_filenames': (
            'bootstrap/js/html5shiv.min.js',
            'bootstrap/js/respond.min.js',
        ),
        'output_filename': 'js/dist/base_ie_only.js'
    },
    'base': {
        'source_filenames': (
            'js/showdown-0.3.1.min.js',
        ),
        'output_filename': 'js/dist/base.js'
    },
    'ckeditor': {
        'source_filenames': (
            # helpers
            'ckeditor/ckeditor.js',
            'ckeditor/adapters/jquery.js',
        ),
        'output_filename': 'js/dist/ck.js'
    },
    'react': {
        'source_filenames': (
            'js/reactjs/0.11.1/react-with-addons.js',
            'js/common.jsx',
            'js/messages.jsx',
            #'js/videoplayer.jsx',
        ),
        'output_filename': 'js/dist/react.js'
    },
    'resources': {
        'source_filenames': (
            'js/resources/resource.js',  # api
            # resources api
            'js/resources/user_resource.js',
            'js/resources/project_resource.js',
            'js/resources/feed_resource.js',
            'js/resources/collaborator_resource.js',
            # 'js/resources/video_resource.js',
            # 'js/resources/comment_resource.js',
        ),
        'output_filename': 'js/dist/resources.js'
    },
    'project_list': {
        'source_filenames': (
            # helpers
            # resources
            'js/resources/project_resource.js',
            'js/project_list.jsx',
        ),
        'output_filename': 'js/project_list.js',
    },
    'project': {
        'source_filenames': (
            # helpers
            # react components
            'js/project_collaborators.jsx',
            # 'js/project_comments.jsx',
            # 'js/project_video.jsx',
            'js/project_detail.jsx',
        ),
        'output_filename': 'js/dist/project.js',
    },
    'chute': {
        'source_filenames': (
            'js/chute.jquery.js',
            'js/foggy-1.1.1.js',
        ),
        'output_filename': 'js/dist/chute.js',
    },
    
}

PIPELINE_COMPILERS = [
    'pipeline.compilers.less.LessCompiler',
    'react.utils.pipeline.JSXCompiler',
]

STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "sk_test_4TQt1KQ0HqJzsm4k6I98ppVQ")
STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY", "pk_test_4TQtMXsWeYaQHIsSoII3rrMc")
PAYMENTS_INVOICE_FROM_EMAIL = 'founders@chute.com'
PAYMENTS_PLANS = {
    "early-bird-monthly": {
        "stripe_plan_id": "early-bird-monthly",
        "name": "Subscription",
        "description": "A monthly subscription to make use of chute.com",
        "features": "Get access to our exclusive members are a bunch of other really cool stuff.",
        "price": 9.99,
        "currency": "usd",
        "interval": "month"
    }
}


VIMEO_SECRET_KEY = os.environ.get("VIMEO_SECRET_KEY", "5f612417220380d3098cf5416895f75a17a6495a")
VIMEO_PUBLIC_KEY = os.environ.get("VIMEO_PUBLIC_KEY", "0fca2de89814122b029493f21900a4e0d637ced1")

# Rest framework
REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.UnicodeJSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        # 'rest_framework.authentication.BasicAuthentication', # Here Temporarily for dev
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # only use this in dev
        # 'toolkit.apps.api.permissions.ApiObjectPermission',
    ],
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
    ),
    'PAGINATE_BY': 25,
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'medium': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'medium'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'medium'
        },
        'logfile': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': '/tmp/chute-{env}.log'.format(env='dev')
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins', 'console', 'logfile'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        }
    }
}


try:
    LOCAL_SETTINGS
except NameError:
    try:
        from local_settings import *
    except ImportError:
        pass

if IS_TESTING:
    try:
        from test_settings import *
    except ImportError:
        pass
