from django.urls import path

from task.views import (
    dashboard,
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    toggle_task_complete_view
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
    path(
        "tasks/<int:pk>/complete/",
        toggle_task_complete_view,
        name="task-complete",
    )
]
