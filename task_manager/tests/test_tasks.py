import pytest
from django.urls import reverse

from tasks.models import TaskModel


@pytest.mark.django_db
def test_task_creation(client, assigned_task_data, subtask_create_form_data):
    response = client.post(
        reverse("create_task"), data=dict(
            **assigned_task_data,
            **subtask_create_form_data
        )
    )
    assert response.status_code == 302
    assert TaskModel.objects.count() == 2, (
        "Убедитесь, что задача создаётся корректно."
    )
    first_task = TaskModel.objects.get(pk=1)
    assert TaskModel.objects.get(pk=2).parent_task == first_task


@pytest.mark.django_db
def test_task_detail_view(client, created_task):
    response = client.get(reverse("task_detail", kwargs={"task_id": 1}))
    assert response.status_code == 200, (
        "Убедитесь, что эндпоинт для просмотра данных о задачах доступен."
    )


@pytest.mark.django_db
def test_task_update_valid_data(
        client,
        created_task,
        subtask,
        in_progress_task_data,
        subtask_form_update_data
):
    response = client.post(
        reverse("update_task", kwargs={"task_id": 1}),
        data=dict(
            **in_progress_task_data,
            **subtask_form_update_data
        )
    )
    assert response.status_code == 302, ("Убедитесь, что данные передаются"
                                         "в формы корректно.")


@pytest.mark.django_db
def test_task_update_invalid_data(client, created_task):
    response = client.post(
        reverse("update_task", kwargs={"task_id": 1}),
        data=dict(
            name="Test Task",
            description="Test description",
            performers="Test performer",
            status="Invalid_status",
            deadline="Invalid_date",
        ),
    )
    assert response.status_code == 200, (
        "Код ответа отличается от ожидаемого. Проверьте корректность "
        "логики вашего эндпоинта."
    )
    assert not response.context_data.get("form").is_valid(), (
        "При передаче некорректных данных в форму она не должна быть валидной."
    )
    assert response.context_data.get("form").errors is not None, (
        "При передаче некорректных данных в форму в ответе должно быть"
        "текстовое описание ошибок, в связи с которыми "
        "не была пройдена валидация."
    )


@pytest.mark.django_db
def test_task_cannot_complete_if_not_in_progress(
        client,
        created_task,
        completed_task_data
):
    response = client.post(
        reverse("update_task", kwargs={"task_id": 1}),
        data=dict(**completed_task_data)
    )
    assert response.status_code == 200, (
        "Код ответа отличается от ожидаемого. Проверьте корректность "
        "логики вашего эндпоинта."
    )
    assert response.context_data.get("form").errors.get("status")[0] == (
        "Задача может быть переведена в статус"
        ' "Завершена" только после её принятия в работу'
    ), "Неверное значение для ошибки валидации поля 'status'."


@pytest.mark.django_db
def test_task_cannot_be_paused_until_in_progress(
        client,
        created_task,
        paused_task_data
):
    response = client.post(
        reverse("update_task", kwargs={"task_id": 1}),
        data=dict(**paused_task_data),
    )
    assert response.status_code == 200, (
        "Код ответа отличается от ожидаемого. Проверьте корректность "
        "логики вашего эндпоинта."
    )
    assert response.context_data.get("form").errors.get("status")[0] == (
        'Задача может быть переведена в статус "Приостановлена" '
        "только после её принятия в работу"
    ), "Неверное значение для ошибки валидации поля 'status'."


@pytest.mark.django_db
def test_task_cannot_be_completed_if_any_tasks_not_completed(
        client, task_in_progress, completed_task_data, subtask
):
    response = client.post(
        reverse("update_task", kwargs={"task_id": 1}),
        data=dict(completed_task_data),
    )
    assert response.status_code == 200, (
        "Код ответа отличается от ожидаемого. Проверьте корректность "
        "логики вашего эндпоинта."
    )
    assert not response.context_data.get("form").is_valid(), (
        "Форма не должна проходить валидацию при наличии хотя бы одной"
        "подзадачи, которая не может быть завершена."
    )
    assert response.context_data.get("form").errors.get("status")[0] == (
        'Задача может быть переведена в статус "Завершена" '
        "только после того, как все подзадачи будут выполнены."
    ), "Неверное значение для ошибки валидации поля 'status'."


@pytest.mark.django_db
def test_task_completes_when_all_subtasks_are_able_to_be_finished(
        client,
        task_in_progress,
        subtask_in_progress,
        subtask_form_update_data,
        completed_task_data,
):
    response = client.post(
        reverse("update_task", kwargs={"task_id": 1}),
        data=dict(
            **completed_task_data,
            **subtask_form_update_data,
        ),
    )
    assert response.status_code == 302, (
        "Код ответа отличается от ожидаемого. Проверьте корректность "
        "логики вашего эндпоинта."
    )
    assert TaskModel.objects.first().status == "Completed", (
        "При корректной передаче данных в форму об изменении статуса"
        "задачи на 'Завершено' её статус не изменился. Проверьте логику работы"
        "вашего эндпоинта."
    )


@pytest.mark.django_db
def test_disabled_fields_cannot_be_changed(
        client, created_task
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
    assert response.status_code == 200, (
        "Код ответа отличается от ожидаемого. Проверьте корректность "
        "логики вашего эндпоинта."
    )
    assert (
            TaskModel.objects.first().planned_intensity
            != new_planned_intensity
    ), (
        "Данные в этом поле не подлежат изменению. Пожалуйста, проверьте"
        "корректность работы вашей формы."
    )

    assert (
            TaskModel.objects.first().actual_completion_time
            != new_actual_completion_time
    ), (
        "Данные в этом поле не подлежат изменению. Пожалуйста, проверьте"
        "корректность работы вашей формы."
    )


@pytest.mark.django_db
def test_task_deletion(client, created_task):
    response = client.post(reverse("delete_task", kwargs={"task_id": 1}))
    assert response.status_code == 302, (
        "Код ответа отличается от ожидаемого. Проверьте корректность "
        "логики вашего эндпоинта."
    )
    assert TaskModel.objects.count() == 0, (
        "Убедитесь, что при отправке DELETE-запроса объект задачи удаляется"
        "корректно."
    )
