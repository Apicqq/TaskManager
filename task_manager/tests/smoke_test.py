import pytest

from tests.url_schemas import (
    TASK_GET_URLS,
    TASK_POST_URLS,
    SUBTASK_GET_URLS,
    SUBTASK_POST_URLS
)


@pytest.mark.django_db
def test_task_get_urls(client, created_task):
    for url in TASK_GET_URLS:
        response = client.get(url)
        assert response.status_code == 200, (
            f"Убедитесь, что эндпоинт {url} доступен."
        )


@pytest.mark.django_db
def test_task_post_urls(client, created_task):
    for url in TASK_POST_URLS:
        response = client.get(url)
        assert response.status_code == 200, (
            f"Убедитесь, что эндпоинт {url} доступен."
        )


@pytest.mark.django_db
def test_subtask_get_urls(client, created_task, created_subtask):
    for url in SUBTASK_GET_URLS:
        response = client.get(url)
        assert response.status_code == 200, (
            f"Убедитесь, что эндпоинт {url} доступен."
        )

@pytest.mark.django_db
def test_subtask_post_urls(client, created_task, created_subtask):
    for url in SUBTASK_POST_URLS:
        response = client.get(url)
        assert response.status_code == 200, (
            f"Убедитесь, что эндпоинт {url} доступен."
        )
