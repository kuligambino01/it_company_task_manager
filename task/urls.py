from django.urls import path

from task.views import (
    dashboard,
    TaskTypeListView,
    TaskTypeCreateView,
    TaskTypeUpdateView,
)

app_name = "task"

urlpatterns = [
    path("",
         dashboard,
         name="dashboard"),
    path("task_types/",
         TaskTypeListView.as_view(),
         name="task_type-list"),
    path("task_types/create",
         TaskTypeCreateView.as_view(),
         name="task_type-create"),
    path("task_types/<int:pk>/update",
         TaskTypeUpdateView.as_view(),
         name="task_type-update")
]
