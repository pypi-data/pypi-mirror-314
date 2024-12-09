import pytest
from responses import matchers

from arkindex_worker.models import Transcription
from arkindex_worker.worker.entity import MissingEntityType
from tests import CORPUS_ID

from . import BASE_API_CALLS


def test_check_required_entity_types(responses, mock_elements_worker):
    # Set one entity type
    mock_elements_worker.entity_types = {"person": "person-entity-type-id"}

    checked_types = ["person", "new-entity"]

    # Call to create new entity type
    responses.add(
        responses.POST,
        "http://testserver/api/v1/entity/types/",
        status=200,
        match=[
            matchers.json_params_matcher(
                {
                    "name": "new-entity",
                    "corpus": CORPUS_ID,
                }
            )
        ],
        json={
            "id": "new-entity-id",
            "corpus": CORPUS_ID,
            "name": "new-entity",
            "color": "ffd1b3",
        },
    )

    mock_elements_worker.check_required_entity_types(
        entity_types=checked_types,
    )

    # Make sure the entity_types entry has been updated
    assert mock_elements_worker.entity_types == {
        "person": "person-entity-type-id",
        "new-entity": "new-entity-id",
    }

    assert len(responses.calls) == len(BASE_API_CALLS) + 1
    assert [
        (call.request.method, call.request.url) for call in responses.calls
    ] == BASE_API_CALLS + [
        (
            "POST",
            "http://testserver/api/v1/entity/types/",
        ),
    ]


def test_check_required_entity_types_no_creation_allowed(
    responses, mock_elements_worker
):
    # Set one entity type
    mock_elements_worker.entity_types = {"person": "person-entity-type-id"}

    checked_types = ["person", "new-entity"]

    with pytest.raises(
        MissingEntityType, match="Entity type `new-entity` was not in the corpus."
    ):
        mock_elements_worker.check_required_entity_types(
            entity_types=checked_types, create_missing=False
        )

    assert len(responses.calls) == len(BASE_API_CALLS)
    assert [
        (call.request.method, call.request.url) for call in responses.calls
    ] == BASE_API_CALLS


def test_list_transcription_entities_deprecation(fake_dummy_worker):
    transcription = Transcription({"id": "fake_transcription_id"})
    worker_version = "worker_version_id"
    fake_dummy_worker.api_client.add_response(
        "ListTranscriptionEntities",
        id=transcription.id,
        worker_version=worker_version,
        response={"id": "entity_id"},
    )
    with pytest.deprecated_call(
        match="`worker_version` usage is deprecated. Consider using `worker_run` instead."
    ):
        assert fake_dummy_worker.list_transcription_entities(
            transcription, worker_version=worker_version
        ) == {"id": "entity_id"}

    assert len(fake_dummy_worker.api_client.history) == 1
    assert len(fake_dummy_worker.api_client.responses) == 0


def test_list_transcription_entities(fake_dummy_worker):
    transcription = Transcription({"id": "fake_transcription_id"})
    worker_run = "worker_run_id"
    fake_dummy_worker.api_client.add_response(
        "ListTranscriptionEntities",
        id=transcription.id,
        worker_run=worker_run,
        response={"id": "entity_id"},
    )
    assert fake_dummy_worker.list_transcription_entities(
        transcription, worker_run=worker_run
    ) == {"id": "entity_id"}

    assert len(fake_dummy_worker.api_client.history) == 1
    assert len(fake_dummy_worker.api_client.responses) == 0


def test_list_corpus_entities(responses, mock_elements_worker):
    responses.add(
        responses.GET,
        f"http://testserver/api/v1/corpus/{CORPUS_ID}/entities/",
        json={
            "count": 1,
            "next": None,
            "results": [
                {
                    "id": "fake_entity_id",
                }
            ],
        },
    )

    mock_elements_worker.list_corpus_entities()

    assert mock_elements_worker.entities == {
        "fake_entity_id": {
            "id": "fake_entity_id",
        }
    }

    assert len(responses.calls) == len(BASE_API_CALLS) + 1
    assert [
        (call.request.method, call.request.url) for call in responses.calls
    ] == BASE_API_CALLS + [
        (
            "GET",
            f"http://testserver/api/v1/corpus/{CORPUS_ID}/entities/",
        ),
    ]


@pytest.mark.parametrize("wrong_name", [1234, 12.5])
def test_list_corpus_entities_wrong_name(mock_elements_worker, wrong_name):
    with pytest.raises(AssertionError, match="name should be of type str"):
        mock_elements_worker.list_corpus_entities(name=wrong_name)


@pytest.mark.parametrize("wrong_parent", [{"id": "element_id"}, 12.5, "blabla"])
def test_list_corpus_entities_wrong_parent(mock_elements_worker, wrong_parent):
    with pytest.raises(AssertionError, match="parent should be of type Element"):
        mock_elements_worker.list_corpus_entities(parent=wrong_parent)
