from django.db import models
from django.db.models.functions.datetime import Now

from core.constants import Literals, TASK_STATUSES


class TaskSubtaskBaseModel(models.Model):
    """
    Базовая модель для задач и подзадач, включающая в себя схожие поля.
    """

    description = models.TextField(
        verbose_name=Literals.DESCRIPTION,
    )
    performers = models.CharField(
        max_length=100,
        verbose_name=Literals.PERFORMERS,
        null=True,
    )
    created_at = models.DateTimeField(
        verbose_name=Literals.CREATED_AT,
        auto_now_add=True,
    )
    status = models.CharField(
        verbose_name=Literals.STATUS,
        max_length=100,
        choices=TASK_STATUSES,
        default=TASK_STATUSES[0][0],
    )
    planned_intensity = models.IntegerField(
        verbose_name=Literals.PLANNED_INTENSITY,
    )
    deadline = models.DateTimeField(
        verbose_name=Literals.DEADLINE,
        null=True,
    )
    actual_completion_time = models.IntegerField(
        Literals.ACTUAL_COMPLETION_TIME,
        help_text=Literals.ACTUAL_COMPLETION_TIME_HELP_TEXT,
    )

    class Meta:
        abstract = True
        constraints = [
            models.CheckConstraint(
                check=models.Q(deadline__gte=Now()),
                name="deadline_cannot_be_in_the_past",
            ),
        ]
