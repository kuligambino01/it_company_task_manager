from datetime import timedelta

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone

from task.models import Task


class TaskSearchForm(forms.Form):
    is_completed = forms.TypedChoiceField(
        choices=(
            ("", "All"),
            ("true", "Completed"),
            ("false", "Not completed")),
        coerce=lambda value: value == "true",
        empty_value=None,
        required=False)


class TaskCreationForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    deadline = forms.DateTimeField(
        initial=lambda: timezone.now() + timedelta(days=1),
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"},
            format="%Y-%m-%dT%H:%M"),
    )

    class Meta:
        model = Task
        fields = "__all__"

    def clean_deadline(self):
        deadline = self.cleaned_data["deadline"]

        if deadline <= timezone.now():
            raise ValidationError("Deadline must be in the future")

        return deadline
