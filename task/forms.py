from django import forms


class TaskSearchForm(forms.Form):
    is_completed = forms.TypedChoiceField(
        choices=(
            ("", "All"),
            ("true", "Completed"),
            ("false", "Not completed")),
        coerce=lambda value: value == "true",
        empty_value=None,
        required=False)
