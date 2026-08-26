from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from task.models import TaskType, Task, Position, Worker


# Register your models here.

@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "deadline", "is_completed", "priority", "task_type",)
    search_fields = ("priority",)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = ("position",) + UserAdmin.list_display
    fieldsets = UserAdmin.fieldsets
    list_filter = ("position__name",)
