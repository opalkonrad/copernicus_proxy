# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
import cdsapi
import json
import os


@shared_task
def download_from_cdsapi(result, tmp_format_api, tmp_years, tmp_months, tmp_days):
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

    print("Pobralem") # temporary

    # on tutaj pobral pliczek, zajmij sie obsluga bazy danych ;)



