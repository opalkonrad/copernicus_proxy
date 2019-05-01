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
        context['yearOptions'] = options.years
        context['monthOptions'] = options.months
        context['dayOptions'] = options.days
        return context

    def form_valid(self, form):
        result = {
            "years": [],
            "months": [],
            "days": [],
            "format": ""
        }
        tmp_format_api = ""  # Api format e.g. "tgz"
        tmp_format_ext = ""  # File extension e.g. ".tar.gz"
        tmp_years = ""
        tmp_months = ""
        tmp_days = ""

        # Filling the dictionary with a completed form
        for key, values in form.cleaned_data.items():
            for value in values:
                if key == 'format':
                    tmp_format_ext += value
                    continue

                result[key].append(value)

                if key == 'years':
                    tmp_years += "%d" % int(value)
                    tmp_years += ","

                if key == 'months':
                    tmp_months += "{:02d}".format(int(value))
                    tmp_months += ","

                if key == 'days':
                    tmp_days += "{:02d}".format(int(value))
                    tmp_days += ","

        result['format'] = tmp_format_ext

        # Find the right notation for the given format (needed for api -> format)
        for f in formats.list:
            if f.extension[0] == result['format']:
                tmp_format_api = f.extension[1]

        # Delete the comma at the end of string
        tmp_years = tmp_years[:-1]
        tmp_months = tmp_months[:-1]
        tmp_days = tmp_days[:-1]

        # API REQUEST
        c = cdsapi.Client()

        c.retrieve(
            'satellite-sea-level-mediterranean',
            {
                'variable': 'all',
                'format': tmp_format_api,
                'year': tmp_years.split(','),
                'month': tmp_months.split(','),
                'day': tmp_days.split(',')
            },
            "download" + result['format'])

        return HttpResponse(json.dumps(result))
