from django.http import HttpResponse
from downloader.forms.sea_level_form import SeaLevelForm
from django.views.generic.edit import FormView
from downloader.apps import TEMPLATES_DIR
import os
import json


def index(request):
    return HttpResponse("Hello, world. You're at the downloader index.")


class SeaLevelView(FormView):
    template_name = 'sea_level/sea_level.html'
    form_class = SeaLevelForm
    success_url = '/downloader/'

    def form_valid(self, form):
        result = {
            "years": [],
            "months": [],
            "days": [],
            "format": ""
        }
        tmp_format = ""

        for key, values in form.cleaned_data.items():
            for value in values:
                if key == 'format':
                    tmp_format += value
                    continue

                result[key].append(int(value))

        result['format'] = tmp_format

        return HttpResponse(json.dumps(result))
