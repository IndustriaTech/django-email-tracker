from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
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
        # Try to get category from extra headers
        category = message.extra_headers.get('X-Category')
        if category:
            instance, created = self.get_or_create(title=category)
        else:
            # If there is existing category which is same as the subject
            # then use that, but does not create new category for every subject
            try:
                instance = self.get(title=message.subject)
            except self.model.DoesNotExist:
                return
        return instance


class TrackedEmailManager(models.Manager):
    def create_from_message(self, message, is_sent=False):
        """
        Create TrackedEmail for given EmailMessage object
        """
        try:
            message_id = [val for key, val in message.extra_headers.items() if key.lower() == 'message-id'][0]
        except IndexError:
            message_id = None
        instance = self.create(
            from_email=message.from_email,
            subject=message.subject,
            body=message.body,
            recipients=', '.join(message.recipients()),
            cc=', '.join(message.cc),
            bcc=', '.join(message.bcc),
            category=EmailCategory.objects.get_for_message(message),
            is_sent=is_sent,
            esp_message_id=message_id,
        )
        for content, mimetype in getattr(message, 'alternatives', ()):
            if 'text' in mimetype:
                instance.alternatives.create(
                    mimetype=mimetype,
                    content=content,
                )
        return instance


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
    esp_message_id = models.CharField(max_length=254, unique=True, blank=True, null=True, editable=False, verbose_name=_('ESP message ID'))

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
    get_body.short_description = _('Body')


@python_2_unicode_compatible
class TrackedEmailAlternative(models.Model):
    email = models.ForeignKey(TrackedEmail, related_name='alternatives', on_delete=models.CASCADE)
    mimetype = models.CharField(max_length=250)
    content = models.TextField()

    class Meta:
        verbose_name = _('Alternative')
        verbose_name_plural = _('Alternatives')

    def __str__(self):
        return self.mimetype


@python_2_unicode_compatible
class TrackedEmailEvent(models.Model):
    email = models.ForeignKey(TrackedEmail, related_name='events', on_delete=models.PROTECT)
    event = models.CharField(max_length=254, verbose_name=_('Event'), editable=False)
    created_at = models.DateTimeField(verbose_name=_('Created at'), editable=False, default=timezone.now)
    data = models.TextField(verbose_name=_('Raw data for the event'), editable=False)

    class Meta:
        ordering = '-created_at',
        verbose_name = _('Event')
        verbose_name_plural = _('Events')

    def __str__(self):
        return u'{self.event} at {self.created_at}'.format(self=self)

    def is_mail_sent(self):
        """
        Method that will determine based of the event is it for send or rejected email.
        It is used by post_save handler in order to change the status of email.
        If the result is None then post_save handler will not change the status of the mail
        """
        if self.event in ('sent', 'delivered'):
            return True
        elif self.event in ('rejected', 'failed', 'bounced'):
            return False


@receiver(post_save, sender=TrackedEmailEvent)
def _on_post_save_event_handler(sender, instance, created=False, raw=False, **kwargs):
    if raw or not created:
        return

    is_sent = instance.is_mail_sent()

    if is_sent is None:
        # If is_sent is None we will not change anything
        return

    TrackedEmail.objects.filter(
        pk=instance.email_id,
        is_sent=not is_sent,
    ).update(is_sent=is_sent)


if settings.EMAIL_TRACKER_USE_ANYMAIL:
    from anymail.signals import pre_send, post_send, tracking

    @receiver(pre_send)
    def _on_pre_send_handler(sender, message, esp_name, **kwargs):
        message._tracked_email = TrackedEmail.objects.create_from_message(message)

    @receiver(post_send)
    def _on_post_send_handler(sender, message, status, esp_name, **kwargs):
        try:
            tracked_email = message._tracked_email
        except AttributeError:
            # If for some reason pre_send signal was not send for this
            # message then _tracked_email will be unset
            return

        tracked_email.esp_message_id = status.message_id

        if status.status.union(('sent', 'queued')):
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
        except TrackedEmail.DoesNotExist:
            return

        tracked_email.events.create(
            event=event.event_type,
            created_at=event.timestamp,
            data=event.esp_event,
        )
