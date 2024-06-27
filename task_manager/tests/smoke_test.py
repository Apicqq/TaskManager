import pytest
from tests.url_schemas import TASK_GET_URLS, TASK_POST_URLS, SUBTASK_GET_URLS, SUBTASK_POST_URLS
@pytest.mark.django_db
def test_task_get_urls(client, task):
    for url in TASK_GET_URLS:
        response = client.get(url)
        assert response.status_code == 200


@pytest.mark.django_db
def test_task_post_urls(client, task):
    for url in TASK_POST_URLS:
        response = client.post(url)
        assert response.status_code == 200