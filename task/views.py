from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.decorators.http import require_POST

from task.forms import TaskSearchForm, TaskForm
from task.models import (
    Task,
)


# Create your views here.

@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    workers = get_user_model().objects.count()
    tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(is_completed=True).count()
    open_tasks = Task.objects.filter(is_completed=False).count()
    my_tasks = (Task.objects.filter
        (
        assignees=request.user,
        is_completed=False, ).order_by("deadline")[:5]
    )

    context = {
        "workers": workers,
        "tasks": tasks,
        "completed_tasks": completed_tasks,
        "open_tasks": open_tasks,
        "my_tasks": my_tasks
    }

    return render(request, "task/dashboard.html", context=context)


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "task/task_list.html"
    queryset = Task.objects.select_related("task_type").prefetch_related("assignees").order_by("deadline")
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
    template_name = "task/task_form.html"
    success_url = reverse_lazy("task:task-list")
    form_class = TaskForm


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    template_name = "task/task_form.html"
    form_class = TaskForm

    def get_success_url(self):
        return reverse("task:task-detail",
                       kwargs={"pk": self.object.pk})


@login_required
def toggle_task_complete_view(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        task.is_completed = True
        task.save(update_fields=["is_completed"])

    return redirect("task:task-list")


@login_required
@require_POST
def assign_to_task_view(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if task.assignees.filter(pk=request.user.pk).exists():
        task.assignees.remove(request.user)
    else:
        task.assignees.add(request.user)

    return redirect("task:task-detail", task.pk)



class MyTasksListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "task/my_tasks.html"
    paginate_by = 10


    def get_queryset(self):
        queryset = Task.objects.filter(assignees=self.request.user).order_by("deadline")

        status = self.request.GET.get("status")

        if status == "completed":
            queryset = queryset.filter(is_completed=True)

        elif status == "open":
            queryset = queryset.filter(is_completed=False)

        return queryset