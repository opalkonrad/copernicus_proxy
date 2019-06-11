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
    required_options_counter = 0  # next attribute from db
    options_counter = 0  # for compare if attr from db exists in form

    # change it later to set(dict_1.keys()) == set(dict_2.keys())
    # check required attributes
    for single_required_option in required_options:
        required_options_counter += 1

        # look for attributes
        for key in options:
            if single_required_option == key:
                options_counter += 1

        # check if variable is always "all" or "at_least_one"
        if single_required_option == 'variable':
            if required_options["variable"] == 'at_least_one':
                if len(options["variable"]) <= 0:
                    raise ValidationError('you have to choose at least one option for variable')

            if required_options["variable"] == 'all':
                if options["variable"] != 'all':
                    raise ValidationError('variable should be "all"')

        # lack of attribute in form needed for Copernicus
        if required_options_counter != options_counter:
            raise ValidationError('lack of argument in form - ' + single_required_option)


def validate_json_content(value):
    from service.models import DataSet
    try:
        data = json.loads(value)
    except json.JSONDecodeError:
        raise ValidationError('JSON decoding failed')

    DataSet.initialize_data_sets()
    data_set = DataSet.get_by_name(data[0])  # string that defines a data_set
    validate_data_set(data_set)

    options = data[1]  # dictionary that contains filled options of the form
    unwrap_single_element_lists(options)
    required_options = json.loads(data_set.attributes)
    validate_options(options, required_options)
