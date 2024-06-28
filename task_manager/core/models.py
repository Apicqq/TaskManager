from django.db import models
from django.db.models.functions.datetime import Now

from core.constants import TASK_STATUSES


class TaskSubtaskBaseModel(models.Model):
    """
    Базовая модель для задач и подзадач, включающая в себя схожие поля.
    """

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
    status = models.CharField(
        verbose_name="Статус задачи",
        max_length=100,
        choices=TASK_STATUSES,
        default=TASK_STATUSES[0][0],
    )
    planned_intensity = models.IntegerField(
        verbose_name="Планируемая интенсивность",
    )
    deadline = models.DateTimeField(
        verbose_name="Дата завершения задачи",
        null=True,
    )
    actual_completion_time = models.IntegerField(
        "Фактическое время выполнения",
        help_text="В часах",
    )

    class Meta:
        abstract = True
        constraints = [
            models.CheckConstraint(
                check=models.Q(deadline__gte=Now()),
                name="deadline_cannot_be_in_the_past",
            ),
        ]
