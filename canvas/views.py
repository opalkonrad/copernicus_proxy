from django.http import HttpResponse
from canvas.forms.copernicus_form import CopernicusForm
from django.views.generic.edit import FormView
from django.views.generic import ListView
import canvas.forms.copernicus_choices as options
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
    form_class = CopernicusForm
    success_url = '/canvas/db_browser/'

    def get_context_data(self, **kwargs):
        context = super(CopernicusView, self).get_context_data(**kwargs)
        context['options'] = options
        return context

    def form_valid(self, form):
        json_content = form.cleaned_data['json_content']
        filling_type = form.cleaned_data['filling_type']
        if filling_type == 'manual':
            task_list_url = self.request.build_absolute_uri(reverse('task_list'))
            requests.post(task_list_url, data=json_content, headers={'content-type': 'application/json'})
        elif filling_type == 'random':
            data_set = json.loads(json_content)['data_set']
            number_of_forms = form.cleaned_data['number_of_forms']
            for i in range(1, number_of_forms + 1):
                raise ValueError(number_of_forms)
        return super().form_valid(form)


class DatabaseBrowser(ListView):
    template_name = 'canvas/db_browser.html'
    context_object_name = 'tasks'

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
