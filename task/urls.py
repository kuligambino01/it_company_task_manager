from django.urls import path

from task.views import (
    dashboard,
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
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
    path("tasks/<int:pk>/update",
         TaskUpdateView.as_view(),
         name="task-update"),
]
