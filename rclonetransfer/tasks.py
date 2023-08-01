from celery import shared_task
from .run import RCloneRunner
from django.contrib.auth import get_user_model

@shared_task
def run_rclone_copy_task(user_id, source, destination):
    User = get_user_model()
    user = User.objects.get(pk=user_id)
    runner = RCloneRunner(user)
    runner.run_rclone_copy(source, destination)