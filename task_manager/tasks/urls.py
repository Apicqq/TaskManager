from django.urls import path

from tasks.views import (
    TaskListView, TaskDetailView, TaskCreateView, TaskDeleteView, SubTaskDetailView,
    TaskUpdateView, SubTaskCreateView, SubTaskDeleteView, SubTaskUpdateView,
add_task
)

urlpatterns = [
    path(
        "",
        TaskListView.as_view(),
        name="task_list"
    ),
    path(
        "create_task/",
        TaskCreateView.as_view(),
        name="create_task"
    ),
    path(
        "<int:task_id>/",
        TaskDetailView.as_view(),
        name="task_detail"
    ),
    path(
        "<int:task_id>/delete/",
        TaskDeleteView.as_view(),
        name="delete_task"
    ),
    path(
        "<int:task_id>/update_task/",
        TaskUpdateView.as_view(),
        name="update_task"
    ),
    path(
        "<int:task_id>/create_subtask/",
        SubTaskCreateView.as_view(),
        name="create_subtask"
    ),
    path(
        "<int:task_id>/subtasks/<int:subtask_id>/",
        SubTaskDetailView.as_view(),
        name="subtask_detail"
    ),
    path(
        "<int:task_id>/subtasks/<int:subtask_id>/update/",
        SubTaskUpdateView.as_view(),
        name="update_subtask"
    ),
    path(
        "<int:task_id>/subtasks/<int:subtask_id>/delete/",
        SubTaskDeleteView.as_view(),
        name="delete_subtask"
    ),
    path("add_subtask/", add_task, name="add_subtask"),
]
