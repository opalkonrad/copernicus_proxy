from django import forms


class SeaLevelForm(forms.Form):
    year_choice = (
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        )
    years = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=year_choice)
