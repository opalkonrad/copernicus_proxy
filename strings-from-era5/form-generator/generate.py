#!/usr/bin/python

import json
import random
from random import randint
import sys

number_of_tests = int(sys.argv[1])

all_strings = open('all_strings.json')
json_data = all_strings.read()
list_of_strings = json.loads(json_data)

list_of_products = ['ensemble_mean','ensemble_members','ensemble_spread','reanalysis']

list_of_dicts = []

for i in range(number_of_tests):
    product = random.sample(set(list_of_products), 1)
    filters = random.sample(set(list_of_strings), 3)

    years = []
    for i in range(2):
        years.append(str(randint(1979,2018)))
    years = list(dict.fromkeys(years)) # remove duplicates

    months = []
    for i in range(2):
        month = str(randint(1,12))
        if len(month) == 1:
            month = '0' + month
        months.append(month)
    months = list(dict.fromkeys(months)) # remove duplicates
    

    days = []
    for i in range(1):
        day = str(randint(1,28))
        if len(month) == 1:
            month = '0' + month
        days.append(day)
    days = list(dict.fromkeys(days)) # remove duplicates

    hours = []
    for i in range(1):
        hour = str(3*randint(0,7))
        if len(hour) == 1:
            hour = '0' + hour
        hour = hour + ":00"
        hours.append(hour)
    hours = list(dict.fromkeys(hours)) # remove duplicates

    dictionary = {"product": product, "filters": filters, "years": years, "months": months, "days": days}
    list_of_dicts.append(dictionary)

    with open('generated.json', 'w') as outfile:
        json.dump(list_of_dicts, outfile)