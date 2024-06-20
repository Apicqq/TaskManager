from django.db import models
from django.db.models.functions.datetime import Now

from core.constants import TASK_STATUSES


class TaskSubtaskBaseModel(models.Model):
    """
    Базовая модель для задач и подзадач, включающая в себя схожие поля.
    """

    name = models.CharField(
        max_length=100,
        verbose_name="Название задачи",
    )
    description = models.TextField(
        verbose_name="Описание задачи",
    )
    performers = models.CharField(
        max_length=100,
        verbose_name="Исполнители",
        null=True,
    )
    created_at = models.DateTimeField(
        verbose_name="Дата регистрации задачи",
        auto_now_add=True,
    )
    deadline = models.DateTimeField(
        verbose_name="Дата завершения задачи",
        null=True,
    )
    status = models.CharField(
        verbose_name="Статус задачи",
        max_length=100,
        choices=TASK_STATUSES,
    )
    planned_intensity = models.IntegerField()
    actual_completion_time = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.name}: {self.description}"

    class Meta:
        abstract = True
        constraints = [
            models.CheckConstraint(
                check=models.Q(deadline__gte=Now()),
                name="deadline_cannot_be_in_the_past",
            ),
        ]
