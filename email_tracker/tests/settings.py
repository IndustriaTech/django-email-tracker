ADMINS = ()
MANAGERS = ()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'email_tracker_tests.db',
    },
}

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'django.contrib.sessions',
    'email_tracker',
]

MIDDLEWARE = MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

EMAIL_BACKEND = 'email_tracker.backends.EmailTrackerBackend'
EMAIL_TRACKER_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

SECRET_KEY = 'very secred key ;)'

ROOT_URLCONF = 'email_tracker.tests.urls'
WSGI_APPLICATION = 'email_tracker.tests.wsgi.application'

TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
            ],
        },
    }
]

SILENCED_SYSTEM_CHECKS = [
    '1_8.W001',  # Silance warning for using TEMPLATE_*
    '1_10.W001',  # Silance warning for using MIDDLEWARE_CLASSES
]
