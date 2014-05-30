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
    subject = models.CharField(max_length=512, verbose_name=_('Subject'))
    from_email = models.CharField(max_length=255, verbose_name=_('From email'))
    recipients = models.TextField(verbose_name=_('Recipients'))
    cc = models.TextField(verbose_name=_('Cc'))
    bcc = models.TextField(verbose_name=_('Bcc'))
    body = models.TextField(verbose_name=_('Body'))
    is_sent = models.BooleanField(verbose_name=_('Is sent'))
    category = models.ForeignKey(EmailCategory, null=True, blank=True, verbose_name=_('Category'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))

    def __unicode__(self):
        return 'Mail to {}'.format(self.recipients)

    class Meta:
        ordering = '-created_at',
        verbose_name = _('Tracked Email')
        verbose_name_plural = _('Tracked Emails')
