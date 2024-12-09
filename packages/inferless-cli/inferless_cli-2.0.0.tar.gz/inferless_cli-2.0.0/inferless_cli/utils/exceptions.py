class InferlessCLIError(Exception):
    """Base class for exceptions in this module."""


class ServerError(InferlessCLIError):
    """Exception raised for server errors."""


class ConfigurationError(InferlessCLIError):
    """Exception raised for configuration errors."""


class ModelImportException(Exception):
    """Exception raised for model import not found errors."""


class TritonError(Exception):
    """Exception raised for Triton errors."""


class VersionNotStringTomlFileError(Exception):
    """Exception raised for version not string in toml file."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)