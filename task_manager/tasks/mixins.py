from tasks.models import TaskModel, SubTask


class TaskMixin:
    """
    Миксин для контроллеров модели TaskModel, объединяющий их общие поля.
    """

    model = TaskModel
    pk_url_kwarg = "task_id"


class SubTaskMixin:
    """
    Миксин для контроллеров модели SubTask, объединяющий их общие поля.
    """
    model = SubTask
    pk_url_kwarg = "subtask_id"
