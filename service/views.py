from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.http import QueryDict
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from sea_level.settings import BASE_DIR
from service.models import Task as TaskModel, DataSet as DataSetModel
from service.constants import formats
from django.core.exceptions import ValidationError
import os
import json


# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
class CsrfFreeView(View):
    """
    Cross-site request forgery unsafe view for processing requests without csrf token.
    """


class TaskList(CsrfFreeView):
    """
    View for displaying all tasks (GET) and creating new task (POST)
    """

    def get(self, request):
        return JsonResponse(TaskModel.list_all(), safe=False)

    def post(self, request):
        json_content = request.POST.get('json_content', '')
        try:
            task = TaskModel(json_content=json_content)
            task.full_clean()
            task.save()
            return JsonResponse({'task_id': task.pk})
        except ValidationError as e:
            task = TaskModel(json_content=json_content, status='error', msg=e)
            task.save()
            return HttpResponse(e, status=400)


class Task(CsrfFreeView):
    """
    View for displaying (GET) all information about single task indicated by 'id' in the URL
    """

    def get(self, request, url_id):
        try:
            task = TaskModel.objects.get(id=url_id)
            return JsonResponse(task.to_dict())
        except TaskModel.DoesNotExist:
            return HttpResponse(status=404)


class File(View):
    """
    View for downloading (GET) single file indicated by 'id' in the URL
    """

    def get(self, request, url_id):

        requested_file = TaskModel.objects.get(id=url_id)

        json_string = json.loads(requested_file.json_content)

        data_set = json_string[0]
        file_format = json_string[1]['format']

        for f in formats.list:
            if f.extension[1] == file_format:
                file_format = f.extension[0]

        file_location = os.path.join(BASE_DIR, 'files', data_set, 'file_id_' + str(url_id) + file_format)

        try:
            with open(file_location, 'rb') as f:
                file_data = f.read()

            # sending response
            response = HttpResponse(file_data, content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename="file_id_' + str(url_id) + file_format
            return response

        except IOError:
            return HttpResponse(status=404)
        # handle file not exist case here
        # search for file indicated by id, if none return 404
        # try:
        #    task = FileModel.objects.get(id=url_id)
        # except:
        #    return HttpResponse(status=404)


class DataSetList(CsrfFreeView):
    """
    View for displaying all records (GET) and creating new record (POST)
    """

    def get(self, request):
        return JsonResponse(DataSetModel.list_all(), safe=False)

    def post(self, request):
        ds = request.POST.get('data_set', '')
        attrs = request.POST.get('attributes', '')
        try:
            new_data_set = DataSetModel(data_set=ds, attributes=attrs)
            new_data_set.full_clean()
            new_data_set.save()
            return HttpResponse(status=201)

        except ValidationError as e:
            return HttpResponse(e, status=400)


class DataSet(CsrfFreeView):
    """
    View for editing single record indicated by 'id' (PUT)
    """

    def put(self, request, url_id):
        try:
            req_json = json.loads(request.body)
            attrs = '{'
            for key, val in req_json["attributes"].items():
                attrs += '"' + key + '":'
                attrs += '"' + val + '",'
            attrs = attrs[:-1] + '}'

            existing_db_record = DataSetModel.objects.get(id=url_id)
            existing_db_record.data_set = req_json["data_set"]
            existing_db_record.attributes = attrs
            existing_db_record.full_clean()
            existing_db_record.save()
            return HttpResponse(status=200)

        except json.JSONDecodeError as e:
            return HttpResponse(e, status=400)

        except ObjectDoesNotExist as e:
            return HttpResponse(e, status=400)

        except ValidationError as e:
            return HttpResponse(e, status=400)

    def delete(self, request, url_id):
        try:
            DataSetModel.objects.get(id=url_id).delete()
            return HttpResponse(status=200)
        except ObjectDoesNotExist as e:
            return HttpResponse(e, status=400)
