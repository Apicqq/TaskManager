from django.utils import timezone
import pytest

from tasks.models import TaskModel


@pytest.fixture
def assigned_task_data():
    task = dict(
        name="Test task",
        description="Test description",
        performers="Test performer",
        status="Assigned",
        deadline=timezone.now() + timezone.timedelta(days=1),
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
        deadline=timezone.now() + timezone.timedelta(days=1),
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
        deadline=timezone.now() + timezone.timedelta(days=1),
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
        deadline=timezone.now() + timezone.timedelta(days=1),
        planned_intensity=3,
        actual_completion_time=3,
    )
    return task


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
        "form-0-deadline": timezone.now() + timezone.timedelta(days=1),
        "form-0-planned_intensity": "3",
        "form-0-actual_completion_time": "3",
        "form-0-id": "",
    }
    return subtask


@pytest.fixture
def subtask_form_update_data():
    subtask = {
        "subtasks-TOTAL_FORMS": "2",
        "subtasks-INITIAL_FORMS": "1",
        "subtasks-MIN_NUM_FORMS": "0",
        "subtasks-MAX_NUM_FORMS": "1000",
        "subtasks-0-name": "Test subtask",
        "subtasks-0-description": "Test description",
        "subtasks-0-performers": "Test performer",
        "subtasks-0-deadline": timezone.now() + timezone.timedelta(days=1),
        "subtasks-0-status": "In progress",
        "subtasks-0-planned_intensity": "3",
        "subtasks-0-actual_completion_time": "3",
        "subtasks-0-id": "1",
        "subtasks-0-DELETE": "",
        "subtasks-0-parent_task": "1",
        "subtasks-1-name": "",
        "subtasks-1-description": "",
        "subtasks-1-performers": "",
        "subtasks-1-status": "In progress",
        "subtasks-1-deadline": "",
        "subtasks-1-planned_intensity": "",
        "subtasks-1-actual_completion_time": "",
        "subtasks-1-id": "",
        "subtasks-1-DELETE": "on",
        "subtasks-1-parent_task": "",
    }
    return subtask


@pytest.fixture
def created_task(assigned_task_data):
    task = TaskModel.objects.create(**assigned_task_data)
    return task


@pytest.fixture
def task_in_progress(in_progress_task_data):
    return TaskModel.objects.create(**in_progress_task_data)


@pytest.fixture
def subtask(task_in_progress):
    subtask = TaskModel.objects.create(
        name="Test subtask",
        description="Test description",
        performers="Test performer",
        status="Assigned",
        deadline=timezone.now() + timezone.timedelta(days=1),
        planned_intensity=3,
        actual_completion_time=3,
        parent_task=task_in_progress,
    )
    return subtask


@pytest.fixture
def subtask_in_progress(in_progress_task_data):
    return TaskModel.objects.create(**in_progress_task_data)
