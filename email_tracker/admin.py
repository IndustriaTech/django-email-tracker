from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from email_tracker.models import EmailCategory, TrackedEmail, TrackedEmailEvent


class TrackedEmailEventInline(admin.TabularInline):
    model = TrackedEmailEvent
    readonly_fields = 'event', 'created_at',
    max_num = extra = 0
    can_delete = False


class TrackedEmailAdmin(admin.ModelAdmin):
    readonly_fields = (
        'esp_message_id',
        'subject', 'from_email', 'recipients', 'cc', 'bcc',
        'get_body', 'is_sent', 'category', 'created_at', 'content_type'
    )
    fieldsets = (
        (None, {
            'fields': (
                'esp_message_id',
                'subject',
                'from_email',
                'recipients',
                ('cc', 'bcc'),
            )
        }),
        (_('Body'), {
            'classes': ('collapse', ),
            'fields': ('content_type', 'get_body')
        }),
        (None, {
            'fields': ('category', 'created_at', 'is_sent'),
        }),

    )
    inlines = (TrackedEmailEventInline, )

    list_filter = ('is_sent', 'created_at', 'category')
    list_display = ('created_at', 'subject', 'recipients', 'is_sent')
    date_hierarchy = 'created_at'
    search_fields = ('subject', 'recipients')
    actions = None

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False

admin.site.register(TrackedEmail, TrackedEmailAdmin)
admin.site.register(EmailCategory)
