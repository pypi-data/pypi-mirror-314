import json
import re
from uuid import UUID

import pytest
from responses import matchers

from arkindex.exceptions import ErrorResponse
from arkindex_worker.cache import (
    CachedElement,
    CachedEntity,
    CachedTranscription,
    CachedTranscriptionEntity,
)
from arkindex_worker.models import Transcription
from arkindex_worker.worker.transcription import TextOrientation
from tests import CORPUS_ID

from . import BASE_API_CALLS


def test_create_entity_wrong_name(mock_elements_worker):
    with pytest.raises(
        AssertionError, match="name shouldn't be null and should be of type str"
    ):
        mock_elements_worker.create_entity(
            name=None,
            type="person",
        )

    with pytest.raises(
        AssertionError, match="name shouldn't be null and should be of type str"
    ):
        mock_elements_worker.create_entity(
            name=1234,
            type="person",
        )


def test_create_entity_wrong_type(mock_elements_worker):
    with pytest.raises(
        AssertionError, match="type shouldn't be null and should be of type str"
    ):
        mock_elements_worker.create_entity(
            name="Bob Bob",
            type=None,
        )

    with pytest.raises(
        AssertionError, match="type shouldn't be null and should be of type str"
    ):
        mock_elements_worker.create_entity(
            name="Bob Bob",
            type=1234,
        )


def test_create_entity_wrong_corpus(mock_elements_worker):
    # Triggering an error on metas param, not giving corpus should work since
    # ARKINDEX_CORPUS_ID environment variable is set on mock_elements_worker
    with pytest.raises(AssertionError, match="metas should be of type dict"):
        mock_elements_worker.create_entity(
            name="Bob Bob",
            type="person",
            metas="wrong metas",
        )


def test_create_entity_wrong_metas(mock_elements_worker):
    with pytest.raises(AssertionError, match="metas should be of type dict"):
        mock_elements_worker.create_entity(
            name="Bob Bob",
            type="person",
            metas="wrong metas",
        )


def test_create_entity_wrong_validated(mock_elements_worker):
    with pytest.raises(AssertionError, match="validated should be of type bool"):
        mock_elements_worker.create_entity(
            name="Bob Bob",
            type="person",
            validated="wrong validated",
        )


def test_create_entity_api_error(responses, mock_elements_worker):
    # Set one entity type
    mock_elements_worker.entity_types = {"person": "person-entity-type-id"}
    responses.add(
        responses.POST,
        "http://testserver/api/v1/entity/",
        status=418,
    )

    with pytest.raises(ErrorResponse):
        mock_elements_worker.create_entity(
            name="Bob Bob",
            type="person",
        )

    assert len(responses.calls) == len(BASE_API_CALLS) + 1
    assert [
        (call.request.method, call.request.url) for call in responses.calls
    ] == BASE_API_CALLS + [("POST", "http://testserver/api/v1/entity/")]


def test_create_entity(responses, mock_elements_worker):
    # Set one entity type
    mock_elements_worker.entity_types = {"person": "person-entity-type-id"}

    responses.add(
        responses.POST,
        "http://testserver/api/v1/entity/",
        status=200,
        json={"id": "12345678-1234-1234-1234-123456789123"},
    )

    entity_id = mock_elements_worker.create_entity(
        name="Bob Bob",
        type="person",
    )

    assert len(responses.calls) == len(BASE_API_CALLS) + 1
    assert [
        (call.request.method, call.request.url) for call in responses.calls
    ] == BASE_API_CALLS + [
        ("POST", "http://testserver/api/v1/entity/"),
    ]
    assert json.loads(responses.calls[-1].request.body) == {
        "name": "Bob Bob",
        "type_id": "person-entity-type-id",
        "metas": {},
        "validated": None,
        "corpus": CORPUS_ID,
        "worker_run_id": "56785678-5678-5678-5678-567856785678",
    }
    assert entity_id == "12345678-1234-1234-1234-123456789123"


def test_create_entity_missing_type(responses, mock_elements_worker):
    """
    Create entity with an unknown type will fail.
    """
    # Call to list entity types
    responses.add(
        responses.GET,
        f"http://testserver/api/v1/corpus/{CORPUS_ID}/entity-types/",
        status=200,
        json={
            "count": 1,
            "next": None,
            "results": [
                {"id": "person-entity-type-id", "name": "person", "color": "00d1b2"}
            ],
        },
    )

    with pytest.raises(
        AssertionError, match="Entity type `new-entity` not found in the corpus."
    ):
        mock_elements_worker.create_entity(
            name="Bob Bob",
            type="new-entity",
        )

    assert len(responses.calls) == len(BASE_API_CALLS) + 1
    assert [
        (call.request.method, call.request.url) for call in responses.calls
    ] == BASE_API_CALLS + [
        (
            "GET",
            f"http://testserver/api/v1/corpus/{CORPUS_ID}/entity-types/",
        ),
    ]


