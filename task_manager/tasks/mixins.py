from tasks.models import TaskModel, SubTask


class TaskMixin:
    model = TaskModel
    pk_url_kwarg = "task_id"


class SubTaskMixin:
    model = SubTask
    pk_url_kwarg = "subtask_id"
