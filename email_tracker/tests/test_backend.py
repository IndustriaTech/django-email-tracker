from __future__ import absolute_import

from django.core import mail
from django.test import TestCase
from django.test.utils import override_settings

from email_tracker.models import TrackedEmail
from .settings import EMAIL_BACKEND


# We need to overwrite EMAIL_BACKED because Django was overwritten it
@override_settings(EMAIL_BACKEND=EMAIL_BACKEND)
class EmailBackendTestCase(TestCase):

    def test_send_new_mail(self):
        mail.send_mail(
            subject='Subject',
            message='Message',
            from_email='from@example.com',
            recipient_list=['to@example.com', 'to2@example.com'],
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(TrackedEmail.objects.count(), 1)
        tracked_email = TrackedEmail.objects.get()
        self.assertEqual(tracked_email.subject, 'Subject')
        self.assertEqual(tracked_email.from_email, 'from@example.com')
        self.assertEqual(tracked_email.recipients, 'to@example.com, to2@example.com')
        self.assertEqual(tracked_email.is_sent, True)
