import json

# it creates tuples with nice looking names

name = 'all_strings'

era5file = open('./strings/' + name + '.json')
json_data = era5file.read()
list_of_strings = json.loads(json_data)

tuples = []

for string in list_of_strings:
    string2 = string.replace("_", " ")
    string2 = string2.capitalize()
    newtuple = (string, string2)
    tuples.append(newtuple)

with open('./strings/' + name + '_tuples.json', 'w') as outfile:
    json.dump(tuples, outfile)