from __future__ import absolute_import

from django.test import TestCase
from django.contrib.auth.models import User
from email_tracker.models import TrackedEmail, EmailCategory
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse


class EmailTrackerAdminTestCase(TestCase):
    def setUp(self):
        super(EmailTrackerAdminTestCase, self).setUp()
        self.admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        category = EmailCategory.objects.create(title='Test Category')
        self.tracked_email = TrackedEmail.objects.create(
            category=category,
            subject='Test Email',
            body='Test email content',
            recipients='to@example.com',
        )

    def test_admin_can_list_emails(self):
        self.client.login(username='admin', password='admin')
        url = reverse('admin:email_tracker_trackedemail_changelist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_admin_can_see_details(self):
        self.client.login(username='admin', password='admin')
        url = reverse('admin:email_tracker_trackedemail_change', args=(self.tracked_email.pk, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
