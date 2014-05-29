from django.contrib import admin

from email_tracker.models import EmailCategory, TrackedEmail


class TrackedEmailAdmin(admin.ModelAdmin):
    list_filter = ('category', )
    readonly_fields = ['subject', 'from_email', 'recipients', 'cc', 'bcc', 'body', 'is_sent', 'category', 'created_at']
 

admin.site.register(TrackedEmail, TrackedEmailAdmin)
admin.site.register(EmailCategory)