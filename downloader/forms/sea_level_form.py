from django import forms
import downloader.forms.sea_level_choices as options


class SeaLevelForm(forms.Form):
    years = forms.CharField(required=True, min_length=3)
    months = forms.CharField(required=True, min_length=3)
    days = forms.CharField(required=True, min_length=3)
    format = forms.ChoiceField(
        widget=forms.Select,
        choices=options.formats,
        required=True
    )
