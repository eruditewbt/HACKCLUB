class AIPlatformError(Exception):
    pass


class StorageError(AIPlatformError):
    pass


class IngestError(AIPlatformError):
    pass


class QueryError(AIPlatformError):
    pass
