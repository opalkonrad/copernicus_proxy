from django.http import HttpResponse
from downloader.forms.sea_level_form import SeaLevelForm
from django.views.generic.edit import FormView
from downloader.apps import TEMPLATES_DIR
import os
import json
import cdsapi
from downloader.constants import formats
import downloader.forms.sea_level_choices as options


def index(request):
    return HttpResponse("Hello, world. You're at the downloader index.")


class SeaLevelView(FormView):
    template_name = 'sea_level/sea_level.html'
    form_class = SeaLevelForm
    success_url = '/downloader/'

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
        return HttpResponse(json.dumps(result))
