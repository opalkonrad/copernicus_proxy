from django.http import HttpResponse
from canvas.forms.canvas_form import SeaLevelForm
from django.views.generic.edit import FormView
from django.views.generic import ListView
import canvas.forms.canvas_choices as options
from django.shortcuts import redirect
from django.urls import reverse
from service.management.commands.restartworkers import reset_task_queue, reset_workers
import requests
import json


def index(request):
    task_list_url = request.build_absolute_uri(reverse('task_list'))
    r = requests.get(task_list_url)
    return HttpResponse(str(r.status_code) + ": " + str(r.text))


class CopernicusView(FormView):
    template_name = 'canvas/copernicus.html'
    form_class = SeaLevelForm
    success_url = '/canvas/db_browser/'

    def get_context_data(self, **kwargs):
        context = super(CopernicusView, self).get_context_data(**kwargs)
        context['options'] = options
        return context

    def form_valid(self, form):
        json_content = form.cleaned_data['json_content']
        task_list_url = self.request.build_absolute_uri(reverse('task_list'))
        requests.post(task_list_url, data={'json_content': json_content})
        return super().form_valid(form)


class TestView(FormView):
    template_name = 'canvas/testing.html'
    form_class = SeaLevelForm
    success_url = '/canvas/db_browser/'


class DatabaseBrowser(ListView):
    template_name = 'canvas/db_browser.html'
    context_object_name = 'tasks'
    success_url = '/canvas/canvas/'

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
            reset_workers(10)
            reset_task_queue()
        return redirect('/canvas/db_browser/')
