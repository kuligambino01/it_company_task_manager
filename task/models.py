from django.contrib.auth.models import AbstractUser
from django.db import models


class TaskType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    def __str__(self):
        if self.position:
            return f"{self.username} - {self.position}"
        return self.username


class Priority(models.TextChoices):
    LOW = "low", "LOW"
    MEDIUM = "medium", "MEDIUM"
    HIGH = "high", "HIGH"
    URGENT = "urgent", "URGENT"


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
    task_type = models.ForeignKey(TaskType, on_delete=models.PROTECT)
    assignees = models.ManyToManyField(Worker, related_name="tasks")

    def __str__(self):
        return self.name
