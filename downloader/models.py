from django.db import models
from django.utils import timezone
import jsonfield

class Request(models.Model):
    request_date = models.DateTimeField(default=timezone.now)
    json_content = jsonfield.JSONField()