def test_create_entity_with_cache(responses, mock_elements_worker_with_cache):
    # Set one entity type
    mock_elements_worker_with_cache.entity_types = {"person": "person-entity-type-id"}
    responses.add(
        responses.POST,
        "http://testserver/api/v1/entity/",
        status=200,
        json={"id": "12345678-1234-1234-1234-123456789123"},
    )

    entity_id = mock_elements_worker_with_cache.create_entity(
        name="Bob Bob",
        type="person",
    )

    assert len(responses.calls) == len(BASE_API_CALLS) + 1
    assert [
        (call.request.method, call.request.url) for call in responses.calls
    ] == BASE_API_CALLS + [
        ("POST", "http://testserver/api/v1/entity/"),
    ]

    assert json.loads(responses.calls[-1].request.body) == {
        "name": "Bob Bob",
        "type_id": "person-entity-type-id",
        "metas": {},
        "validated": None,
        "corpus": CORPUS_ID,
        "worker_run_id": "56785678-5678-5678-5678-567856785678",
    }
    assert entity_id == "12345678-1234-1234-1234-123456789123"

    # Check that created entity was properly stored in SQLite cache
    assert list(CachedEntity.select()) == [
        CachedEntity(
            id=UUID("12345678-1234-1234-1234-123456789123"),
            type="person",
            name="Bob Bob",
            validated=False,
            metas={},
            worker_run_id=UUID("56785678-5678-5678-5678-567856785678"),
        )
    ]


def test_create_transcription_entity_wrong_transcription(mock_elements_worker):
    with pytest.raises(
        AssertionError,
        match="transcription shouldn't be null and should be a Transcription",
    ):
        mock_elements_worker.create_transcription_entity(
            transcription=None,
            entity="11111111-1111-1111-1111-111111111111",
            offset=5,
            length=10,
        )

    with pytest.raises(
        AssertionError,
        match="transcription shouldn't be null and should be a Transcription",
    ):
        mock_elements_worker.create_transcription_entity(
            transcription=1234,
            entity="11111111-1111-1111-1111-111111111111",
            offset=5,
            length=10,
        )


def test_create_transcription_entity_wrong_entity(mock_elements_worker):
    with pytest.raises(
        AssertionError, match="entity shouldn't be null and should be of type str"
    ):
        mock_elements_worker.create_transcription_entity(
            transcription=Transcription(
                {
                    "id": "11111111-1111-1111-1111-111111111111",
                    "element": {"id": "myelement"},
                }
            ),
            entity=None,
            offset=5,
            length=10,
        )

    with pytest.raises(
        AssertionError, match="entity shouldn't be null and should be of type str"
    ):
        mock_elements_worker.create_transcription_entity(
            transcription=Transcription(
                {
                    "id": "11111111-1111-1111-1111-111111111111",
                    "element": {"id": "myelement"},
                }
            ),
            entity=1234,
            offset=5,
            length=10,
        )


def test_create_transcription_entity_wrong_offset(mock_elements_worker):
    with pytest.raises(
        AssertionError,
        match="offset shouldn't be null and should be a positive integer",
    ):
        mock_elements_worker.create_transcription_entity(
            transcription=Transcription(
                {
                    "id": "11111111-1111-1111-1111-111111111111",
                    "element": {"id": "myelement"},
                }
            ),
            entity="11111111-1111-1111-1111-111111111111",
            offset=None,
            length=10,
        )

    with pytest.raises(
        AssertionError,
        match="offset shouldn't be null and should be a positive integer",
    ):
        mock_elements_worker.create_transcription_entity(
            transcription=Transcription(
                {
                    "id": "11111111-1111-1111-1111-111111111111",
                    "element": {"id": "myelement"},
                }
            ),
            entity="11111111-1111-1111-1111-111111111111",
            offset="not an int",
            length=10,
        )

    with pytest.raises(
        AssertionError,
        match="offset shouldn't be null and should be a positive integer",
    ):
        mock_elements_worker.create_transcription_entity(
            transcription=Transcription(
                {
                    "id": "11111111-1111-1111-1111-111111111111",
                    "element": {"id": "myelement"},
                }
            ),
            entity="11111111-1111-1111-1111-111111111111",
            offset=-1,
            length=10,
        )


