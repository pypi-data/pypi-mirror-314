class ValidationError(Exception):
    """Raised when data validation fails."""
    def __init__(self, message, field=None):
        super().__init__(message)
        self.message = message
        self.field = field


class SerializationError(Exception):
    """Raised when serialization/deserialization fails."""
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class SchemaVersionError(Exception):
    """Raised when schema versioning fails."""
    def __init__(self, message):
        super().__init__(message)
        self.message = message
