from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from task.models import Task


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
