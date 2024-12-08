import unittest
import sys
import os

# Add the project root directory to sys.path to allow importing from `src`
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from src.core.errors import ValidationError
from src.core.validator import SchemaValidator, NestedValidator
from src.utils.validators import is_required, is_type, is_email

class TestValidator(unittest.TestCase):
    def test_simple_validation(self):
        schema = {
            "name": [is_required, is_type(str)],
            "age": [is_required, is_type(int)],
        }
        data = {"name": "John", "age": 30}
        validator = SchemaValidator(schema)
        self.assertEqual(validator.validate(data), data)

    def test_missing_field(self):
        schema = {"name": [is_required]}
        validator = SchemaValidator(schema)
        with self.assertRaises(Exception):
            validator.validate({})

    def test_invalid_type(self):
        schema = {"age": [is_required, is_type(int)]}
        data = {"age": "thirty"}
        validator = SchemaValidator(schema)
        with self.assertRaises(Exception):
            validator.validate(data)

    def test_email_validation(self):
        schema = {"email": [is_required, is_email]}
        valid_data = {"email": "user@example.com"}
        invalid_data = {"email": "not-an-email"}

        validator = SchemaValidator(schema)
        self.assertEqual(validator.validate(valid_data), valid_data)

        with self.assertRaises(Exception):
            validator.validate(invalid_data)

    def test_nested_validation(self):
        schema = {
            "user": {
                "name": [is_required, is_type(str)],  # Flat validation rules
                "details": {
                    "age": [is_required, is_type(int)],  # Nested schema
                    "email": [is_required, is_email],    # Nested schema
                },
            }
        }

        # Valid Data
        data = {
            "user": {
                "name": "John",
                "details": {
                    "age": 30,
                    "email": "john@example.com"
                }
            }
        }

        # Nested Validator
        nested_validator = NestedValidator(schema)

        # Validate and assert
        self.assertEqual(nested_validator.validate(data), data)

        # Invalid Data
        invalid_data = {
            "user": {
                "name": "John",
                "details": {
                    "age": "thirty",  # Invalid age type
                    "email": "not-an-email"  # Invalid email
                }
            }
        }

        # Validate and assert errors
        with self.assertRaises(ValidationError) as context:
            nested_validator.validate(invalid_data)

        # Check error messages
        self.assertIn("age", str(context.exception))
        self.assertIn("email", str(context.exception))

if __name__ == "__main__":
    unittest.main()
