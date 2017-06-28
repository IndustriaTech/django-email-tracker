import warnings

from django.core import mail
from django.core.mail.backends.smtp import EmailBackend
from email_tracker.models import TrackedEmail


class EmailTrackerBackend(EmailBackend):
    """
    Sends one or more EmailMessage objects and returns the number of email
    messages sent.
    Creates EmailMessage and EmailCategory (if needed) for every message
    with defined extra header

    """

    def send_messages(self, email_messages):
        if not email_messages:
            return
        with self._lock:
            new_conn_created = self.open()
            if not self.connection:
                # We failed silently on open().
                # Trying to send would be pointless.
                return
            num_sent = 0
            for message in email_messages:
                sent = self._send(message)
                if sent:
                    num_sent += 1
                self.track_message(message, bool(sent))
            if new_conn_created:
                self.close()
        return num_sent

    def track_message(self, message, is_sent):
        TrackedEmail.objects.create_from_message(message, is_sent=is_sent)


class LocmemTrackerBackend(EmailTrackerBackend):
    """
    Similar to Django's builtin locmem email backend used for testing
    but preserve SMPT email backend API
    """
    def __init__(self, *args, **kwargs):
        super(LocmemTrackerBackend, self).__init__(*args, **kwargs)
        if not hasattr(mail, 'outbox'):
            mail.outbox = []

    def open(self):
        # Fake SMTP connection creation
        self.connection = True
        # Tell that the connection was already created
        return False

    def close(self):
        # Do nothing because we do not have real connection
        pass

    def _send(self, message):
        # Fake sending the email
        mail.outbox.append(message)
        return True


def create_tracked_email(email_message, is_sent):
    warnings.warn('create_tracked_email is deprecated. Use TrackedEmail.objects.create_from_message instead',
                  DeprecationWarning,
                  stacklevel=2)
    return TrackedEmail.objects.create_from_message(email_message,
                                                    is_sent=is_sent)
