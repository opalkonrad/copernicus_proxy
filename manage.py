#!/usr/bin/env python
import os
import sys
import subprocess


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sea_level.settings')
    # print("DEBUGGER 1")
    # os.system("celery -A sea_level control shutdown &")
    # print("DEBUGGER 2")
    # os.system("celery -A sea_level worker --loglevel=INFO --concurrency=2 -n seaworker &")
    # print("DEBUGGER 3")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
