from tasks.models import TaskModel


class TaskMixin:
    """
    Миксин для контроллеров модели TaskModel, объединяющий их общие поля.
    """

    model = TaskModel
    pk_url_kwarg = "task_id"