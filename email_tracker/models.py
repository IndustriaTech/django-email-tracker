from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.html import linebreaks
from django.utils.safestring import mark_safe
from email_tracker.compat import python_2_unicode_compatible
from email_tracker.conf import settings


# Managers

class EmailCategoryManager(models.Manager):
    def get_for_message(self, message):
        """
        Get or create category for given EmailMessage object
        """
        title = message.extra_headers.get('X-Category')
        if not title:
            return
        instance, created = self.get_or_create(title=title)
        return instance


class TrackedEmailManager(models.Manager):
    def create_from_message(self, message, is_sent=False):
        """
        Create TrackedEmail for given EmailMessage object
        """
        return self.create(
            from_email=message.from_email,
            subject=message.subject,
            body=message.body,
            recipients=(', ').join(message.recipients()),
            cc=(', ').join(message.cc),
            bcc=(', ').join(message.bcc),
            category=EmailCategory.objects.get_for_message(message),
            is_sent=is_sent,
        )


# Models

@python_2_unicode_compatible
class EmailCategory(models.Model):
    title = models.CharField(max_length=200, unique=True)

    objects = EmailCategoryManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Email Category')
        verbose_name_plural = _('Email Categories')


@python_2_unicode_compatible
class TrackedEmail(models.Model):
    subject = models.CharField(max_length=512, verbose_name=_('Subject'))
    from_email = models.CharField(max_length=255, verbose_name=_('From email'))
    recipients = models.TextField(verbose_name=_('Recipients'))
    cc = models.TextField(verbose_name=_('Cc'))
    bcc = models.TextField(verbose_name=_('Bcc'))
    body = models.TextField(verbose_name=_('Body'), editable=False)
    content_type = models.CharField(max_length=64, default='plain')
    is_sent = models.BooleanField(verbose_name=_('Is sent'), default=False)
    category = models.ForeignKey(EmailCategory, null=True, blank=True, verbose_name=_('Category'), on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    esp_message_id = models.CharField(max_length=254, unique=True, blank=True, null=True)

    objects = TrackedEmailManager()

    def __str__(self):
        return u'Mail to {}'.format(self.recipients)

    class Meta:
        ordering = '-created_at',
        verbose_name = _('Tracked Email')
        verbose_name_plural = _('Tracked Emails')

    def get_body(self):
        if self.content_type == 'plain':
            return mark_safe(linebreaks(self.body, autoescape=True))
        return self.body


@python_2_unicode_compatible
class TrackedEmailEvent(models.Model):
    email = models.ForeignKey(TrackedEmail, related_name='events', on_delete=models.PROTECT)
    event = models.CharField(max_length=254, verbose_name=_('Event'), editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    data = models.TextField(verbose_name=_('Raw data for the event'), editable=False)

    class Meta:
        ordering = '-created_at',
        verbose_name = _('Event')
        verbose_name_plural = _('Events')

    def __str__(self):
        return u'{self.event} at {self.created_at}'.format(self=self)


if settings.EMAIL_TRACKER_USE_ANYMAIL:
    from django.dispatch import receiver
    from anymail.signals import pre_send, post_send, tracking

    @receiver(pre_send)
    def _on_pre_send_handler(sender, message, esp_name, **kwargs):
        message._tracked_email = TrackedEmail.objects.create_from_message(message)

    @receiver(post_send)
    def _on_post_send_handler(sedner, message, status, esp_name, **kwargs):
        try:
            tracked_email = message._tracked_email
        except AttributeError:
            # If for some reason pre_send signal was not send for this
            # message then _tracked_email will be unset
            return

        tracked_email.esp_message_id = status.message_id

        if status.status == 'sent':
            tracked_email.is_sent = True

        type(tracked_email).objects.filter(
            pk=tracked_email.pk
        ).update(
            esp_message_id=tracked_email.esp_message_id,
            is_sent=tracked_email.is_sent,
        )

    @receiver(tracking)
    def _on_tracking_handler(sender, event, esp_name, **kwargs):
        try:
            tracked_email = TrackedEmail.objects.get(esp_message_id=event.message_id)
        except TrackedEmail.DoesNotExists:
            return

        tracked_email.events.create(
            event=event.event_type,
            created_at=event.timestamp,
            data=event.esp_event,
        )
