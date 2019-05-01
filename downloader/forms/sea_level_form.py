from django import forms
import downloader.forms.sea_level_choices as options


class SeaLevelForm(forms.Form):
    years = forms.CharField(required=True)
    months = forms.CharField(required=True)
    days = forms.CharField(required=True)
    format = forms.ChoiceField(
        widget=forms.Select,
        choices=options.formats,
        required=True
    )
