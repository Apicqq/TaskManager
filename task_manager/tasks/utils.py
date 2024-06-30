"""Вспомогательные функции, помогающие реализовать бизнес-логику проекта."""
from typing import Union

from django.db.models import Sum

from core.constants import Literals
from tasks.models import TaskModel, SubTask


def can_set_status_to_completed(task: Union[TaskModel, SubTask]) -> bool:
    """
    Проверка возможности установки статуса "Завершена" для задачи.
    """
    if task.status == Literals.COMPLETED_INTERNAL:
        return True
    elif task.status == Literals.IN_PROGRESS_INTERNAL:
        return all(
            [
                subtask.status in (
                    Literals.IN_PROGRESS_INTERNAL, Literals.COMPLETED_INTERNAL
                ) for
                subtask in task.subtasks.all()
            ]
        )
    else:
        return False


def calculate_task_values(instance: TaskModel) -> None:
    """
    Функция, использующаяся для пересчёта значений полей
    "Плановая трудоёмкость задачи" и "Фактическое время выполнения"
    после удаления/добавления подзадач к задаче.
    """
    if instance.subtasks.exists():
        subtask_sums = instance.subtasks.aggregate(
            planned_intensity=Sum("planned_intensity"),
            actual_completion_time=Sum("actual_completion_time"),
        )
        instance.planned_intensity = (
                subtask_sums["planned_intensity"] + instance.planned_intensity
        )
        instance.actual_completion_time = (
                subtask_sums["actual_completion_time"]
                + instance.actual_completion_time
        )
        instance.save()
    else:
        instance.planned_intensity = 0
        instance.actual_completion_time = 0
        instance.save()