def test_create_transcription_entity_wrong_length(mock_elements_worker):
    with pytest.raises(
        AssertionError,
        match="length shouldn't be null and should be a strictly positive integer",
    ):
        mock_elements_worker.create_transcription_entity(
            transcription=Transcription(
                {
                    "id": "11111111-1111-1111-1111-111111111111",
                    "element": {"id": "myelement"},
                }
            ),
            entity="11111111-1111-1111-1111-111111111111",
            offset=5,
            length=None,
        )

    with pytest.raises(
        AssertionError,
        match="length shouldn't be null and should be a strictly positive integer",
    ):
        mock_elements_worker.create_transcription_entity(
            transcription=Transcription(
                {
                    "id": "11111111-1111-1111-1111-111111111111",
                    "element": {"id": "myelement"},
                }
            ),
            entity="11111111-1111-1111-1111-111111111111",
            offset=5,
            length="not an int",
        )

    with pytest.raises(
        AssertionError,
        match="length shouldn't be null and should be a strictly positive integer",
    ):
        mock_elements_worker.create_transcription_entity(
            transcription=Transcription(
                {
                    "id": "11111111-1111-1111-1111-111111111111",
                    "element": {"id": "myelement"},
                }
            ),
            entity="11111111-1111-1111-1111-111111111111",
            offset=5,
            length=0,
        )


def test_create_transcription_entity_api_error(responses, mock_elements_worker):
    responses.add(
        responses.POST,
        "http://testserver/api/v1/transcription/11111111-1111-1111-1111-111111111111/entity/",
        status=418,
    )

    with pytest.raises(ErrorResponse):
        mock_elements_worker.create_transcription_entity(
            transcription=Transcription(
                {
                    "id": "11111111-1111-1111-1111-111111111111",
                    "element": {"id": "myelement"},
                }
            ),
            entity="11111111-1111-1111-1111-111111111111",
            offset=5,
            length=10,
        )

    assert len(responses.calls) == len(BASE_API_CALLS) + 1
    assert [
        (call.request.method, call.request.url) for call in responses.calls
    ] == BASE_API_CALLS + [
        (
            "POST",
            "http://testserver/api/v1/transcription/11111111-1111-1111-1111-111111111111/entity/",
        )
    ]


def test_create_transcription_entity_no_confidence(responses, mock_elements_worker):
    responses.add(
        responses.POST,
        "http://testserver/api/v1/transcription/11111111-1111-1111-1111-111111111111/entity/",
        status=200,
        json={
            "entity": "11111111-1111-1111-1111-111111111111",
            "offset": 5,
            "length": 10,
        },
    )

    mock_elements_worker.create_transcription_entity(
        transcription=Transcription(
            {
                "id": "11111111-1111-1111-1111-111111111111",
                "element": {"id": "myelement"},
            }
        ),
        entity="11111111-1111-1111-1111-111111111111",
        offset=5,
        length=10,
    )

    assert len(responses.calls) == len(BASE_API_CALLS) + 1
    assert [
        (call.request.method, call.request.url) for call in responses.calls
    ] == BASE_API_CALLS + [
        (
            "POST",
            "http://testserver/api/v1/transcription/11111111-1111-1111-1111-111111111111/entity/",
        ),
    ]
    assert json.loads(responses.calls[-1].request.body) == {
        "entity": "11111111-1111-1111-1111-111111111111",
        "offset": 5,
        "length": 10,
        "worker_run_id": "56785678-5678-5678-5678-567856785678",
    }


