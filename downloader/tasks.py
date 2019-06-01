from __future__ import absolute_import, unicode_literals
from downloader.constants import formats
from celery import shared_task
from django.db import models
from django.http import HttpResponse
from downloader.forms.sea_level_form import SeaLevelForm
from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.utils import timezone
from downloader.models import DataSets, Task
import downloader.forms.sea_level_choices as options
import cdsapi
import json
import datetime
import os
from django.core.exceptions import ObjectDoesNotExist, ValidationError


@shared_task
def download_from_cdsapi(form_content, pk):
    # get information about task
    data = json.loads(form_content)
    curr_task = Task.objects.get(id=pk)
    data_set = curr_task.data_set

    # update task's status in database
    curr_task.status = "being downloaded"
    curr_task.msg = ""
    curr_task.save()

    # check required attributes
    try:
        attr_check = DataSets.objects.get(data_set=data_set)

    except ObjectDoesNotExist:
        curr_task.status = 'error'
        curr_task.msg = 'no matching data set'
        curr_task.save()
        return

    result = json.loads(attr_check.attributes)

    db_cntr = 0
    internal_cntr = 0

    try:
        for attrs_db in result:
            db_cntr += 1

            # look for attributes
            for key in data:
                if attrs_db == key:
                    internal_cntr += 1

            # lack of attribute in form needed for Copernicus
            if db_cntr != internal_cntr:
                raise ValidationError('lack of argument in form - ' + attrs_db)

    except ValidationError as e:
        # update request's status in database to error
        curr_task.status = 'error'
        curr_task.msg = e
        curr_task.save()
        return

    save_format = data['format']

    # find the right notation for the given format (needed for api -> format)
    for f in formats.list:
        if f.extension[0] == data['format']:
            data['format'] = f.extension[1]

    # create file directory
    os.makedirs("./files/" + data_set, exist_ok=True)

    # API REQUEST
    c = cdsapi.Client()

    try:
        c.retrieve(
            data_set,
            data,
            "./files/" + data_set + "/file_id_" + pk + save_format
        )

    except Exception as e:
        # update request's status in database to error
        curr_task.status = 'error'
        curr_task.msg = e
        curr_task.save()
        return

    # update request's status in database to downloaded
    curr_task.status = 'downloaded'
    curr_task.msg = 'success'
    curr_task.save()
