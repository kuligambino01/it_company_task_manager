from django import forms


class TaskTypeSearchForm(forms.Form):
    name = forms.CharField(max_length=50, required=False)