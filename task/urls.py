from django.urls import path

from task.views import (
    dashboard,
    TaskListView
)

app_name = "task"

urlpatterns = [
    path("",
         dashboard,
         name="dashboard"),
    path("tasks/",
         TaskListView.as_view(),
         name="task-list"),
]
