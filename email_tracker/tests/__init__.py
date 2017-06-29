import django

if django.VERSION < (1, 7):
    from .test_models import *  # NOQA
    from .test_backend import *  # NOQA
    from .test_admin import *  # NOQA
