import datetime
from django.db import models


class EmailCategory(models.Model):
    title = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return self.title


class TrackedEmail(models.Model):
    subject = models.CharField(max_length=512)
    from_email = models.CharField(max_length=255)
    recipients = models.TextField()
    cc = models.TextField()
    bcc = models.TextField()
    body = models.TextField()
    is_sent = models.BooleanField()
    category = models.ForeignKey(EmailCategory, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return 'Mail to {}'.format(self.recipients)

    class Meta:
        ordering = '-created_at',
