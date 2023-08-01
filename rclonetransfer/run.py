import subprocess
import tempfile
from django.utils import timezone
from .models import UserProfile, TransferJob
from .utils import refresh_google_token, refresh_dropbox_token
import json
import os

class RCloneRunner:
    def __init__(self, user):
        self.user = user
        self.user_profile = UserProfile.objects.get(user=user)

    def create_rclone_config(self):

        if self.user_profile.google_token.get('expiry') is not None and not self.user_profile.google_token[
            'expiry'].endswith('Z'):
            self.user_profile.google_token['expiry'] += 'Z'

        if self.user_profile.dropbox_token.get('expiry') is not None and not self.user_profile.dropbox_token[
            'expiry'].endswith('Z'):
            self.user_profile.dropbox_token['expiry'] += 'Z'

        config = "[gdrive]\n"
        config += f"type = drive\n"
        config += f"token = {json.dumps(self.user_profile.google_token)}\n"
        config += "[dropbox]\n"
        config += f"type = dropbox\n"
        config += f"token = {json.dumps(self.user_profile.dropbox_token)}\n"

        return config

    def refresh_tokens(self):
        refresh_google_token(self.user_profile)
        refresh_dropbox_token(self.user_profile)
        self.user_profile.refresh_from_db()

    def run_rclone_copy(self, source, destination):
        self.refresh_tokens()
        rclone_config = self.create_rclone_config()

        fd, path = tempfile.mkstemp()
        try:
            with os.fdopen(fd, 'w') as tmp:
                tmp.write(rclone_config)
            process = subprocess.Popen(["rclone", "-v", "-P", "--config", path, "copy", source, destination],
                                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            for line in iter(process.stdout.readline, b''):
                print(line.decode().strip())

            process.stdout.close()
            process.wait()
        finally:
            os.remove(path)

    def start_rclone_job(self, source, destination):
        transfer_job = TransferJob.objects.create(
            user=self.user,
            source=source,
            destination=destination,
            status="running",
            time_started=timezone.now()
        )

        try:
            self.run_rclone_copy(source, destination)
            transfer_job.status = "completed"
        except Exception as e:
            transfer_job.status = "failed"
            transfer_job.error_message = str(e)

        transfer_job.time_finished = timezone.now()
        transfer_job.save()