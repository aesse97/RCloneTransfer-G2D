from django.contrib import admin
from .models import TransferJob, UserProfile

class TransferJobAdmin(admin.ModelAdmin):
    list_display = ('user', 'source', 'destination', 'status', 'time_started', 'time_finished')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'google_token', 'dropbox_token')

admin.site.register(TransferJob, TransferJobAdmin)
admin.site.register(UserProfile, UserProfileAdmin)