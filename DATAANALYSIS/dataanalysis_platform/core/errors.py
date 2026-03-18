class DataAnalysisError(Exception):
    """Base error for DATAANALYSIS modules."""


class ValidationError(DataAnalysisError):
    pass


class ProfileError(DataAnalysisError):
    pass
