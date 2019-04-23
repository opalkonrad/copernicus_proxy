from django.http import HttpResponse
from downloader.forms.sea_level_form import SeaLevelForm
from django.views.generic.edit import FormView
from downloader.apps import TEMPLATES_DIR
import os
import json
import cdsapi


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
        tmp_years = ""
        tmp_months = ""
        tmp_days = ""

        for key, values in form.cleaned_data.items():
            for value in values:
                if key == 'format':
                    tmp_format += value
                    continue

                result[key].append(value)

                if key == 'years':
                    tmp_years += "%d" % int(value)
                    tmp_years += ","

                if key == 'months':
                    tmp_months += "%d" % int(value)
                    tmp_months += ","

                if key == 'days':
                    tmp_days += "%d" % int(value)
                    tmp_days += ","

        result['format'] = tmp_format

        tmp_years = tmp_years[:-1]
        tmp_months = tmp_months[:-1]
        tmp_days = tmp_days[:-1]

        c = cdsapi.Client()

        c.retrieve(
            'satellite-sea-level-mediterranean',
            {
                'variable': 'all',
                'format': 'zip',
                'year': tmp_years.split(','),
                'month': tmp_months.split(','),
                'day': tmp_days.split(',')
            },
            'download.zip')

        return HttpResponse(json.dumps(result))
