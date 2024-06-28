TASK_GET_URLS = [
    "/",
    "/tasks/1/",
]
TASK_POST_URLS = [
    "/create_task/",
    "/tasks/1/update_task/",
    "/tasks/1/delete_task/",
]
SUBTASK_GET_URLS = [
    "/task/<int:task_id>/subtasks/",
    "/task/<int:task_id>/subtasks/<int:subtask_id>/",
]
SUBTASK_POST_URLS = [
    "/task/<int:task_id>/subtasks/create_subtask/",
    "/task/<int:task_id>/subtasks/<int:subtask_id>/update/",
    "/task/<int:task_id>/subtasks/<int:subtask_id>/delete/",
]