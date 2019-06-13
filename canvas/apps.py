from django.apps import AppConfig
import os


class DownloaderConfig(AppConfig):
    name = 'canvas'


DOWNLOADER_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(DOWNLOADER_DIR, 'templates')
