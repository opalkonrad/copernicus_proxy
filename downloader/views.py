from django.http import HttpResponse
from downloader.forms.sea_level_form import SeaLevelForm
from django.views.generic.edit import FormView
from django.views.generic import ListView
from downloader.models import Task
import downloader.forms.sea_level_choices as options
from .tasks import download_from_cdsapi
from django.shortcuts import redirect
import json
from .query_validation import query_validation


def index(request):
    return HttpResponse("Hello, world. You're at the downloader index.")


class SeaLevelView(FormView):
    template_name = 'sea_level/sea_level.html'
    form_class = SeaLevelForm
    success_url = '/downloader/db_browser/'

    def get_context_data(self, **kwargs):
        context = super(SeaLevelView, self).get_context_data(**kwargs)
        context['options'] = options
        return context

    def form_valid(self, form):
        # form.cleaned_data - tuple of data_set name and filled options of the form
        json_form = form.cleaned_data['serialized_form']
        query_validation(json.loads(json_form))
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

        return redirect("/downloader/db_browser")


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
            # check if task is appropriate
            if task.status != "error":
                task.status = "waiting in queue"
                task.msg = ""
                task.save()

                download_from_cdsapi.delay(task.json_content, pk)

        return redirect("/downloader/db_browser")