def test_create_transcription_entity_with_confidence(responses, mock_elements_worker):
    responses.add(
        responses.POST,
        "http://testserver/api/v1/transcription/11111111-1111-1111-1111-111111111111/entity/",
        status=200,
        json={
            "entity": "11111111-1111-1111-1111-111111111111",
            "offset": 5,
            "length": 10,
            "confidence": 0.33,
        },
    )

    mock_elements_worker.create_transcription_entity(
        transcription=Transcription(
            {
                "id": "11111111-1111-1111-1111-111111111111",
                "element": {"id": "myelement"},
            }
        ),
        entity="11111111-1111-1111-1111-111111111111",
        offset=5,
        length=10,
        confidence=0.33,
    )

    assert len(responses.calls) == len(BASE_API_CALLS) + 1
    assert [
        (call.request.method, call.request.url) for call in responses.calls
    ] == BASE_API_CALLS + [
        (
            "POST",
            "http://testserver/api/v1/transcription/11111111-1111-1111-1111-111111111111/entity/",
        ),
    ]
    assert json.loads(responses.calls[-1].request.body) == {
        "entity": "11111111-1111-1111-1111-111111111111",
        "offset": 5,
        "length": 10,
        "worker_run_id": "56785678-5678-5678-5678-567856785678",
        "confidence": 0.33,
    }


def test_create_transcription_entity_confidence_none(responses, mock_elements_worker):
    responses.add(
        responses.POST,
        "http://testserver/api/v1/transcription/11111111-1111-1111-1111-111111111111/entity/",
        status=200,
        json={
            "entity": "11111111-1111-1111-1111-111111111111",
            "offset": 5,
            "length": 10,
            "confidence": None,
        },
    )

    mock_elements_worker.create_transcription_entity(
        transcription=Transcription(
            {
                "id": "11111111-1111-1111-1111-111111111111",
                "element": {"id": "myelement"},
            }
        ),
        entity="11111111-1111-1111-1111-111111111111",
        offset=5,
        length=10,
        confidence=None,
    )

    assert len(responses.calls) == len(BASE_API_CALLS) + 1
    assert [
        (call.request.method, call.request.url) for call in responses.calls
    ] == BASE_API_CALLS + [
        (
            "POST",
            "http://testserver/api/v1/transcription/11111111-1111-1111-1111-111111111111/entity/",
        ),
    ]
    assert json.loads(responses.calls[-1].request.body) == {
        "entity": "11111111-1111-1111-1111-111111111111",
        "offset": 5,
        "length": 10,
        "worker_run_id": "56785678-5678-5678-5678-567856785678",
    }


def test_create_transcription_entity_with_cache(
    responses, mock_elements_worker_with_cache
):
    CachedElement.create(
        id=UUID("12341234-1234-1234-1234-123412341234"),
        type="page",
    )
    CachedTranscription.create(
        id=UUID("11111111-1111-1111-1111-111111111111"),
        element=UUID("12341234-1234-1234-1234-123412341234"),
        text="Hello, it's me.",
        confidence=0.42,
        orientation=TextOrientation.HorizontalLeftToRight,
        worker_run_id=UUID("56785678-5678-5678-5678-567856785678"),
    )
    CachedEntity.create(
        id=UUID("11111111-1111-1111-1111-111111111111"),
        type="person",
        name="Bob Bob",
        worker_run_id=UUID("56785678-5678-5678-5678-567856785678"),
    )

    responses.add(
        responses.POST,
        "http://testserver/api/v1/transcription/11111111-1111-1111-1111-111111111111/entity/",
        status=200,
        json={
            "entity": "11111111-1111-1111-1111-111111111111",
            "offset": 5,
            "length": 10,
        },
    )

    mock_elements_worker_with_cache.create_transcription_entity(
        transcription=Transcription(
            {
                "id": "11111111-1111-1111-1111-111111111111",
                "element": {"id": "myelement"},
            }
        ),
        entity="11111111-1111-1111-1111-111111111111",
        offset=5,
        length=10,
    )

    assert len(responses.calls) == len(BASE_API_CALLS) + 1
    assert [
        (call.request.method, call.request.url) for call in responses.calls
    ] == BASE_API_CALLS + [
        (
            "POST",
            "http://testserver/api/v1/transcription/11111111-1111-1111-1111-111111111111/entity/",
        ),
    ]
    assert json.loads(responses.calls[-1].request.body) == {
        "entity": "11111111-1111-1111-1111-111111111111",
        "offset": 5,
        "length": 10,
        "worker_run_id": "56785678-5678-5678-5678-567856785678",
    }
    # Check that created transcription entity was properly stored in SQLite cache
    assert list(CachedTranscriptionEntity.select()) == [
        CachedTranscriptionEntity(
            transcription=UUID("11111111-1111-1111-1111-111111111111"),
            entity=UUID("11111111-1111-1111-1111-111111111111"),
            offset=5,
            length=10,
            worker_run_id=UUID("56785678-5678-5678-5678-567856785678"),
        )
    ]


