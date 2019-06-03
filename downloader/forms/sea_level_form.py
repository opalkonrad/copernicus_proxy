from django import forms
import downloader.forms.sea_level_choices as options


class SeaLevelForm(forms.Form):
    # product_types = forms.CharField(required=True, min_length=3)
    popular_filters = forms.CharField(required=True, min_length=3)
    temperature_and_pressure_filters = forms.CharField(required=True, min_length=3)
    years = forms.CharField(required=True, min_length=3)
    months = forms.CharField(required=True, min_length=3)
    days = forms.CharField(required=True, min_length=3)
    # hours = forms.CharField(required=True, min_length=3)
    format = forms.ChoiceField(
        widget=forms.Select,
        choices=options.formats,
        required=True
    )
