from django.db import models
from django.db.models.functions import Now

from core.constants import Literals, Values
from core.models import TaskSubtaskBaseModel


class TaskModel(TaskSubtaskBaseModel):
    """Модель задачи."""

    name = models.CharField(
        max_length=Values.NAME_MAX_LENGTH,
        verbose_name=Literals.TASK_NAME,
    )

    class Meta:
        verbose_name = Literals.TASK_VERBOSE_NAME
        verbose_name_plural = Literals.TASK_VERBOSE_NAME_PLURAL

    def __str__(self):
        return f"{self.name}: {self.description}"

    def save(self, *args, **kwargs):
        if self.status == Literals.COMPLETED_INTERNAL:
            self.actual_completion_time = Now()
            for subtask in self.subtasks.all():
                subtask.status = Literals.COMPLETED_INTERNAL
                subtask.save()
        super().save(*args, **kwargs)


class SubTask(TaskSubtaskBaseModel):
    """Модель подзадачи."""

    name = models.CharField(
        max_length=100,
        verbose_name=Literals.SUBTASK_NAME,
    )

    task = models.ForeignKey(
        TaskModel,
        blank=True,
        verbose_name=Literals.TASK_VERBOSE_NAME,
        on_delete=models.SET_NULL,
        related_name="subtasks",
        null=True,
    )

    class Meta:
        verbose_name = Literals.SUBTASK_VERBOSE_NAME
        verbose_name_plural = Literals.SUBTASK_VERBOSE_NAME_PLURAL

    def __str__(self):
        return f"{self.name}: {self.description}"
