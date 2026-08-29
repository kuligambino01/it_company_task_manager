from django.urls import path

from task.views import (
    dashboard,
    TaskListView,
    TaskDetailView, TaskCreateView,
)

app_name = "task"

urlpatterns = [
    path("",
         dashboard,
         name="dashboard"),
    path("tasks/",
         TaskListView.as_view(),
         name="task-list"),
    path("tasks/<int:pk>/details",
         TaskDetailView.as_view(),
         name="task-detail"),
    path("tasks/create",
         TaskCreateView.as_view(),
         name="task-create"),
]
