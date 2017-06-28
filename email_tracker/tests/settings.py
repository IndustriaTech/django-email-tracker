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
    'email_tracker',
]

EMAIL_BACKEND = 'email_tracker.backends.EmailTrackerBackend'
EMAIL_TRACKER_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

SECRET_KEY = 'very secred key ;)'
