from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.core import validators
from service.validators import validate_json_content, validate_json
import json

DATA_SET_MAX_LENGTH = 128
JSON_CONTENT_MAX_LENGTH = 16384
STATUS_MAX_LENGTH = 16
MSG_MAX_LENGTH = 512

ATTRIBUTES_MAX_LENGTH = 256
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


class Task(models.Model):
    # data_set = models.ForeignKey(
    #     'DataSet',
    #     on_delete=models.PROTECT,
    # )
    json_content = models.CharField(
        max_length=JSON_CONTENT_MAX_LENGTH,
        validators=[validate_json_content, validators.MaxLengthValidator(JSON_CONTENT_MAX_LENGTH)]
    )
    status = models.CharField(
        max_length=STATUS_MAX_LENGTH,
        validators=[validators.MaxLengthValidator(STATUS_MAX_LENGTH)],
        default="pending"
    )
    task_date = models.DateTimeField(default=timezone.now)
    msg = models.CharField(
        max_length=MSG_MAX_LENGTH,
        validators=[validators.MaxLengthValidator(MSG_MAX_LENGTH)],
        default="",
        blank=True
    )
    bytes = models.IntegerField(
        default=None,
        blank=True,
        null=True
    )

    def to_dict(self):
        task_date = self.task_date.replace(tzinfo=None).strftime(DATETIME_FORMAT)
        json_content = json.loads(self.json_content)
        task_dict = {
            'id': self.pk,
            'data_set': json_content[0],
            'json_content': json_content,
            'status': self.status,
            'task_date': task_date,
            'msg': self.msg,
            'bytes': self.bytes
        }
        return task_dict

    @classmethod
    def list_all(cls):
        tasks_list = []
        for task in cls.objects.all():
            tasks_list.append(task.to_dict())
        return tasks_list

    @classmethod
    def mark_being_downloaded_as_pending(cls):
        for task in cls.objects.filter(status="being downloaded"):
            task.status = "pending"
            task.save()

    @classmethod
    def get_all_pending(cls):
        pending_list = []
        for task in cls.objects.filter(status="pending"):
            pending_list.append(task.pk)
        return pending_list


class DataSet(models.Model):
    data_set = models.CharField(
        max_length=DATA_SET_MAX_LENGTH,
        validators=[validators.MaxLengthValidator(DATA_SET_MAX_LENGTH)],
        unique=True
    )
    attributes = models.CharField(
        max_length=ATTRIBUTES_MAX_LENGTH,
        validators=[validate_json, validators.MaxLengthValidator(ATTRIBUTES_MAX_LENGTH)],
    )

    @classmethod
    def add_default_data_sets(cls):
        default0 = cls(
            data_set='satellite-sea-level-mediterranean',
            attributes='{"variable": "all", '
                       '"format": "one", '
                       '"day": "at_least_one", '
                       '"year": "at_least_one", '
                       '"month": "at_least_one"}'
        )
        default0.save()
        default1 = cls(
            data_set='reanalysis-era5-single-levels',
            attributes='{"product_type": "at_least_one", '
                       '"format": "one", '
                       '"variable": "at_least_one", '
                       '"day": "at_least_one", '
                       '"year": "at_least_one", '
                       '"month": "at_least_one", '
                       '"time": "at_least_one"}'
        )
        default1.save()

    @classmethod
    def initialize_data_sets(cls):
        if not cls.objects.exists():
            cls.add_default_data_sets()

    @classmethod
    def get_by_name(cls, data_set_name):
        try:
            data_set = cls.objects.get(data_set=data_set_name)
            return data_set
        except ObjectDoesNotExist:
            return None

    def to_dict(self):
        data_set_dict = {
            'id': self.pk,
            'data_set': self.data_set,
            'attributes': json.loads(self.attributes)
        }
        return data_set_dict

    @classmethod
    def list_all(cls):
        data_set_list = []
        for record in cls.objects.all():
            data_set_list.append(record.to_dict())
        return data_set_list
