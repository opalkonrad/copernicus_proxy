from django import forms


class SeaLevelForm(forms.Form):
    json_content = forms.CharField(required=True, min_length=3)
