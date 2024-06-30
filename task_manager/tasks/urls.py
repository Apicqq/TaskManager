from django.urls import path

from tasks.views import (
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskDeleteView,
    SubTaskDetailView,
    TaskUpdateView,
    SubTaskDeleteView,
    SubTaskUpdateView,
    task_detail, subtask_detail,
)

urlpatterns = [
    path("", TaskListView.as_view(), name="task_list"),
    path("create_task/", TaskCreateView.as_view(), name="create_task"),
    path("tasks/<int:task_id>/", TaskDetailView.as_view(), name="task_detail"),
    path(
        "tasks/<int:task_id>/delete_task/",
        TaskDeleteView.as_view(),
        name="delete_task",
    ),
    path(
        "tasks/<int:task_id>/update_task/",
        TaskUpdateView.as_view(),
        name="update_task",
    ),
    path(
        "tasks/<int:task_id>/subtasks/<int:subtask_id>/",
        SubTaskDetailView.as_view(),
        name="subtask_detail",
    ),
    path(
        "tasks/<int:task_id>/subtasks/<int:subtask_id>/update/",
        SubTaskUpdateView.as_view(),
        name="update_subtask",
    ),
    path(
        "tasks/<int:task_id>/subtasks/<int:subtask_id>/delete_subtask/",
        SubTaskDeleteView.as_view(),
        name="delete_subtask",
    ),
    path(r"ajax/task_data/", task_detail, name="task_data"),
    path(r"ajax/subtask_data", subtask_detail, name="subtask_data")
]