def test_create_transcription_entity_with_confidence_with_cache(
    responses, mock_elements_worker_with_cache
):
    CachedElement.create(
        id=UUID("12341234-1234-1234-1234-123412341234"),
        type="page",
    )
    CachedTranscription.create(
        id=UUID("11111111-1111-1111-1111-111111111111"),
        element=UUID("12341234-1234-1234-1234-123412341234"),
        text="Hello, it's me.",
        confidence=0.42,
        orientation=TextOrientation.HorizontalLeftToRight,
        worker_run_id=UUID("56785678-5678-5678-5678-567856785678"),
    )
    CachedEntity.create(
        id=UUID("11111111-1111-1111-1111-111111111111"),
        type="person",
        name="Bob Bob",
        worker_run_id=UUID("56785678-5678-5678-5678-567856785678"),
    )

    responses.add(
        responses.POST,
        "http://testserver/api/v1/transcription/11111111-1111-1111-1111-111111111111/entity/",
        status=200,
        json={
            "entity": "11111111-1111-1111-1111-111111111111",
            "offset": 5,
            "length": 10,
            "confidence": 0.77,
        },
    )

    mock_elements_worker_with_cache.create_transcription_entity(
        transcription=Transcription(
            {
                "id": "11111111-1111-1111-1111-111111111111",
                "element": {"id": "myelement"},
            }
        ),
        entity="11111111-1111-1111-1111-111111111111",
        offset=5,
        length=10,
        confidence=0.77,
    )

    assert len(responses.calls) == len(BASE_API_CALLS) + 1
    assert [
        (call.request.method, call.request.url) for call in responses.calls
    ] == BASE_API_CALLS + [
        (
            "POST",
            "http://testserver/api/v1/transcription/11111111-1111-1111-1111-111111111111/entity/",
        ),
    ]
    assert json.loads(responses.calls[-1].request.body) == {
        "entity": "11111111-1111-1111-1111-111111111111",
        "offset": 5,
        "length": 10,
        "worker_run_id": "56785678-5678-5678-5678-567856785678",
        "confidence": 0.77,
    }

    # Check that created transcription entity was properly stored in SQLite cache
    assert list(CachedTranscriptionEntity.select()) == [
        CachedTranscriptionEntity(
            transcription=UUID("11111111-1111-1111-1111-111111111111"),
            entity=UUID("11111111-1111-1111-1111-111111111111"),
            offset=5,
            length=10,
            worker_run_id=UUID("56785678-5678-5678-5678-567856785678"),
            confidence=0.77,
        )
    ]


@pytest.mark.parametrize("transcription", [None, "not a transcription", 1])
def test_create_transcription_entities_wrong_transcription(
    mock_elements_worker, transcription
):
    with pytest.raises(
        AssertionError,
        match="transcription shouldn't be null and should be of type Transcription",
    ):
        mock_elements_worker.create_transcription_entities(
            transcription=transcription,
            entities=[],
        )


@pytest.mark.parametrize(
    ("entities", "error"),
    [
        (None, "entities shouldn't be null and should be of type list"),
        (
            "not a list of entities",
            "entities shouldn't be null and should be of type list",
        ),
        (1, "entities shouldn't be null and should be of type list"),
        (
            [
                {
                    "name": "A",
                    "type_id": "12341234-1234-1234-1234-123412341234",
                    "offset": 0,
                    "length": 1,
                    "confidence": 0.5,
                }
            ]
            * 2,
            "entities should be unique",
        ),
    ],
)
def test_create_transcription_entities_wrong_entities(
    mock_elements_worker, entities, error
):
    with pytest.raises(AssertionError, match=error):
        mock_elements_worker.create_transcription_entities(
            transcription=Transcription(id="transcription_id"),
            entities=entities,
        )


def test_create_transcription_entities_wrong_entities_subtype(mock_elements_worker):
    with pytest.raises(
        AssertionError, match="Entity at index 0 in entities: Should be of type dict"
    ):
        mock_elements_worker.create_transcription_entities(
            transcription=Transcription(id="transcription_id"),
            entities=["not a dict"],
        )


