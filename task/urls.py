from django.urls import path

from task.views import dashboard, TaskTypeListView

app_name = "task"

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("task_types/", TaskTypeListView.as_view(), name="task_type-list"),
]
