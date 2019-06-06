from django.apps import AppConfig
import os


class ServiceConfig(AppConfig):
    name = 'service'


DOWNLOADER_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(DOWNLOADER_DIR, 'templates')
