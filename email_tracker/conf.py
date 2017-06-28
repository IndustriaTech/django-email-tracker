try:
    import anymail
except ImportError:
    anymail = False


class Settings:
    """
    Wrapper around Django's settings object to provide some defaults
    """
    from django.conf import settings as __settings
    __defaults = {}

    def __init__(self, **kwargs):
        self.__defaults = kwargs

    def __getattr__(self, name):
        try:
            return getattr(self.__settings, name)
        except AttributeError as e:
            try:
                return self.__defaults[name]
            except KeyError:
                raise e


settings = Settings(
    EMAIL_TRACKER_BACKEND='django.core.mail.backends.smtp.EmailBackend',
    EMAIL_TRACKER_USE_ANYMAIL=bool(anymail),
)
