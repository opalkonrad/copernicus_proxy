from django.db import models
from django.utils import timezone

CONTENT_MAX_LENGTH = 512
STATUS_MAX_LENGTH = 16
MSG_MAX_LENGTH = 512
DATA_SET_NAME_MAX_LENGTH = 128
ATTRIBUTES_MAX_LENGTH = 256


class Task(models.Model):
    task_date = models.DateTimeField(default=timezone.now)
    content = models.CharField(max_length=CONTENT_MAX_LENGTH)
    status = models.CharField(max_length=STATUS_MAX_LENGTH, default="pending")
    data_set = models.TextField(max_length=DATA_SET_NAME_MAX_LENGTH, default="???")
    msg = models.CharField(max_length=MSG_MAX_LENGTH)


# DataSets Foreign Key TBA
# DownloadedFile Foreign Key TBA

class DataSets(models.Model):
    data_set_name = models.CharField(max_length=DATA_SET_NAME_MAX_LENGTH)
    attributes = models.CharField(max_length=ATTRIBUTES_MAX_LENGTH)

# DownloadedFile TBA
