from django.http import HttpResponse
from canvas.forms.copernicus_form import CopernicusForm
from django.views.generic.edit import FormView
from django.views.generic import ListView
import canvas.forms.copernicus_choices as options
from django.shortcuts import redirect
from django.urls import reverse
from service.management.commands.restartworkers import reset_task_queue, reset_workers
from canvas.random.random_sea_level import generate_sea_level
from canvas.random.random_era5 import generate_era5
import requests
import json


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
        task_list_url = self.request.build_absolute_uri(reverse('task_list'))
        if filling_type == 'manual':
            requests.post(task_list_url, data=json_content, headers={'content-type': 'application/json'})
        elif filling_type == 'random':
            number_of_forms = form.cleaned_data['number_of_forms']
            data_set = json.loads(json_content)['data_set']
            tasks = []
            if data_set == 'satellite-sea-level-mediterranean':
                tasks = generate_sea_level(number_of_forms)
            elif data_set == 'reanalysis-era5-single-levels':
                tasks = generate_era5(number_of_forms)
            for task in tasks:
                json_content = json.dumps(task)
                requests.post(task_list_url, data=json_content, headers={'content-type': 'application/json'})
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
