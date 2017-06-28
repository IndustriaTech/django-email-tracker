import warnings
import threading

from django.core.mail import get_connection
from django.core.mail.backends.base import BaseEmailBackend

from email_tracker.conf import settings
from email_tracker.models import TrackedEmail


class EmailBackendWrapper(BaseEmailBackend):
    """
    Email backend wrapper that will wraps backend configured in
    settings.EMAIL_TRACKER_BACKEND
    """

    def __init__(self, **kwargs):
        super(EmailBackendWrapper, self).__init__(**kwargs)
        self.connection = get_connection(settings.EMAIL_TRACKER_BACKEND, **kwargs)
        self._lock = threading.RLock()

    def open(self):
        return self.connection.open()

    def close(self):
        return self.connection.close()

    def send_messages(self, email_messages):
        if not email_messages:
            return
        with self._lock:
            new_conn_created = self.open()
            num_sent = 0
            for message in email_messages:
                sent = self._send(message)
                if sent:
                    num_sent += 1
            if new_conn_created:
                self.close()
        return num_sent

    def _send(self, message):
        return self.connection.send_messages([message])


class EmailTrackerBackend(EmailBackendWrapper):
    """
    Sends one or more EmailMessage objects and returns the number of email
    messages sent.
    Creates EmailMessage and EmailCategory (if needed) for every message
    with defined extra header

    """

    def _send(self, message):
        sent = super(EmailTrackerBackend, self)._send(message)
        self.track_message(message, bool(sent))
        return sent

    def track_message(self, message, is_sent):
        TrackedEmail.objects.create_from_message(message, is_sent=is_sent)


def create_tracked_email(email_message, is_sent):
    warnings.warn('create_tracked_email is deprecated. Use TrackedEmail.objects.create_from_message instead',
                  DeprecationWarning,
                  stacklevel=2)
    return TrackedEmail.objects.create_from_message(email_message,
                                                    is_sent=is_sent)
