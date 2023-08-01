from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rclonetransfer.run import RCloneRunner
import os

class Command(BaseCommand):
    help = 'Starts an RClone job for a given user, source, and destination.'

    def handle(self, *args, **kwargs):
        username = os.environ.get('username')
        source = os.environ.get('source')
        destination = os.environ.get('destination')

        user = User.objects.get(username=username)
        rclone_runner = RCloneRunner(user)
        rclone_runner.start_rclone_job(source, destination)