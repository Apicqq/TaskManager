from django.db import models
from django.db.models.functions import Now

from core.constants import Literals, Values, TASK_STATUSES
from tasks.validators import validate_deadline


class TaskModel(models.Model):
    """
    Модель задачи.

    Включает в себя поле "parent_task", которое является PK к самому себе,
    позволяющее создавать неограниченную вложенность задач, а также поле
    is_root_task, указывающее на "корневую" задачу, позволяющее отделять задачи
    от их подзадач.
    """

    name = models.CharField(
        max_length=Values.NAME_MAX_LENGTH,
        verbose_name=Literals.TASK_NAME,
    )

    description = models.TextField(
        verbose_name=Literals.DESCRIPTION,
    )
    performers = models.CharField(
        max_length=Values.NAME_MAX_LENGTH,
        verbose_name=Literals.PERFORMERS,
        null=True,
    )
    created_at = models.DateTimeField(
        verbose_name=Literals.CREATED_AT,
        auto_now_add=True,
    )
    status = models.CharField(
        verbose_name=Literals.STATUS,
        max_length=Values.NAME_MAX_LENGTH,
        choices=TASK_STATUSES,
        blank=True,
        default=TASK_STATUSES[0][0],
    )
    planned_intensity = models.IntegerField(
        verbose_name=Literals.PLANNED_INTENSITY,
    )
    deadline = models.DateTimeField(
        verbose_name=Literals.DEADLINE,
        null=True,
        validators=[validate_deadline],
    )
    actual_completion_time = models.IntegerField(
        Literals.ACTUAL_COMPLETION_TIME,
        help_text=Literals.ACTUAL_COMPLETION_TIME_HELP_TEXT,
    )
    parent_task = models.ForeignKey(
        "self",
        blank=True,
        verbose_name=Literals.SUBTASK_VERBOSE_NAME,
        on_delete=models.SET_NULL,
        related_name="subtasks",
        null=True,
    )
    is_root_task = models.BooleanField(
        default=False,
    )

    class Meta:
        verbose_name = Literals.TASK_VERBOSE_NAME
        verbose_name_plural = Literals.TASK_VERBOSE_NAME_PLURAL

    def get_all_subtasks(self):
        """
        Метод получения всех подзадач конкретной задачи.
        """
        subtasks = list(self.subtasks.all())
        for subtask in self.subtasks.all():
            subtasks.extend(subtask.get_all_subtasks())
        return subtasks

    def save(self, *args, **kwargs):
        """
        Метод сохранения объекта модели TaskModel.

        Переопределяем логику для того, чтобы также переводить в статус
        "Завершена" подзадачи конкретной задачи.
        """
        if self.status == Literals.COMPLETED_INTERNAL:
            self.actual_completion_time = Now()
            for subtask in self.get_all_subtasks():
                subtask.status = Literals.COMPLETED_INTERNAL
                subtask.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
