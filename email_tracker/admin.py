from django.contrib import admin

from email_tracker.models import EmailCategory, TrackedEmail


class TrackedEmailAdmin(admin.ModelAdmin):
    list_filter = ('created_at', 'category')
    list_display = ('__unicode__', 'created_at')
    readonly_fields = ['subject', 'from_email', 'recipients', 'cc', 'bcc', 'get_body', 'is_sent', 'category', 'created_at', 'content_type']
    date_hierarchy = 'created_at'

admin.site.register(TrackedEmail, TrackedEmailAdmin)
admin.site.register(EmailCategory)
