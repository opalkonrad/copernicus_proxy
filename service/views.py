from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


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
        return HttpResponse(status=200)


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
        return HttpResponse(status=200)


class DataSet(CsrfFreeView):
    """
    View for creating (POST) or editing (PUT) dataset indicated by 'id' in the URL
    """

    def post(self, request, url_id):
        return HttpResponse(status=200)

    def put(self, request, url_id):
        return HttpResponse(status=200)
