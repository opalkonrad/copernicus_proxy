import json
import random
from random import randint
import os


def generate_era5(number_of_tests):
    # define dataset
    data_set = 'reanalysis-era5-single-levels'

    # defines how many of each parameter is generated
    number_of_years = 2
    number_of_months = 2
    number_of_days = 1
    number_of_hours = 1

    all_strings = open(os.path.dirname(os.path.abspath(__file__)) + '/all_era5_filters.json')
    json_data = all_strings.read()
    list_of_strings = json.loads(json_data)

    list_of_products = ['ensemble_mean', 'ensemble_members', 'ensemble_spread', 'reanalysis']
    list_of_formats = ['grib', 'netcdf']

    list_of_tasks = []

    for i in range(number_of_tests):
        product = random.sample(set(list_of_products), 1)
        filters = random.sample(set(list_of_strings), 1)
        fileformat = random.sample(set(list_of_formats), 1)

        years = []
        for i in range(number_of_years):
            years.append(str(randint(1979, 2018)))
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

        hours = []
        for i in range(number_of_hours):
            hour = str(3 * randint(0, 7))
            if len(hour) == 1:
                hour = '0' + hour
            hour = hour + ":00"
            hours.append(hour)
        hours = list(dict.fromkeys(hours))  # remove duplicates

        dictionary = {"product_type": product, "variable": filters, "year": years, "month": months, "day": days,
                      "time": hours, "format": fileformat}
        task = {
            "data_set": data_set,
            "options": dictionary
        }

        list_of_tasks.append(task)

    return list_of_tasks
