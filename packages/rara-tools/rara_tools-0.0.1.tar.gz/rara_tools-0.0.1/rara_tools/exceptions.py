class S3InputException(Exception):
    """Raised S3 input error."""

class S3InitException(Exception):
    """Raised S3 Error."""

class S3ConnectionException(Exception):
    """Raised S3 Bucket/Connection Error."""

class ElasticsearchException(Exception):
    """Raised Elasticsearch Error."""

class TaskReporterException(Exception):
    """Raised TaskReporter Error."""
