import json 

fileopen = open('generated.json')
json_text = fileopen.read()
full_data = json.loads(json_text)

for data in full_data:
    result = data[1]

    # we don't want single-element lists
    for key in result:
        if len(result[key]) == 1:
            tmp = result[key][0]
            result[key] = tmp

    print(result)
