import django

if django.VERSION < (1, 7):
    from .test_backend import *  # NOQA
