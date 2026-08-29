from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from task.forms import TaskSearchForm, TaskCreationForm
from task.models import (
    Task,
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


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "task/task_list.html"
    queryset = Task.objects.select_related("task_type").prefetch_related("assignees")
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context["search_form"] = TaskSearchForm(self.request.GET or None)

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = TaskSearchForm(self.request.GET)

        if form.is_valid():
            is_completed = form.cleaned_data.get("is_completed")

            if is_completed is not None:
                queryset = queryset.filter(is_completed=is_completed)

        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    template_name = "task/task_detail.html"


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    template_name = "task/task_creation_form.html"
    success_url = reverse_lazy("task:task-list")
    form_class = TaskCreationForm