from typing import List, Dict, Any


class FieldValidationError(Exception):
    """Custom Base exception for field validation errors."""
    def __init__(self, message: str, issues: Any = None, problematic_data: Any = None):
        super().__init__(message)
        self.issues = issues
        self.problematic_data = problematic_data


class DuplicateDataError(FieldValidationError):
    """Custom exception for duplicate data errors."""
    pass


class MissingFieldError(FieldValidationError):
    """Exception raised when required fields are missing."""
    pass


class InvalidTypeError(FieldValidationError):
    """Exception raised when fields have incorrect types."""
    pass


class InvalidLengthError(FieldValidationError):
    """Exception raised when fields exceed the maximum length."""
    pass


class CustomValidationError(FieldValidationError):
    """Exception raised when custom validation fails."""
    pass

