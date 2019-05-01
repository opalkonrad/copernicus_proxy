from django.http import HttpResponse
from downloader.forms.sea_level_form import SeaLevelForm
from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.shortcuts import render
from downloader.apps import TEMPLATES_DIR
import os
import json
import cdsapi
from downloader.constants import formats
from downloader.models import Request
from django.db import models


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
        tmp_format_api = ""     # Api format e.g. "tgz"
        tmp_format_ext = ""     # File extension e.g. ".tar.gz"
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

        to_db = Request(json_content = json.dumps(result))
        to_db.save()
        return HttpResponse(json.dumps(result))

class DatabaseBrowser(ListView):
    template_name = 'sea_level/db_browser.html'
    context_object_name = 'requests'

    def get_queryset(self):
        return Request.objects.all()