from django.db import models
from django.utils.translation import ugettext_lazy as _


class EmailCategory(models.Model):
    title = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('Email Category')
        verbose_name_plural = _('Email Categories')


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
        verbose_name = _('Tracked Email')
        verbose_name_plural = _('Tracked Emails')
