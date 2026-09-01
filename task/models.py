from django.contrib.auth.models import AbstractUser
from django.db import models


class TaskType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.username} - {self.position}"


class Priority(models.TextChoices):
    URGENT = "urgent", "URGENT"
    LOW = "low", "LOW"
    MEDIUM = "medium", "MEDIUM"
    HIGH = "high", "HIGH"


class Task(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    assignees = models.ManyToManyField(Worker, related_name="tasks")

    def __str__(self):
        return self.name
