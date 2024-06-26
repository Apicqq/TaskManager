from enum import Enum, auto

TASK_STATUSES = (
    ("Assigned", "Назначена"),
    ("In progress", "Выполняется"),
    ("Paused", "Приостановлена"),
    ("Completed", "Завершена"),
)


class Literals(Enum):
    COMPLETED = auto()
    IN_PROGRESS = auto()
    PAUSED = auto()
    ASSIGNED = auto()
