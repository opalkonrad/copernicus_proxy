from django.http import HttpResponse
from downloader.forms.sea_level_form import SeaLevelForm
from django.views.generic.edit import FormView
from django.views.generic import ListView
import downloader.forms.sea_level_choices as options
from django.shortcuts import redirect
import json
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


class DatabaseBrowser(ListView):
    template_name = 'sea_level/db_browser.html'
    context_object_name = 'tasks'
    success_url = '/downloader/sea_level/'

    def get_queryset(self):
        task_list_url = self.request.build_absolute_uri(reverse('task_list'))
        r = requests.get(task_list_url)
        return json.loads(r.text)

    def post(self, request):
        action = request.POST.get('action', '')
        task_id = request.POST.get('task_id', '')
        if action == 'delete':
            task_url = self.request.build_absolute_uri(reverse('task', kwargs={'url_id': task_id}))
            requests.delete(task_url)
        return redirect('/downloader/db_browser/')
