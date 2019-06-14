from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.core import validators
from service.validators import validate_data_set, validate_task_json_content, validate_json
from service.constants import formats
from copernicus_proxy.settings import BASE_DIR
import json
import os

DATA_SET_MAX_LENGTH = 128
JSON_CONTENT_MAX_LENGTH = 16384
STATUS_MAX_LENGTH = 16
MSG_MAX_LENGTH = 512

ATTRIBUTES_MAX_LENGTH = 256
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


class Task(models.Model):
    data_set = models.ForeignKey(
        'DataSet',
        on_delete=models.PROTECT,
        validators=[validate_data_set],
        null=True
    )
    json_content = models.CharField(
        max_length=JSON_CONTENT_MAX_LENGTH,
        validators=[validate_task_json_content, validators.MaxLengthValidator(JSON_CONTENT_MAX_LENGTH)]
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
        default=None,
        null=True,
        blank=True
    )
    bytes = models.IntegerField(
        default=None,
        blank=True,
        null=True
    )

    def to_dict(self):
        task_date = self.task_date.replace(tzinfo=None).strftime(DATETIME_FORMAT)
        data_set_name = None
        if self.data_set:
            data_set_name = self.data_set.name
        task_dict = {
            'id': self.pk,
            'data_set': data_set_name,
            'json_content': json.loads(self.json_content),
            'status': self.status,
            'task_date': task_date,
            'msg': self.msg,
            'bytes': self.bytes
        }
        return task_dict

    @classmethod
    def create_from_json(cls, json_content):
        validate_task_json_content(json_content)
        init_data = json.loads(json_content)

        data_set_name = init_data['data_set']
        DataSet.initialize_data_sets()
        data_set = DataSet.get_by_name(data_set_name)

        task = cls(json_content=json_content)
        task.data_set = data_set
        task.full_clean()
        task.save()
        return task

    @classmethod
    def delete_first_if_count_bigger_than(cls, maximum_count):
        task_count = cls.objects.count()
        if task_count >= maximum_count:
            task_to_remove = cls.objects.all().order_by("id")[0]
            task_id = task_to_remove.id
            json_content = json.loads(task_to_remove.json_content)
            data_set = json_content['data_set']
            file_format = json_content['options']['format']
            for f in formats.list:
                if f.extension[1] == file_format:
                    file_format = f.extension[0]

            file_location = os.path.join(BASE_DIR, 'files', data_set, 'file_id_' + str(task_id) + file_format)
            if os.path.exists(file_location):
                os.remove(file_location)
            task_to_remove.delete()

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
    name = models.CharField(
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
            name='satellite-sea-level-mediterranean',
            attributes='{"variable": "all", '
                       '"format": "one", '
                       '"day": "at_least_one", '
                       '"year": "at_least_one", '
                       '"month": "at_least_one"}'
        )
        default0.save()
        default1 = cls(
            name='reanalysis-era5-single-levels',
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
            data_set = cls.objects.get(name=data_set_name)
            return data_set
        except ObjectDoesNotExist:
            return None

    def to_dict(self):
        data_set_dict = {
            'id': self.pk,
            'data_set': self.name,
            'attributes': json.loads(self.attributes)
        }
        return data_set_dict

    @classmethod
    def list_all(cls):
        data_set_list = []
        for record in cls.objects.all():
            data_set_list.append(record.to_dict())
        return data_set_list
