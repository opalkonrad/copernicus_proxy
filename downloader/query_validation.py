from .models import DataSets
from django.core.exceptions import ObjectDoesNotExist, ValidationError
import json
from downloader.models import Task
from django.http import HttpResponse


def query_validation(data):
    # tmp0  DataSets(data_set='satellite-sea-level-mediterranean', attributes='{"variable": "all", "format": "null", "day": "null, "year": "null", "month": "null"}')
    # tmp0.save()
    # tmp1 = DataSets(data_set='reanalysis-era5-single-levels', attributes='{"product_type": "null", "format": "null", "variable": "at_least_one", "day": "null", "year": "null", "month": "null", "time": "null"}')
    # tmp1.save()

    data_set = data[0]  # string that defines a data_set
    result = data[1]  # dictionary that contains filled options of the form

    # we don't want single-element lists
    for key in result:
        if len(result[key]) == 1:
            result[key] = result[key][0]

    # check required attributes
    # try:
    #     db_form = DataSets.objects.get(data_set=data_set)

    except ObjectDoesNotExist:
        curr_task = Task(json_content=json.dumps(result), data_set=data[0])
        curr_task.status = "error"
        curr_task.msg = "no matching data set"
        curr_task.save()
        return

    # load required attributes from db
    attr_check = json.loads(db_form.attributes)

    db_cntr = 0  # next attribute from db
    internal_cntr = 0  # for compare if attr from db exists in form

    # check required attributes
    try:
        for attr_db in attr_check:
            db_cntr += 1

            # look for attributes
            for key in result:
                if attr_db == key:
                    internal_cntr += 1

            # check if variable is always "all" or "at_least_one"
            if attr_db == 'variable':
                if attr_check["variable"] == 'at_least_one':
                    if len(result["variable"]) <= 0:
                        raise ValidationError('you have to choose at least one option for variable')

                if attr_check["variable"] == 'all':
                    if result["variable"] != 'all':
                        raise ValidationError('variable should be "all"')

            # lack of attribute in form needed for Copernicus
            if db_cntr != internal_cntr:
                raise ValidationError('lack of argument in form - ' + attr_db)

    except ValidationError as e:
        # update request's status in database to error
        curr_task = Task(json_content=json.dumps(result), data_set=data[0])
        curr_task.status = "error"
        curr_task.msg = e
        curr_task.save()
        return

    curr_task = Task(json_content=json.dumps(result), data_set=data[0])
    curr_task.save()
