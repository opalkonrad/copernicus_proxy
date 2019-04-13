from django import forms


class SeaLevelForm(forms.Form):
    years = forms.CharField()
    months = forms.CharField()
    days = forms.CharField()
