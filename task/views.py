from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from task.forms import TaskTypeSearchForm
from task.models import (Task,
                         TaskType,

                         )


# Create your views here.

@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    workers = get_user_model().objects.count()
    task = Task.objects.count()
    context = {
        "workers": workers,
        "tasks": task
    }

    return render(request, "task/dashboard.html", context=context)


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    paginate_by = 10
    template_name = "task/task_type_list.html"
    form_class = TaskTypeSearchForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = TaskTypeSearchForm(
            initial={"name": name}
        )

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        name = self.request.GET.get("name")

        if name:
            return queryset.filter(name__icontains=name)

        return queryset
