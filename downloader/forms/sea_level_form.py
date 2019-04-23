from django import forms
import downloader.forms.sea_level_choices as options


class SeaLevelForm(forms.Form):
    years = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=options.years,
        required=True
    )
    months = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=options.months,
        required=True
    )
    days = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=options.days,
        required=True
    )
    format = forms.ChoiceField(
        widget=forms.Select,
        choices=options.formats,
        required=True
    )
