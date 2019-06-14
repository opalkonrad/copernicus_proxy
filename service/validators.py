from django.core.exceptions import ValidationError
import json


def unwrap_single_element_lists(options):
    for key in options:
        if len(options[key]) == 1:
            options[key] = options[key][0]


def validate_data_set(data_set):
    if not data_set:
        raise ValidationError('no matching data set')


def validate_options(options, required_options):
    # compare keys and if different show the difference
    if set(options.keys()) != set(required_options.keys()):
        diff_keys = ''
        for key in required_options.keys():
            if key not in options.keys():
                diff_keys += key + ','

        diff_keys = diff_keys[:-1]
        raise ValidationError('lack of required keys: ' + diff_keys)

    # check required attributes
    for req_attr, req_value in required_options.items():
        # check if variable is always "all", "at_least_one" or "one"
        if req_value == 'all':
            if options[req_attr] != 'all':
                raise ValidationError(req_attr + ' should be "all"')

        if req_value == 'at_least_one':
            if len(options[req_attr]) <= 0:
                raise ValidationError('you have to choose at least one option for attribute: ' + req_attr)

        if req_value == 'one':
            if type(options[req_attr]) != str:  # it should be changed to str while unwrapping if contained one option
                raise ValidationError(req_attr + ' should contain only one selected option')


def validate_json_content(value):
    from service.models import DataSet
    try:
        data = json.loads(value)
    except json.JSONDecodeError:
        raise ValidationError('JSON decoding failed')

    data_set = DataSet.get_by_name(data['data_set'])  # string that defines a data_set
    validate_data_set(data_set)

    options = data['options']  # dictionary that contains filled options of the form
    unwrap_single_element_lists(options)
    required_options = json.loads(data_set.attributes)
    validate_options(options, required_options)


def validate_json(value):
    try:
        json.loads(value)
    except json.JSONDecodeError:
        raise ValidationError('JSON decoding failed')
