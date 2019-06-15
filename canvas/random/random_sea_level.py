import json
from random import randint
import sys


def generate_sea_level(number_of_tests):
    # define dataset
    data_set = 'satellite-sea-level-mediterranean'

    # defines how many of each parameter is generated
    number_of_years = 2
    number_of_months = 2
    number_of_days = 2

    # all_strings = open('all_era5_filters.json')
    # json_data = all_strings.read()
    # list_of_strings = json.loads(json_data)

    # list_of_products = ['ensemble_mean','ensemble_members','ensemble_spread','reanalysis']
    # list_of_formats = ['zip', 'tgz']

    list_of_tasks = []

    for i in range(number_of_tests):
        # fileformat = random.sample(set(list_of_formats), 1)

        years = []
        for i in range(number_of_years):
            years.append(str(randint(1995, 2018)))
        years = list(dict.fromkeys(years))  # remove duplicates

        months = []
        for i in range(number_of_months):
            month = str(randint(1, 12))
            if len(month) == 1:
                month = '0' + month
            months.append(month)
        months = list(dict.fromkeys(months))  # remove duplicates

        days = []
        for i in range(number_of_days):
            day = str(randint(1, 28))
            if len(day) == 1:
                day = '0' + day
            days.append(day)
        days = list(dict.fromkeys(days))  # remove duplicates

        dictionary = {"variable": "all", "year": years, "month": months, "day": days, "format": "zip"}
        task = {
            "data_set": data_set,
            "options": dictionary
        }

        list_of_tasks.append(task)

    return list_of_tasks
