from django.contrib import admin

from email_tracker.models import EmailCategory, TrackedEmail, TrackedEmailEvent


class TrackedEmailEventInline(admin.TabularInline):
    model = TrackedEmailEvent
    readonly_fields = 'event', 'created_at',
    max_num = extra = 0
    can_delete = False


class TrackedEmailAdmin(admin.ModelAdmin):
    list_filter = ('created_at', 'category')
    list_display = ('__str__', 'created_at')
    readonly_fields = (
        'esp_message_id',
        'subject', 'from_email', 'recipients', 'cc', 'bcc',
        'get_body', 'is_sent', 'category', 'created_at', 'content_type'
    )
    inlines = (TrackedEmailEventInline, )
    date_hierarchy = 'created_at'
    search_fields = ('subject', 'recipients')

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False

admin.site.register(TrackedEmail, TrackedEmailAdmin)
admin.site.register(EmailCategory)
