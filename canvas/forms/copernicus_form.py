from django import forms


class CopernicusForm(forms.Form):
    json_content = forms.CharField(required=True, min_length=3)
    filling_type = forms.CharField(required=True, min_length=3)
    number_of_forms = forms.IntegerField(required=True)
