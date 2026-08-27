from django.urls import path

from task.views import dashboard

app_name = "task"


urlpatterns = [
    path("", dashboard, name='dashboard',)
]