"""
ElementsWorker methods for worker versions.
"""

import functools
from warnings import warn


def worker_version_deprecation(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        warn("WorkerVersion usage is deprecated.", DeprecationWarning, stacklevel=2)
        return func(self, *args, **kwargs)

    return wrapper


class WorkerVersionMixin:
    @worker_version_deprecation
    def get_worker_version(self, worker_version_id: str) -> dict:
        """
        Warns:
        ----
        This method is **deprecated**.

        Retrieve a worker version, using the [ElementsWorker][arkindex_worker.worker.ElementsWorker]'s internal cache when possible.

        :param worker_version_id: ID of the worker version to retrieve.
        :returns: The requested worker version, as returned by the ``RetrieveWorkerVersion`` API endpoint.
        """
        if worker_version_id is None:
            raise ValueError("No worker version ID")

        if worker_version_id in self._worker_version_cache:
            return self._worker_version_cache[worker_version_id]

        worker_version = self.api_client.request(
            "RetrieveWorkerVersion", id=worker_version_id
        )
        self._worker_version_cache[worker_version_id] = worker_version

        return worker_version

    @worker_version_deprecation
    def get_worker_version_slug(self, worker_version_id: str) -> str:
        """
        Warns:
        ----
        This method is **deprecated**.

        Retrieve the slug of the worker of a worker version, from a worker version UUID.
        Uses a worker version from the internal cache if possible, otherwise makes an API request.

        :param worker_version_id: ID of the worker version to find a slug for.
        :returns: Slug of the worker of this worker version.
        """
        worker_version = self.get_worker_version(worker_version_id)
        return worker_version["worker"]["slug"]
