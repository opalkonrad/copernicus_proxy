from django.db import models
from django.utils import timezone
import jsonfield

class Task(models.Model):
    task_date = models.DateTimeField(default=timezone.now)
    json_content = jsonfield.JSONField()
    status = models.TextField(default="pending")
    data_set = models.TextField(max_length=255, default="???")

    def set_downloaded(self):
        self.status = "downloaded"

# class DownloadedFile(models.Model):
#     date = models.DateTimeField(default=timezone.now)
#     path = models.CharField(max_length=255)
#     size = models.CharField(max_length=31)
#     fk = models.ForeignKey(Task, on_delete=models.CASCADE)

#     def set_path(self, category):
#         self.path = "./files/" + category + "/file_id_" + self.fk