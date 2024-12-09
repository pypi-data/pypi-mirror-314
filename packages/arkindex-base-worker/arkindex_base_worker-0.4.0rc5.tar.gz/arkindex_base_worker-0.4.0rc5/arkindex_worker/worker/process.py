from enum import Enum


class ActivityState(Enum):
    """
    Processing state of an element.
    """

    Queued = "queued"
    """
    The element has not yet been processed by a worker.
    """

    Started = "started"
    """
    The element is being processed by a worker.
    """

    Processed = "processed"
    """
    The element has been successfully processed by a worker.
    """

    Error = "error"
    """
    An error occurred while processing this element.
    """


class ProcessMode(Enum):
    """
    Mode of the process of the worker.
    """

    Files = "files"
    """
    Processes of files (images, PDFs, IIIF, ...) imports.
    """

    Workers = "workers"
    """
    Processes of worker executions.
    """

    Template = "template"
    """
    Process templates.
    """

    S3 = "s3"
    """
    Processes of imports from an S3-compatible storage.
    """

    Local = "local"
    """
    Local processes.
    """

    Dataset = "dataset"
    """
    Dataset processes.
    """

    Export = "export"
    """
    Export processes.
    """
