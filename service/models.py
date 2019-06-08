from django.db import models
from django.utils import timezone
import jsonfield
import json

STATUS_MAX_LENGTH = 16
MSG_MAX_LENGTH = 512
DATA_SET_MAX_LENGTH = 128
ATTRIBUTES_MAX_LENGTH = 256
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


class Task(models.Model):
    task_date = models.DateTimeField(default=timezone.now)
    json_content = jsonfield.JSONField()
    status = models.CharField(max_length=STATUS_MAX_LENGTH, default="pending")
    data_set = models.TextField(max_length=DATA_SET_MAX_LENGTH, default="???")
    msg = models.CharField(max_length=MSG_MAX_LENGTH)

    def to_dict(self):
        task_date = self.task_date.replace(tzinfo=None).strftime(DATETIME_FORMAT)
        task_dict = {
            'id': self.pk,
            'json_content': json.loads(self.json_content),
            'status': self.status,
            'data_set': self.data_set,
            'task_date': task_date,
            'msg': self.msg
        }
        return task_dict

    @classmethod
    def list_all(cls):
        tasks_list = []
        for task in cls.objects.all():
            tasks_list.append(task.to_dict())
        return tasks_list


class DataSets(models.Model):
    data_set = models.CharField(max_length=DATA_SET_MAX_LENGTH, unique=True)
    attributes = models.CharField(max_length=ATTRIBUTES_MAX_LENGTH)

# DataSets Foreign Key TBA
# DownloadedFile Foreign Key TBA
# DownloadedFile TBA


# class DownloadedFile(models.Model):
#     date = models.DateTimeField(default=timezone.now)
#     path = models.CharField(max_length=255)
#     size = models.CharField(max_length=31)
#     fk = models.ForeignKey(Task, on_delete=models.CASCADE)

#     def set_path(self, category):
#         self.path = "./files/" + category + "/file_id_" + self.fk
