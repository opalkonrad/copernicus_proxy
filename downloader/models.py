from django.db import models
from django.utils import timezone
import jsonfield

STATUS_MAX_LENGTH = 16
MSG_MAX_LENGTH = 512
DATA_SET_MAX_LENGTH = 128
ATTRIBUTES_MAX_LENGTH = 256


class Request(models.Model):
    request_date = models.DateTimeField(default=timezone.now)
    json_content = jsonfield.JSONField()
    status = models.CharField(max_length=STATUS_MAX_LENGTH, default="pending")
    msg = models.CharField(max_length=MSG_MAX_LENGTH)


class DataSets(models.Model):
    data_set = models.CharField(max_length=DATA_SET_MAX_LENGTH)
    attributes = models.CharField(max_length=ATTRIBUTES_MAX_LENGTH)
