import pytest
from django.urls import reverse

from tasks.models import TaskModel, SubTask


@pytest.mark.django_db
def test_task_creation(client, task_data, subtask_form_data):
    response = client.post(
        reverse("create_task"), data=dict(**task_data, **subtask_form_data)
    )
    assert response.status_code == 302
    assert TaskModel.objects.count() == 1, (
        "Убедитесь," " что задача создаётся корректно"
    )
    assert SubTask.objects.count() == 1, (
        "(Убедитесь," " что подзадача создаётся корректно"
    )


@pytest.mark.django_db
def test_task_detail_view(client, created_task):
    response = client.get(reverse("task_detail", kwargs={"task_id": 1}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_task_update_valid_data(client, created_task):
    response = client.post(
        reverse("update_task", kwargs={"task_id": 1}),
        data=dict(
            name="Test task",
            description="Test description",
            performers="Test performer",
            status="Assigned",
            deadline="2024-05-30",
        ),
    )
    assert response.status_code == 200
    assert TaskModel.objects.count() == 1
    assert response.context_data.get("form").is_valid()
    assert not response.context_data.get("formset").is_valid()


@pytest.mark.django_db
def test_task_update_invalid_data(client, created_task):
    response = client.post(
        reverse("update_task", kwargs={"task_id": 1}),
        data=dict(
            name=13,
            description="Test description",
            performers="Test performer",
            status="Invalid_status",
            deadline="Invalid_date",
        ),
    )
    assert response.status_code == 200
    assert not response.context_data.get("form").is_valid()
    assert response.context_data.get("form").errors is not None


@pytest.mark.django_db
def test_task_update_completes_when_in_progress(client, task_in_progress):
    response = client.post(
        reverse("update_task", kwargs={"task_id": 1}),
        data=dict(
            name="Test Task",
            description="Test description",
            performers="Test performer",
            status="Completed",
            deadline="2024-05-30",
        ),
    )
    assert response.status_code == 200
    assert response.context_data.get("form").is_valid()


@pytest.mark.django_db
def test_task_cannot_complete_if_not_in_progress(client, created_task):
    response = client.post(
        reverse("update_task", kwargs={"task_id": 1}),
        data=dict(
            name="Test Task",
            description="Test description",
            performers="Test performer",
            status="Completed",
            deadline="2024-05-30",
        ),
    )
    assert response.status_code == 200
    assert response.context_data.get("form").errors.get("status")[0] == (
        "Задача может быть переведена в статус"
        ' "Завершена" только после её принятия в работу'
    )


@pytest.mark.django_db
def test_task_cannot_be_paused_until_in_progress(client, created_task):
    response = client.post(
        reverse("update_task", kwargs={"task_id": 1}),
        data=dict(
            name="Test Task",
            description="Test description",
            performers="Test performer",
            status="Paused",
            deadline="2024-05-30",
        ),
    )
    assert response.status_code == 200
    assert response.context_data.get("form").errors.get("status")[0] == (
        'Задача может быть переведена в статус "Приостановлена" '
        "только после её принятия в работу"
    )


@pytest.mark.django_db
def test_task_cannot_be_completed_if_any_tasks_not_completed(
    client, task_in_progress, created_subtask
):
    response = client.post(
        reverse("update_task", kwargs={"task_id": 1}),
        data=dict(
            name="Test Task",
            description="Test description",
            performers="Test performer",
            status="Completed",
            deadline="2024-05-30",
        ),
    )
    assert response.status_code == 200
    assert not response.context_data.get("form").is_valid()
    assert response.context_data.get("form").errors.get("status")[0] == (
        'Задача может быть переведена в статус "Завершена" '
        "только после того, как все подзадачи будут выполнены."
    )


@pytest.mark.django_db
def test_disabled_fields_cannot_be_changed(
    client, created_task, created_subtask
):
    new_planned_intensity = 100
    new_actual_completion_time = 350
    response = client.post(
        reverse("update_task", kwargs={"task_id": 1}),
        data=dict(
            name="Test Task",
            description="Test description",
            performers="Test performer",
            status="Assigned",
            deadline="2024-05-30",
            subtasks=1,
            planned_intensity=new_planned_intensity,
            actual_completion_time=new_actual_completion_time,
        ),
    )
    assert response.status_code == 200
    assert created_task.planned_intensity != new_planned_intensity
    assert created_task.actual_completion_time != new_actual_completion_time


@pytest.mark.django_db
def test_task_deletion(client, created_task):
    response = client.post(reverse("delete_task", kwargs={"task_id": 1}))
    assert response.status_code == 302
    assert TaskModel.objects.count() == 0
