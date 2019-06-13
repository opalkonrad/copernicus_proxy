from django.core.management.base import BaseCommand, CommandError
import os

WORKERS_LIMIT = 30


class Command(BaseCommand):
    help = 'Restarts celery task queue with the number of workers specified in command'

    def add_arguments(self, parser):
        parser.add_argument('workers_number', type=int, help='Required. Indicates the number of workers to be created')

    def handle(self, *args, **kwargs):
        n = kwargs['workers_number']
        if n < 1:
            raise CommandError('Number of workers must be bigger than 0')
        elif n > 100:
            raise CommandError('Number of workers must be lower than ' + str(WORKERS_LIMIT))

        os.system("pkill -f copernicus_proxy_worker")
        os.system(
            "celery -A copernicus_proxy worker --loglevel=INFO "
            "--concurrency=" + str(n) + " -n copernicus_proxy_worker &"
        )
