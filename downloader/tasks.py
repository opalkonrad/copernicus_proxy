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


@shared_task
def download_from_cdsapi(form_content, pk):
    data = json.loads(form_content)
    the_task = Task.objects.get(id=pk)
    data_set = the_task.data_set

    result = {
        "years": [],
        "months": [],
        "days": [],
        "format": ""
    }

    tmp_format_api = ""  # Api format e.g. "tgz"
    tmp_format_ext = ""  # File extension e.g. ".tar.gz"
    tmp_years = ""
    tmp_months = ""
    tmp_days = ""

    # Filling the dictionary with a completed form
    for key, values in data.items():
        for value in values:
            if key == 'format':
                tmp_format_ext += value
                continue

            result[key].append(value)

            if key == 'years':
                tmp_years += "%d" % int(value)
                tmp_years += ","

            if key == 'months':
                tmp_months += "{:02d}".format(int(value))
                tmp_months += ","

            if key == 'days':
                tmp_days += "{:02d}".format(int(value))
                tmp_days += ","

    result['format'] = tmp_format_ext

    # Find the right notation for the given format (needed for api -> format)
    for f in formats.list:
        if f.extension[0] == result['format']:
            tmp_format_api = f.extension[1]

    # Delete the comma at the end of string
    tmp_years = tmp_years[:-1]
    tmp_months = tmp_months[:-1]
    tmp_days = tmp_days[:-1]

    # Create file directory
    data_set = 'satellite-sea-level-mediterranean'
    os.makedirs("./files/" + data_set, exist_ok=True)

    # API REQUEST
    c = cdsapi.Client()

    try:
        c.retrieve(
            data_set,
            {
                'variable': 'all',
                'format': tmp_format_api,
                'year': tmp_years.split(','),
                'month': tmp_months.split(','),
                'day': tmp_days.split(',')
            },
            "./files/" + data_set + "/file_id_" + pk + result['format'])
    except Exception as e:
        # update request's status in database to error
        to_update = Task.objects.get(id=pk)
        to_update.status = 'error'
        to_update.msg = e
        to_update.save()
        return

    # update request's status in database to downloaded
    to_update = Task.objects.get(id=pk)
    to_update.status = 'downloaded'
    to_update.msg = 'success'
    to_update.save()
