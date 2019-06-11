from django.http import HttpResponse
from downloader.forms.sea_level_form import SeaLevelForm
from django.views.generic.edit import FormView
from django.views.generic import ListView
import downloader.forms.sea_level_choices as options
from .tasks import download_from_cdsapi
from django.shortcuts import redirect
import json
from .query_validation import query_validation
from django.urls import reverse
from service.models import Task as TaskModel
import requests


def index(request):
    task_list_url = request.build_absolute_uri(reverse('task_list'))
    r = requests.get(task_list_url)
    return HttpResponse(str(r.status_code) + ": " + str(r.text))


class SeaLevelView(FormView):
    template_name = 'sea_level/sea_level.html'
    form_class = SeaLevelForm
    success_url = '/downloader/db_browser/'

    def get_context_data(self, **kwargs):
        context = super(SeaLevelView, self).get_context_data(**kwargs)
        context['options'] = options
        return context

    def form_valid(self, form):
        json_content = form.cleaned_data['json_content']
        task_list_url = self.request.build_absolute_uri(reverse('task_list'))
        requests.post(task_list_url, data={'json_content': json_content})
        return super().form_valid(form)


class TestView(FormView):
    template_name = 'sea_level/testing.html'
    form_class = SeaLevelForm
    success_url = '/downloader/db_browser/'

    def post(self, request):
        if request.method == 'POST':
            json_text = request.POST.get('textfield', None)
            full_data = json.loads(json_text)  # array with [(data_set_name, filled_form_json), ...]

            for data in full_data:
                query_validation(data)

        return redirect('/downloader/db_browser/')


class DatabaseBrowser(ListView):
    template_name = 'sea_level/db_browser.html'
    context_object_name = 'tasks'
    success_url = '/downloader/sea_level/'

    def get_queryset(self):
        task_list_url = self.request.build_absolute_uri(reverse('task_list'))
        r = requests.get(task_list_url)
        return json.loads(r.text)

    def post(self, request, *args, **kwargs):
        pk = request.POST.get("id")
        task = TaskModel.objects.get(id=pk)

        if "download" in request.POST:
            # check if task is appropriate
            if task.status != "error":
                task.status = "waiting in queue"
                task.msg = ""
                task.save()
                download_from_cdsapi.delay(pk)

        return redirect('/downloader/db_browser/')
