import pytest

from tasks.models import TaskModel, SubTask


@pytest.fixture
def assigned_task_data():
    task = dict(
        name="Test task",
        description="Test description",
        performers="Test performer",
        status="Assigned",
        deadline="2024-05-30",
        planned_intensity=3,
        actual_completion_time=3,
    )
    return task


@pytest.fixture
def in_progress_task_data():
    task = dict(
        name="Test task",
        description="Test description",
        performers="Test performer",
        status="In progress",
        deadline="2024-05-30",
        planned_intensity=3,
        actual_completion_time=3,
    )
    return task

@pytest.fixture
def completed_task_data():
    task = dict(
        name="Test task",
        description="Test description",
        performers="Test performer",
        status="Completed",
        deadline="2024-05-30",
        planned_intensity=3,
        actual_completion_time=3,
    )
    return task

@pytest.fixture
def paused_task_data():
    task = dict(
        name="Test task",
        description="Test description",
        performers="Test performer",
        status="Paused",
        deadline="2024-05-30",
        planned_intensity=3,
        actual_completion_time=3,
    )
    return task


@pytest.fixture
def subtask_data():
    subtask = dict(
        name="Test subtask",
        description="Test description",
        performers="Test performer",
        status="Assigned",
        deadline="2024-05-30",
        planned_intensity=3,
        actual_completion_time=3,
    )
    return subtask


@pytest.fixture
def subtask_create_form_data():
    subtask = {
        "form-TOTAL_FORMS": "1",
        "form-INITIAL_FORMS": "0",
        "form-MIN_NUM_FORMS": "0",
        "form-MAX_NUM_FORMS": "1000",
        "form-0-name": "Test subtask",
        "form-0-description": "Test description",
        "form-0-performers": "Test performer",
        "form-0-status": "Assigned",
        "form-0-deadline": "2024-05-30",
        "form-0-planned_intensity": "3",
        "form-0-actual_completion_time": "3",
        "form-0-id": ""
    }
    return subtask


@pytest.fixture
def subtask_form_update_data():
    subtask = {
        # "name": "Test Task",
        # "description": "Test description",
        # "performers": "Test performer",
        # "deadline": "2024-05-30",
        # "status": "Assigned",
        "subtasks-TOTAL_FORMS": "2",
        "subtasks-INITIAL_FORMS": "1",
        "subtasks-MIN_NUM_FORMS": "0",
        "subtasks-MAX_NUM_FORMS": "1000",
        "subtasks-0-name": "Test subtask",
        "subtasks-0-description": "Test description",
        "subtasks-0-performers": "Test performer",
        "subtasks-0-deadline": "2024-05-30",
        "subtasks-0-status": "In progress",
        "subtasks-0-planned_intensity": "3",
        "subtasks-0-actual_completion_time": "3",
        "subtasks-0-id": "1",
        "subtasks-0-DELETE": "",
        "subtasks-0-task": "1",
        "subtasks-1-name": "",
        "subtasks-1-description": "",
        "subtasks-1-performers": "",
        "subtasks-1-status": "Assigned",
        "subtasks-1-deadline": "",
        "subtasks-1-planned_intensity": "",
        "subtasks-1-actual_completion_time": "",
        "subtasks-1-id": "",
        "subtasks-1-DELETE": "on",
        "subtasks-1-task": "1",
    }
    return subtask


@pytest.fixture
def created_task(assigned_task_data):
    task = TaskModel.objects.create(**assigned_task_data)
    return task


@pytest.fixture
def created_subtask(subtask_data):
    subtask = SubTask.objects.create(**subtask_data, task_id=1)
    return subtask


@pytest.fixture
def task_in_progress(created_task):
    created_task.status = "In progress"
    created_task.save()
    return created_task


@pytest.fixture
def subtask_in_progress(created_subtask):
    created_subtask.status = "In progress"
    created_subtask.save()
    return created_subtask
