import pytest
from django.db.models.functions import Now


@pytest.fixture
def task():
    from tasks.models import TaskModel
    task = TaskModel.objects.create(
        name="Test task",
        description="Test description",
        performers="Test performer",
        status="Assigned",
        deadline=Now(),
        planned_intensity=3,
        actual_completion_time=3

    )
    return task
