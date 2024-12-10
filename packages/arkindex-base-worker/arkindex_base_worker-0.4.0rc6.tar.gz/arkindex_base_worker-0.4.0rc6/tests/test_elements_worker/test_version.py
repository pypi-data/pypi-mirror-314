import pytest

TEST_VERSION_ID = "test_123"
TEST_SLUG = "some_slug"


def test_get_worker_version(fake_dummy_worker):
    api_client = fake_dummy_worker.api_client

    response = {"worker": {"slug": TEST_SLUG}}

    api_client.add_response("RetrieveWorkerVersion", response, id=TEST_VERSION_ID)

    with pytest.deprecated_call(match="WorkerVersion usage is deprecated."):
        res = fake_dummy_worker.get_worker_version(TEST_VERSION_ID)

    assert res == response
    assert fake_dummy_worker._worker_version_cache[TEST_VERSION_ID] == response


def test_get_worker_version__uses_cache(fake_dummy_worker):
    api_client = fake_dummy_worker.api_client

    response = {"worker": {"slug": TEST_SLUG}}

    api_client.add_response("RetrieveWorkerVersion", response, id=TEST_VERSION_ID)

    with pytest.deprecated_call(match="WorkerVersion usage is deprecated."):
        response_1 = fake_dummy_worker.get_worker_version(TEST_VERSION_ID)

    with pytest.deprecated_call(match="WorkerVersion usage is deprecated."):
        response_2 = fake_dummy_worker.get_worker_version(TEST_VERSION_ID)

    assert response_1 == response
    assert response_1 == response_2

    # assert that only one call to the API
    assert len(api_client.history) == 1
    assert not api_client.responses


def test_get_worker_version_slug(mocker, fake_dummy_worker):
    fake_dummy_worker.get_worker_version = mocker.MagicMock()
    fake_dummy_worker.get_worker_version.return_value = {
        "id": TEST_VERSION_ID,
        "worker": {"slug": "mock_slug"},
    }

    with pytest.deprecated_call(match="WorkerVersion usage is deprecated."):
        slug = fake_dummy_worker.get_worker_version_slug(TEST_VERSION_ID)
    assert slug == "mock_slug"


def test_get_worker_version_slug_none(fake_dummy_worker):
    # WARNING: pytest.deprecated_call must be placed BEFORE pytest.raises, otherwise `match` argument won't be checked
    with (
        pytest.deprecated_call(match="WorkerVersion usage is deprecated."),
        pytest.raises(ValueError, match="No worker version ID"),
    ):
        fake_dummy_worker.get_worker_version_slug(None)
