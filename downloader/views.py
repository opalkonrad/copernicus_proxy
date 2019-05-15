from django.http import HttpResponse
from downloader.forms.sea_level_form import SeaLevelForm
from django.views.generic.edit import FormView
from django.views.generic import ListView
from downloader.models import Request
import downloader.forms.sea_level_choices as options
from .tasks import download_from_cdsapi
import json


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
        data = form.cleaned_data
        result = {
            'years': json.loads(data.get('years')),
            'months': json.loads(data.get('months')),
            'days': json.loads(data.get('days')),
            'format': data.get('format')
        }
        to_db = Request(json_content=json.dumps(result))
        to_db.save()
        return super().form_valid(form)


class DatabaseBrowser(ListView):
    template_name = 'sea_level/db_browser.html'
    context_object_name = 'requests'
    success_url = '/downloader/sea_level/'

    def get_queryset(self):
        return Request.objects.all()

    def post(self, request, *args, **kwargs):
        pk = request.POST.get("id")
        req = Request.objects.get(id=pk)

        if "download" in request.POST:
            download_from_cdsapi.delay(req.json_content, pk)

            # update request's status in database
            req.status = "being downloaded"
            req.save()
            
            return HttpResponse("Works")
