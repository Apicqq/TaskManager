TASK_GET_URLS = [
    "/",
    "/1/",
]
TASK_POST_URLS = [
    "/create_task/",
    "/task/<int:task_id>/update_task/",
    "/task/<int:task_id>/delete/",
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