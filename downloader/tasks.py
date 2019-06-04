from __future__ import absolute_import, unicode_literals

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
from downloader.constants import formats


@shared_task
def download_from_cdsapi(form_content, pk):
    # get information about task
    data = json.loads(form_content)
    curr_task = Task.objects.get(id=pk)
    data_set = curr_task.data_set
    save_format = ""

    # update task's status in database
    curr_task.status = "being downloaded"
    curr_task.msg = ""
    curr_task.save()

    # find the right notation for the given format (needed for api -> format)
    for f in formats.list:
        if f.extension[1] == data['format']:
            save_format = f.extension[0]

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
        curr_task.status = "error"
        curr_task.msg = e
        curr_task.save()
        return

    # update request's status in database to downloaded
    curr_task.status = "downloaded"
    curr_task.msg = "success"
    curr_task.save()
