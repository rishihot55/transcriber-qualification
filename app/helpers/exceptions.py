class UniqueConstraintError(Exception):
    """Exception thrown when an unique constraint fails."""


class StoreError(Exception):
    """Raise an error when the data is unable to be stored on file."""