@pytest.mark.parametrize(
    ("entity", "error"),
    [
        (
            {
                "name": None,
                "type_id": "12341234-1234-1234-1234-123412341234",
                "offset": 0,
                "length": 1,
                "confidence": 0.5,
            },
            "Entity at index 0 in entities: name shouldn't be null and should be of type str",
        ),
        (
            {"name": "A", "type_id": None, "offset": 0, "length": 1, "confidence": 0.5},
            "Entity at index 0 in entities: type_id shouldn't be null and should be of type str",
        ),
        (
            {"name": "A", "type_id": 0, "offset": 0, "length": 1, "confidence": 0.5},
            "Entity at index 0 in entities: type_id shouldn't be null and should be of type str",
        ),
        (
            {
                "name": "A",
                "type_id": "12341234-1234-1234-1234-123412341234",
                "offset": None,
                "length": 1,
                "confidence": 0.5,
            },
            "Entity at index 0 in entities: offset shouldn't be null and should be a positive integer",
        ),
        (
            {
                "name": "A",
                "type_id": "12341234-1234-1234-1234-123412341234",
                "offset": -2,
                "length": 1,
                "confidence": 0.5,
            },
            "Entity at index 0 in entities: offset shouldn't be null and should be a positive integer",
        ),
        (
            {
                "name": "A",
                "type_id": "12341234-1234-1234-1234-123412341234",
                "offset": 0,
                "length": None,
                "confidence": 0.5,
            },
            "Entity at index 0 in entities: length shouldn't be null and should be a strictly positive integer",
        ),
        (
            {
                "name": "A",
                "type_id": "12341234-1234-1234-1234-123412341234",
                "offset": 0,
                "length": 0,
                "confidence": 0.5,
            },
            "Entity at index 0 in entities: length shouldn't be null and should be a strictly positive integer",
        ),
        (
            {
                "name": "A",
                "type_id": "12341234-1234-1234-1234-123412341234",
                "offset": 0,
                "length": 1,
                "confidence": "not None or a float",
            },
            "Entity at index 0 in entities: confidence should be None or a float in [0..1] range",
        ),
        (
            {
                "name": "A",
                "type_id": "12341234-1234-1234-1234-123412341234",
                "offset": 0,
                "length": 1,
                "confidence": 1.3,
            },
            "Entity at index 0 in entities: confidence should be None or a float in [0..1] range",
        ),
    ],
)
def test_create_transcription_entities_wrong_entity(
    mock_elements_worker, entity, error
):
    with pytest.raises(AssertionError, match=re.escape(error)):
        mock_elements_worker.create_transcription_entities(
            transcription=Transcription(id="transcription_id"),
            entities=[entity],
        )


def test_create_transcription_entities(responses, mock_elements_worker):
    transcription = Transcription(id="transcription-id")

    # Call to Transcription entities creation in bulk
    responses.add(
        responses.POST,
        "http://testserver/api/v1/transcription/transcription-id/entities/bulk/",
        status=201,
        match=[
            matchers.json_params_matcher(
                {
                    "worker_run_id": "56785678-5678-5678-5678-567856785678",
                    "entities": [
                        {
                            "name": "Teklia",
                            "type_id": "22222222-2222-2222-2222-222222222222",
                            "offset": 0,
                            "length": 6,
                            "confidence": 1.0,
                        },
                        {
                            "name": "Team Rocket",
                            "type_id": "22222222-2222-2222-2222-222222222222",
                            "offset": 7,
                            "length": 11,
                            "confidence": 1.0,
                        },
                    ],
                }
            )
        ],
        json={
            "entities": [
                {
                    "transcription_entity_id": "transc-entity-id",
                    "entity_id": "entity-id1",
                },
                {
                    "transcription_entity_id": "transc-entity-id",
                    "entity_id": "entity-id2",
                },
            ]
        },
    )

    # Store entity type/slug correspondence on the worker
    mock_elements_worker.entity_types = {
        "22222222-2222-2222-2222-222222222222": "organization"
    }
    created_objects = mock_elements_worker.create_transcription_entities(
        transcription=transcription,
        entities=[
            {
                "name": "Teklia",
                "type_id": "22222222-2222-2222-2222-222222222222",
                "offset": 0,
                "length": 6,
                "confidence": 1.0,
            },
            {
                "name": "Team Rocket",
                "type_id": "22222222-2222-2222-2222-222222222222",
                "offset": 7,
                "length": 11,
                "confidence": 1.0,
            },
        ],
    )

    assert len(created_objects) == 2

    assert len(responses.calls) == len(BASE_API_CALLS) + 1
    assert [
        (call.request.method, call.request.url) for call in responses.calls
    ] == BASE_API_CALLS + [
        (
            "POST",
            "http://testserver/api/v1/transcription/transcription-id/entities/bulk/",
        )
    ]
