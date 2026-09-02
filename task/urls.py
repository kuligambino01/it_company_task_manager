from django.urls import path

from task.views import (
    MyTasksListView,
    TaskCreateView,
    TaskDetailView,
    TaskListView,
    TaskUpdateView,
    assign_to_task_view,
    complete_task_view,
    dashboard,
)

app_name = "task"

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/create", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/<int:pk>/update", TaskUpdateView.as_view(), name="task-update"),
    path(
        "tasks/<int:pk>/complete/",
        complete_task_view,
        name="task-complete",
    ),
    path(
        "tasks/<int:pk>/assign/",
        assign_to_task_view,
        name="task-assign",
    ),
    path("my-tasks/", MyTasksListView.as_view(), name="my-tasks"),
]
