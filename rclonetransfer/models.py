from django.db import models
from django.contrib.auth.models import User

class TransferJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    status = models.CharField(max_length=20)
    time_started = models.DateTimeField()
    time_finished = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    _google_token = models.JSONField(blank=True, null=True, db_column='google_token')
    _dropbox_token = models.JSONField(blank=True, null=True, db_column='dropbox_token')

    @property
    def google_token(self):
        return self._google_token

    @google_token.setter
    def google_token(self, value):
        self._google_token = value

    @property
    def dropbox_token(self):
        return self._dropbox_token

    @dropbox_token.setter
    def dropbox_token(self, value):
        self._dropbox_token = value