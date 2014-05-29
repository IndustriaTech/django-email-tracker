import datetime
from django.core.mail.backends.smtp import EmailBackend
from models import TrackedEmail, EmailCategory


def create_tracked_email(email_message, is_sent):
    header_category = email_message.extra_headers.get('X-Category')
    if header_category:
        category, created = EmailCategory.objects.get_or_create(
            title=header_category
        )
    else:
        category = None

    tracked_email = TrackedEmail(
        from_email=email_message.from_email,
        subject=email_message.subject,
        body=email_message.body,
        recipients=(', ').join(email_message.recipients()),
        cc=(', ').join(email_message.cc),
        bcc=(', ').join(email_message.bcc),
        category=category,
        is_sent=is_sent,
    ).save()
    return tracked_email


class EmailTrackerBackend(EmailBackend):

    def send_messages(self, email_messages):
        """
        Sends one or more EmailMessage objects and returns the number of email
        messages sent.
        Creates EmailMessage and EmailCategory (if needed) for every message with defined extra header

        """
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
                create_tracked_email(message, bool(sent))
            if new_conn_created:
                self.close()
        return num_sent
