from __future__ import absolute_import, unicode_literals
from celery import shared_task
from service.models import Task
from service.constants import formats
import cdsapi
import json
import os


@shared_task
def download_from_cdsapi(pk):
    # get information about task
    curr_task = Task.objects.get(id=pk)
    content = json.loads(curr_task.json_content)
    data_set = content['data_set']
    options = content['options']
    save_format = ""

    # update task's status in database
    curr_task.status = "being downloaded"
    curr_task.msg = ""
    curr_task.save()

    # find the right notation for the given format (needed for api -> format)
    for f in formats.list:
        if f.extension[1] == options['format']:
            save_format = f.extension[0]

    # create file directory
    os.makedirs("./files/" + data_set, exist_ok=True)

    # API REQUEST
    c = cdsapi.Client()
    filename = "./files/" + data_set + "/file_id_" + str(pk) + save_format

    try:
        c.retrieve(
            data_set,
            options,
            filename
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
    curr_task.bytes = os.path.getsize(filename)
    curr_task.save()
