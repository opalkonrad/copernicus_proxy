from django.core.management.base import BaseCommand, CommandError
from service.models import Task as TaskModel
from service.tasks import download_from_cdsapi
import os

WORKERS_LIMIT = 30


def reset_workers(n):
    os.system("celery -f -A copernicus_proxy purge")
    os.system("pkill -f copernicus_proxy_worker")
    os.system(
        "celery -A copernicus_proxy worker --loglevel=INFO "
        "--concurrency=" + str(n) + " -n copernicus_proxy_worker &"
    )


def reload_task_queue():
    TaskModel.mark_being_downloaded_as_pending()
    pending_list = sorted(TaskModel.get_all_pending())
    for pk in pending_list:
        download_from_cdsapi.delay(pk)


class Command(BaseCommand):
    help = 'Restarts celery task queue with the number of workers specified in command'

    def add_arguments(self, parser):
        parser.add_argument(
            'number_of_workers',
            type=int,
            help='Required. Indicates the number of workers to be created'
        )

    def handle(self, *args, **kwargs):
        n = kwargs['number_of_workers']
        if n < 1:
            raise CommandError('Number of workers must be bigger than 0')
        elif n > 100:
            raise CommandError('Maximum number of workers is ' + str(WORKERS_LIMIT))

        reset_workers(n)
        reload_task_queue()
