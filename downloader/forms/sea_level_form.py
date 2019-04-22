from django import forms


class SeaLevelForm(forms.Form):
    year_choice = (
        ("1998", "year 1998"),
        ("1999", "year 1999"),
        ("2000", "year 2000"),
        )
    years = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=year_choice)
