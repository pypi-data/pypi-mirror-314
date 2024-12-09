"""
ElementsWorker methods for entities.
"""

from operator import itemgetter
from typing import TypedDict
from warnings import warn

from peewee import IntegrityError

from arkindex_worker import logger
from arkindex_worker.cache import (
    CachedEntity,
    CachedTranscriptionEntity,
    unsupported_cache,
)
from arkindex_worker.models import Element, Transcription
from arkindex_worker.utils import (
    pluralize,
)


class Entity(TypedDict):
    name: str
    type_id: str
    length: int
    offset: int
    confidence: float | None


class MissingEntityType(Exception):
    """
    Raised when the specified entity type was not found in the corpus and
    the worker cannot create it.
    """


class EntityMixin:
    @unsupported_cache
    def check_required_entity_types(
        self, entity_types: list[str], create_missing: bool = True
    ):
        """Checks that every entity type needed is available in the corpus.
        Missing ones may be created automatically if needed.

        :param entity_types: Entity type names to search.
        :param create_missing: Whether the missing types should be created. Defaults to True.
        :raises MissingEntityType: When an entity type is missing and cannot create.
        """
        # Retrieve entity_type ID
        if not self.entity_types:
            # Load entity_types of corpus
            self.list_corpus_entity_types()

        for entity_type in entity_types:
            # Do nothing if type already exists
            if entity_type in self.entity_types:
                continue

            # Do not create missing if not requested
            if not create_missing:
                raise MissingEntityType(
                    f"Entity type `{entity_type}` was not in the corpus."
                )

            # Create type if non-existent
            self.entity_types[entity_type] = self.api_client.request(
                "CreateEntityType",
                body={
                    "name": entity_type,
                    "corpus": self.corpus_id,
                },
            )["id"]
            logger.info(f"Created a new entity type with name `{entity_type}`.")

    def create_entity(
        self,
        name: str,
        type: str,
        metas=None,
        validated=None,
    ):
        """
        Create an entity on the given corpus.
        If cache support is enabled, a [CachedEntity][arkindex_worker.cache.CachedEntity] will also be created.

        :param name: Name of the entity.
        :param type: Type of the entity.
        """
        assert name and isinstance(
            name, str
        ), "name shouldn't be null and should be of type str"
        assert type and isinstance(
            type, str
        ), "type shouldn't be null and should be of type str"
        metas = metas or {}
        if metas:
            assert isinstance(metas, dict), "metas should be of type dict"
        if validated is not None:
            assert isinstance(validated, bool), "validated should be of type bool"
        if self.is_read_only:
            logger.warning("Cannot create entity as this worker is in read-only mode")
            return

        # Retrieve entity_type ID
        if not self.entity_types:
            # Load entity_types of corpus
            self.list_corpus_entity_types()

        entity_type_id = self.entity_types.get(type)
        assert entity_type_id, f"Entity type `{type}` not found in the corpus."

        entity = self.api_client.request(
            "CreateEntity",
            body={
                "name": name,
                "type_id": entity_type_id,
                "metas": metas,
                "validated": validated,
                "corpus": self.corpus_id,
                "worker_run_id": self.worker_run_id,
            },
        )

        if self.use_cache:
            # Store entity in local cache
            try:
                to_insert = [
                    {
                        "id": entity["id"],
                        "type": type,
                        "name": name,
                        "validated": validated if validated is not None else False,
                        "metas": metas,
                        "worker_run_id": self.worker_run_id,
                    }
                ]
                CachedEntity.insert_many(to_insert).execute()
            except IntegrityError as e:
                logger.warning(f"Couldn't save created entity in local cache: {e}")

        return entity["id"]

    def create_transcription_entity(
        self,
        transcription: Transcription,
        entity: str,
        offset: int,
        length: int,
        confidence: float | None = None,
    ) -> dict[str, str | int] | None:
        """
        Create a link between an existing entity and an existing transcription.
        If cache support is enabled, a `CachedTranscriptionEntity` will also be created.

        :param transcription: Transcription to create the entity on.
        :param entity: UUID of the existing entity.
        :param offset: Starting position of the entity in the transcription's text,
           as a 0-based index.
        :param length: Length of the entity in the transcription's text.
        :param confidence: Optional confidence score between 0 or 1.
        :returns: A dict as returned by the ``CreateTranscriptionEntity`` API endpoint,
           or None if the worker is in read-only mode.
        """
        assert transcription and isinstance(
            transcription, Transcription
        ), "transcription shouldn't be null and should be a Transcription"
        assert entity and isinstance(
            entity, str
        ), "entity shouldn't be null and should be of type str"
        assert (
            offset is not None and isinstance(offset, int) and offset >= 0
        ), "offset shouldn't be null and should be a positive integer"
        assert (
            length is not None and isinstance(length, int) and length > 0
        ), "length shouldn't be null and should be a strictly positive integer"
        assert (
            confidence is None or isinstance(confidence, float) and 0 <= confidence <= 1
        ), "confidence should be null or a float in [0..1] range"
        if self.is_read_only:
            logger.warning(
                "Cannot create transcription entity as this worker is in read-only mode"
            )
            return

        body = {
            "entity": entity,
            "length": length,
            "offset": offset,
            "worker_run_id": self.worker_run_id,
        }
        if confidence is not None:
            body["confidence"] = confidence

        transcription_ent = self.api_client.request(
            "CreateTranscriptionEntity",
            id=transcription.id,
            body=body,
        )

        if self.use_cache:
            # Store transcription entity in local cache
            try:
                CachedTranscriptionEntity.create(
                    transcription=transcription.id,
                    entity=entity,
                    offset=offset,
                    length=length,
                    worker_run_id=self.worker_run_id,
                    confidence=confidence,
                )
            except IntegrityError as e:
                logger.warning(
                    f"Couldn't save created transcription entity in local cache: {e}"
                )
        return transcription_ent

    @unsupported_cache
    def create_transcription_entities(
        self,
        transcription: Transcription,
        entities: list[Entity],
    ) -> list[dict[str, str]]:
        """
        Create multiple entities attached to a transcription in a single API request.

        :param transcription: Transcription to create the entity on.
        :param entities: List of dicts, one per element. Each dict can have the following keys:

            name (str)
               Required. Name of the entity.

            type_id (str)
               Required. ID of the EntityType of the entity.

            length (int)
               Required. Length of the entity in the transcription's text.

            offset (int)
               Required. Starting position of the entity in the transcription's text, as a 0-based index.

            confidence (float or None)
                Optional confidence score, between 0.0 and 1.0.

        :return: List of dicts, with each dict having a two keys, `transcription_entity_id` and `entity_id`, holding the UUID of each created object.
        """
        assert transcription and isinstance(
            transcription, Transcription
        ), "transcription shouldn't be null and should be of type Transcription"

        assert entities and isinstance(
            entities, list
        ), "entities shouldn't be null and should be of type list"

        for index, entity in enumerate(entities):
            assert isinstance(
                entity, dict
            ), f"Entity at index {index} in entities: Should be of type dict"

            name = entity.get("name")
            assert (
                name and isinstance(name, str)
            ), f"Entity at index {index} in entities: name shouldn't be null and should be of type str"

            type_id = entity.get("type_id")
            assert (
                type_id and isinstance(type_id, str)
            ), f"Entity at index {index} in entities: type_id shouldn't be null and should be of type str"

            offset = entity.get("offset")
            assert (
                offset is not None and isinstance(offset, int) and offset >= 0
            ), f"Entity at index {index} in entities: offset shouldn't be null and should be a positive integer"

            length = entity.get("length")
            assert (
                length is not None and isinstance(length, int) and length > 0
            ), f"Entity at index {index} in entities: length shouldn't be null and should be a strictly positive integer"

            confidence = entity.get("confidence")
            assert (
                confidence is None
                or (isinstance(confidence, float) and 0 <= confidence <= 1)
            ), f"Entity at index {index} in entities: confidence should be None or a float in [0..1] range"

        assert len(entities) == len(
            set(map(itemgetter("offset", "length", "name", "type_id"), entities))
        ), "entities should be unique"

        if self.is_read_only:
            logger.warning(
                "Cannot create transcription entities in bulk as this worker is in read-only mode"
            )
            return

        created_entities = self.api_client.request(
            "CreateTranscriptionEntities",
            id=transcription.id,
            body={
                "worker_run_id": self.worker_run_id,
                "entities": entities,
            },
        )["entities"]

        return created_entities

    def list_transcription_entities(
        self,
        transcription: Transcription,
        worker_version: str | bool | None = None,
        worker_run: str | bool | None = None,
    ):
        """
        List existing entities on a transcription
        This method does not support cache

        Warns:
        ----
        The following parameters are **deprecated**:

        - `worker_version` in favor of `worker_run`

        :param transcription: The transcription to list entities on.
        :param worker_version: **Deprecated** Restrict to entities created by a worker version with this UUID. Set to False to look for manually created entities.
        :param worker_run: Restrict to entities created by a worker run with this UUID. Set to False to look for manually created entities.
        """
        query_params = {}
        assert transcription and isinstance(
            transcription, Transcription
        ), "transcription shouldn't be null and should be a Transcription"

        if worker_version is not None:
            warn(
                "`worker_version` usage is deprecated. Consider using `worker_run` instead.",
                DeprecationWarning,
                stacklevel=1,
            )
            assert isinstance(
                worker_version, str | bool
            ), "worker_version should be of type str or bool"

            if isinstance(worker_version, bool):
                assert (
                    worker_version is False
                ), "if of type bool, worker_version can only be set to False"
            query_params["worker_version"] = worker_version
        if worker_run is not None:
            assert isinstance(
                worker_run, str | bool
            ), "worker_run should be of type str or bool"
            if isinstance(worker_run, bool):
                assert (
                    worker_run is False
                ), "if of type bool, worker_run can only be set to False"
            query_params["worker_run"] = worker_run

        return self.api_client.paginate(
            "ListTranscriptionEntities", id=transcription.id, **query_params
        )

    def list_corpus_entities(
        self,
        name: str | None = None,
        parent: Element | None = None,
    ):
        """
        List all entities in the worker's corpus and store them in the ``self.entities`` cache.
        :param name: Filter entities by part of their name (case-insensitive)
        :param parent: Restrict entities to those linked to all transcriptions of an element and all its descendants. Note that links to metadata are ignored.
        """
        query_params = {}

        if name is not None:
            assert name and isinstance(name, str), "name should be of type str"
            query_params["name"] = name

        if parent is not None:
            assert isinstance(parent, Element), "parent should be of type Element"
            query_params["parent"] = parent.id

        self.entities = {
            entity["id"]: entity
            for entity in self.api_client.paginate(
                "ListCorpusEntities", id=self.corpus_id, **query_params
            )
        }
        count = len(self.entities)
        logger.info(
            f'Loaded {count} {pluralize("entity", count)} in corpus ({self.corpus_id})'
        )

    def list_corpus_entity_types(self):
        """
        Loads available entity types in corpus.
        """
        self.entity_types = {
            entity_type["name"]: entity_type["id"]
            for entity_type in self.api_client.paginate(
                "ListCorpusEntityTypes", id=self.corpus_id
            )
        }
        count = len(self.entity_types)
        logger.info(
            f'Loaded {count} entity {pluralize("type", count)} in corpus ({self.corpus_id}).'
        )
