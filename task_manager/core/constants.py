from enum import StrEnum, IntEnum


class Errors(StrEnum):
    TASK_CANNOT_BE_COMPLETED_UNTIL_IN_PROGRESS = (
        'Задача может быть переведена в статус "Завершена" '
        "только после её принятия в работу"

    )
    TASK_CANNOT_BE_PAUSED_UNTIL_IN_PROGRESS = (
        'Задача может быть переведена в статус "Приостановлена" '
        "только после её принятия в работу"

    )
    TASK_CANNOT_BE_COMPLETED_UNTIL_ALL_SUBTASKS_ARE_DONE = (
        'Задача может быть переведена в статус "Завершена" '
        "только после того, как все подзадачи будут выполнены."

    )


class Values(IntEnum):
    FORMSETS_EXTRA_FORMS = 1
    NAME_MAX_LENGTH = 100


class Literals(StrEnum):
    ASSIGNED_INTERNAL = "Assigned"
    ASSIGNED_RU = "Назначена"
    IN_PROGRESS_INTERNAL = "In progress"
    IN_PROGRESS_RU = "Выполняется"
    PAUSED_INTERNAL = "Paused"
    PAUSED_RU = "Приостановлена"
    COMPLETED_INTERNAL = "Completed"
    COMPLETED_RU = "Завершена"
    TASK_NAME = "Название задачи"
    TASK_VERBOSE_NAME = "Задача"
    TASK_VERBOSE_NAME_PLURAL = "Задачи"
    SUBTASK_NAME = "Название подзадачи"
    SUBTASK_VERBOSE_NAME = "Подзадача"
    SUBTASK_VERBOSE_NAME_PLURAL = "Подзадачи"
    DESCRIPTION = "Описание задачи"
    PERFORMERS = "Исполнители"
    CREATED_AT = "Дата регистрации задачи"
    STATUS = "Статус задачи"
    PLANNED_INTENSITY = "Планируемая интенсивность"
    DEADLINE = "Дата завершения задачи"
    ACTUAL_COMPLETION_TIME = "Фактическое время выполнения"
    ACTUAL_COMPLETION_TIME_HELP_TEXT = "В часах"


TASK_STATUSES = (
    (Literals.ASSIGNED_INTERNAL, Literals.ASSIGNED_RU),
    (Literals.IN_PROGRESS_INTERNAL, Literals.IN_PROGRESS_RU),
    (Literals.PAUSED_INTERNAL, Literals.PAUSED_RU),
    (Literals.COMPLETED_INTERNAL, Literals.COMPLETED_RU),
)
