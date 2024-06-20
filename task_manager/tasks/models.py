from django.db import models

from core.models import TaskSubtaskBaseModel


class TaskModel(TaskSubtaskBaseModel):
    """Модель задачи."""

    subtasks = models.ForeignKey(
        "SubTask",
        blank=True,
        verbose_name="Подзадачи",
        on_delete=models.SET_NULL,
        related_name="subtasks",
        null=True
    )

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"


class SubTask(TaskSubtaskBaseModel):
    """Модель подзадачи."""

    class Meta:
        verbose_name = "Подзадача"
        verbose_name_plural = "Подзадачи"

