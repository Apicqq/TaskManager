from django.db import models
from django.db.models.functions import Now

from core.models import TaskSubtaskBaseModel


class TaskModel(TaskSubtaskBaseModel):
    """Модель задачи."""

    name = models.CharField(
        max_length=100,
        verbose_name="Название задачи",
    )

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def __str__(self):
        return f"{self.name}: {self.description}"

    def save(self, *args, **kwargs):
        if self.status == "Completed":
            self.actual_completion_time = Now()
            for subtask in self.subtasks.all():
                subtask.status = "Завершена"
                subtask.save()
        super().save(*args, **kwargs)


class SubTask(TaskSubtaskBaseModel):
    """Модель подзадачи."""

    name = models.CharField(
        max_length=100,
        verbose_name="Название подзадачи",
    )

    task = models.ForeignKey(
        TaskModel,
        blank=True,
        verbose_name="Задача",
        on_delete=models.SET_NULL,
        related_name="subtasks",
        null=True
    )

    class Meta:
        verbose_name = "Подзадача"
        verbose_name_plural = "Подзадачи"

    def __str__(self):
        return f"{self.name}: {self.description}"
