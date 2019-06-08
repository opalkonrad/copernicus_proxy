from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from sea_level.settings import BASE_DIR
from .query_validation import query_validation
import json
import os


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
        return HttpResponse(status=200)

    def post(self, request):
        json_form = request.POST.get('serialized_form', '')
        if query_validation(json.loads(json_form)):
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)


class Task(CsrfFreeView):
    """
    View for displaying (GET) single task indicated by 'id' in the URL
    """

    def get(self, request, url_id):
        return HttpResponse(status=200)


class File(View):
    """
    View for downloading (GET) single file indicated by 'id' in the URL
    """

    def get(self, request, url_id):

        file_location = os.path.join(BASE_DIR, 'files', '1.txt')

        try:
            with open(file_location, 'r') as f:
                file_data = f.read()

            # sending response
            response = HttpResponse(file_data, content_type='text/plain ')
            response['Content-Disposition'] = 'attachment; filename="1.txt"'
            return response

        except IOError:
            return HttpResponse(status=404)
        # handle file not exist case here
        # search for file indicated by id, if none return 404
        # try:
        #    task = FileModel.objects.get(id=url_id)
        # except:
        #    return HttpResponse(status=404)


class DataSet(CsrfFreeView):
    """
    View for creating (POST) or editing (PUT) dataset indicated by 'id' in the URL
    """

    def post(self, request, url_id):
        return HttpResponse(status=200)

    def put(self, request, url_id):
        return HttpResponse(status=200)
