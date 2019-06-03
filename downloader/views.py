from django.http import HttpResponse
from downloader.forms.sea_level_form import SeaLevelForm
from django.views.generic.edit import FormView
from django.views.generic import ListView
from downloader.models import Task
import downloader.forms.sea_level_choices as options
from .tasks import download_from_cdsapi
from django.shortcuts import redirect
import json
from .models import DataSets


def index(request):
    return HttpResponse("Hello, world. You're at the downloader index.")


class SeaLevelView(FormView):
    template_name = 'sea_level/sea_level.html'
    form_class = SeaLevelForm
    success_url = '/downloader/db_browser/'
    #data_set = 'reanalysis-era5-single-levels'

    def get_context_data(self, **kwargs):
        context = super(SeaLevelView, self).get_context_data(**kwargs)
        context['options'] = options
        return context

    def form_valid(self, form):
        data = form.cleaned_data
        # data should be a tuple consisting of a string that defines a dataset, and a dictonary that contains all required parameters

        result = data[1]

        # we don't want single-element lists
        for key in result:
            if len(result[key]) == 1:
                tmp = result[key][0]
                del result[key]
                result[key] = tmp

        to_db = Task(json_content=json.dumps(result), data_set=data[0])
        to_db.save()
        return super().form_valid(form)


class DatabaseBrowser(ListView):
    template_name = 'sea_level/db_browser.html'
    context_object_name = 'tasks'
    success_url = '/downloader/sea_level/'

    def get_queryset(self):
        return Task.objects.all()

    def post(self, request, *args, **kwargs):
        pk = request.POST.get("id")
        task = Task.objects.get(id=pk)

        if "download" in request.POST:
            # tmp0 = DataSets(data_set='satellite-sea-level-mediterranean', attributes='{"variable":[], "format":[], "day":[], "year":[], "month":[]}')
            # tmp0.save()
            # tmp1 = DataSets(data_set='reanalysis-era5-single-levels', attributes='{"product_type":[], "format":[], "variable":[], "day":[], "year":[], "month":[], "time":[]}')
            # tmp1.save()
            download_from_cdsapi.delay(task.json_content, pk)

            # update task's status in database
            task.status = "being downloaded"
            task.save()
            
            return redirect("/downloader/db_browser")
