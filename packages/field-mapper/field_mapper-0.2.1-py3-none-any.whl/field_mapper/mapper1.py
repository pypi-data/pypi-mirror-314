from typing import List, Dict, Any, Callable, Union, Type


class FieldValidationError(Exception):
    """Custom exception for field validation errors."""
    def __init__(self, message: str, issues: List[str], problematic_data: Any):
        super().__init__(message)
        self.issues = issues
        self.problematic_data = problematic_data


class DuplicateDataError(Exception):
    """Custom exception for duplicate data errors."""
    def __init__(self, message: str, issues: List[str], problematic_data: Any):
        super().__init__(message)
        self.issues = issues
        self.problematic_data = problematic_data


class FieldMapper:
    def __init__(self, fields: Dict[str, Dict[str, Union[Type, int, Callable, bool]]], field_map: Dict[str, str]):
        self.fields = fields
        self.field_map = field_map
        self.errors = []

    def validate_fields(self, data: Dict[str, Any]) -> None:
        """
        Validate fields in a single data dictionary based on the defined rules in `fields`.
        """
        errors = []
        for field_name, constraints in self.fields.items():
            value = self._extract_nested_value(data, constraints.get("position"))
            is_required_field = constraints.get("required_field", True)
            is_required_value = constraints.get("required_value", True)
            expected_type = constraints.get("type")
            max_length = constraints.get("max_length")
            custom_validator = constraints.get("custom")

            # Field presence validation
            if is_required_field and value is None:
                errors.append(f"Missing required field: {field_name}")
                continue

            # Value presence validation
            if is_required_value and not value and value != 0:
                errors.append(f"Missing required value for field: {field_name}")

            # Type validation
            if value is not None and expected_type and not isinstance(value, expected_type):
                errors.append(f"Invalid type for field '{field_name}': Expected {expected_type}, got {type(value)}")

            # Length validation
            if value is not None and max_length and isinstance(value, str) and len(value) > max_length:
                errors.append(f"Field '{field_name}' exceeds maximum length of {max_length} characters")

            # Custom validation
            if value is not None and custom_validator and callable(custom_validator):
                try:
                    if not custom_validator(value):
                        errors.append(f"Custom validation failed for field: {field_name}")
                except Exception as e:
                    errors.append(f"Error during custom validation for field '{field_name}': {str(e)}")

        if errors:
            raise FieldValidationError("Validation errors occurred", errors, data)

    def map_fields(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map the extracted fields to their target field names based on `field_map`.
        """
        mapped_data = {}
        for source_field, target_field in self.field_map.items():
            extracted_value = self._extract_nested_value(data, source_field)
            mapped_data[target_field] = extracted_value
        return mapped_data

    def process_data(self, data: List[Dict[str, Any]], skip_duplicates: bool = False) -> List[Dict[str, Any]]:
        """
        Process a list of data dictionaries, performing validation and field mapping.
        Optionally removes duplicates if `skip_duplicates` is True.
        """
        if not isinstance(data, list):
            raise ValueError("Input data must be a list of dictionaries.")

        if skip_duplicates:
            data = self._remove_duplicates(data)

        processed_data = []
        for entry in data:
            try:
                self.validate_fields(entry)
                mapped_entry = self.map_fields(entry)
                processed_data.append(mapped_entry)
            except FieldValidationError as exc:
                self._log_error(exc)

        return processed_data

    def _extract_nested_value(self, data: Dict[str, Any], position: str) -> Any:
        """
        Extract a value from a nested dictionary or list using dot notation.
        Supports dynamic lists with `[]`.
        """
        keys = position.split('.')
        value = data

        for key in keys:
            if '[' in key and ']' in key:  # Handle indexed or dynamic lists
                base_key, index = key[:-1].split('[')
                value = value.get(base_key, [])
                if index == '':  # Dynamic list extraction
                    continue
                value = value[int(index)] if len(value) > int(index) else None
            else:
                if isinstance(value, list):  # Handle dynamic lists
                    value = [item.get(key) for item in value if isinstance(item, dict)]
                else:
                    value = value.get(key) if isinstance(value, dict) else None

            if value is None:
                break

        return value

    def _remove_duplicates(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Remove duplicate entries from the input data.
        """
        seen_hashes = set()
        unique_data = []
        duplicate_entries = []

        for entry in data:
            entry_hashable = self._make_hashable(entry)
            if entry_hashable in seen_hashes:
                duplicate_entries.append(entry)
            else:
                seen_hashes.add(entry_hashable)
                unique_data.append(entry)

        if duplicate_entries:
            raise DuplicateDataError("Duplicate data detected", ["Duplicate entries found"], duplicate_entries)

        return unique_data

    def _make_hashable(self, obj: Any) -> Any:
        """
        Convert mutable structures into hashable ones for deduplication purposes.
        """
        if isinstance(obj, dict):
            return frozenset((key, self._make_hashable(value)) for key, value in obj.items())
        elif isinstance(obj, list):
            return tuple(self._make_hashable(item) for item in obj)
        return obj

    def _log_error(self, exc: FieldValidationError) -> None:
        """
        Log validation errors for debugging and tracking.
        """
        formatted_error = (
            f"Validation Error:\n"
            f"Issues: {', '.join(exc.issues)}\n"
            f"Problematic Data: {exc.problematic_data}"
        )
        self.errors.append(formatted_error)
        print(formatted_error)
