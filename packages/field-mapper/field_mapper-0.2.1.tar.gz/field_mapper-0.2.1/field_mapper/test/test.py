import unittest
from field_mapper.exc.exception import FieldValidationError, DuplicateDataError
from field_mapper.mapper import FieldMapper, DuplicateDataHandler

class TestFieldMapper(unittest.TestCase):
    def setUp(self):
        self.fields = {
            "name": {"type": str, "max_length": 50, "required_field": True},
            "email": {"type": str, "max_length": 100, "required_field": True},
        }
        self.field_map = {"name": "full_name", "email": "contact_email"}
        self.mapper = FieldMapper(self.fields, self.field_map)

    def test_validate_missing_required_field(self):
        data = {"name": "Alice"}
        with self.assertRaises(FieldValidationError) as context:
            self.mapper.validate(data)

        exc = context.exception
        self.assertEqual(str(exc), "Validation errors occurred")
        self.assertIn("Missing required field: email", exc.issues)
        self.assertEqual(exc.problematic_data, [data])

    def test_validate_field_type_error(self):
        data = {"name": "Alice", "email": 12345}
        with self.assertRaises(FieldValidationError) as context:
            self.mapper.validate(data)

        exc = context.exception
        self.assertIn("Invalid type for field: email", exc.issues)
        self.assertEqual(exc.problematic_data, [data])

    def test_validate_max_length_error(self):
        data = {"name": "A" * 51, "email": "alice@example.com"}
        with self.assertRaises(FieldValidationError) as context:
            self.mapper.validate(data)

        exc = context.exception
        self.assertIn("Field 'name' exceeds max length of 50 characters", exc.issues)
        self.assertEqual(exc.problematic_data, [data])

    def test_map_fields(self):
        data = {"name": "Alice", "email": "alice@example.com"}
        result = self.mapper.map_fields(data)
        expected = {"full_name": "Alice", "contact_email": "alice@example.com"}
        self.assertEqual(result, expected)

    def test_process_with_validation_error(self):
        data = [{"name": "Alice"}]
        result = self.mapper.process(data)
        self.assertEqual(len(result), 0)
        self.assertEqual(len(self.mapper.error), 1)

    # def test_process_with_duplicates(self):
    #     data = [
    #         {"name": "Alice", "email": "alice@example.com"},
    #         {"name": "Alice", "email": "alice@example.com"},
    #     ]
    #     with self.assertRaises(DuplicateDataError) as context:
    #         self.mapper.process(data, skip_duplicate=True)
    #
    #     exc = context.exception
    #     self.assertEqual(str(exc), "Duplicate data detected")
    #     self.assertEqual(len(exc.problematic_data), 1)

class TestDuplicateDataHandler(unittest.TestCase):
    def setUp(self):
        self.handler = DuplicateDataHandler()

    def test_remove_duplicates(self):
        data = [
            {"name": "Alice", "email": "alice@example.com"},
            {"name": "Bob", "email": "bob@example.com"},
            {"name": "Alice", "email": "alice@example.com"},
        ]
        with self.assertRaises(DuplicateDataError) as context:
            self.handler.remove_duplicates(data)

        exc = context.exception
        self.assertEqual(len(exc.problematic_data), 1)
        self.assertEqual(exc.problematic_data[0], {"name": "Alice", "email": "alice@example.com"})

    def test_no_duplicates(self):
        data = [
            {"name": "Alice", "email": "alice@example.com"},
            {"name": "Bob", "email": "bob@example.com"},
        ]
        result = self.handler.remove_duplicates(data)
        self.assertEqual(len(result), 2)
        self.assertEqual(result, data)

if __name__ == "__main__":
    unittest.main()
