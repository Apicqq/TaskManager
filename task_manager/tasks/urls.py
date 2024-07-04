from django.urls import path

from tasks.views import (
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskDeleteView,
    TaskUpdateView,
    task_detail,
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
    path(r"ajax/task_data/", task_detail, name="task_data"),
]
