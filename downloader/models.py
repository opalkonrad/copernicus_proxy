from django.db import models
from django.utils import timezone
import jsonfield



class Request(models.Model):
    request_date = models.DateTimeField(default=timezone.now)
    json_content = jsonfield.JSONField()
    status = models.CharField(max_length=15, default="pending")
    msg = models.CharField(max_length=500)

    def set_downloaded(self):
        self.status = "downloaded"
