import unittest
from datetime import datetime
from uuid import UUID
import sys
import os

# Add the project root directory to sys.path to allow importing from `src`
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from src.utils.validators import (
    is_required, is_type, is_in_range, is_email, max_length, min_length,
    matches_regex, is_positive, is_negative, is_integer, is_date,
    is_before_date, is_after_date, is_in_list, has_unique_elements,
    is_uuid, is_url
)
from src.core.errors import ValidationError

class TestValidators(unittest.TestCase):

    # Basic Validators
    def test_is_required(self):
        self.assertIsNone(is_required("test"))  # Valid
        with self.assertRaises(ValidationError):
            is_required(None)  # Invalid

    def test_is_type(self):
        is_type_validator = is_type(str)
        self.assertIsNone(is_type_validator("string"))  # Valid
        with self.assertRaises(ValidationError):
            is_type_validator(123)  # Invalid

    def test_is_in_range(self):
        is_in_range_validator = is_in_range(10, 20)
        self.assertIsNone(is_in_range_validator(15))  # Valid
        with self.assertRaises(ValidationError):
            is_in_range_validator(5)  # Invalid

    def test_is_email(self):
        self.assertIsNone(is_email("test@example.com"))  # Valid
        with self.assertRaises(ValidationError):
            is_email("not-an-email")  # Invalid

    # String Validators
    def test_max_length(self):
        max_length_validator = max_length(5)
        self.assertIsNone(max_length_validator("12345"))  # Valid
        with self.assertRaises(ValidationError):
            max_length_validator("123456")  # Invalid

    def test_min_length(self):
        min_length_validator = min_length(3)
        self.assertIsNone(min_length_validator("abc"))  # Valid
        with self.assertRaises(ValidationError):
            min_length_validator("ab")  # Invalid

    def test_matches_regex(self):
        regex_validator = matches_regex(r"^[a-zA-Z]+$")
        self.assertIsNone(regex_validator("ValidString"))  # Valid
        with self.assertRaises(ValidationError):
            regex_validator("123Invalid")  # Invalid

    # Numerical Validators
    def test_is_positive(self):
        self.assertIsNone(is_positive(5))  # Valid
        with self.assertRaises(ValidationError):
            is_positive(-1)  # Invalid

    def test_is_negative(self):
        self.assertIsNone(is_negative(-5))  # Valid
        with self.assertRaises(ValidationError):
            is_negative(1)  # Invalid

    def test_is_integer(self):
        self.assertIsNone(is_integer(10))  # Valid
        with self.assertRaises(ValidationError):
            is_integer(10.5)  # Invalid

    # Date and Time Validators
    def test_is_date(self):
        is_date_validator = is_date("%Y-%m-%d")
        self.assertIsNone(is_date_validator("2023-12-01"))  # Valid
        with self.assertRaises(ValidationError):
            is_date_validator("01-12-2023")  # Invalid

    def test_is_before_date(self):
        is_before_date_validator = is_before_date("2023-12-01")
        self.assertIsNone(is_before_date_validator("2023-11-30"))  # Valid
        with self.assertRaises(ValidationError):
            is_before_date_validator("2023-12-02")  # Invalid

    def test_is_after_date(self):
        is_after_date_validator = is_after_date("2023-12-01")
        self.assertIsNone(is_after_date_validator("2023-12-02"))  # Valid
        with self.assertRaises(ValidationError):
            is_after_date_validator("2023-11-30")  # Invalid

    # Collection Validators
    def test_is_in_list(self):
        is_in_list_validator = is_in_list(["a", "b", "c"])
        self.assertIsNone(is_in_list_validator("b"))  # Valid
        with self.assertRaises(ValidationError):
            is_in_list_validator("d")  # Invalid

    def test_has_unique_elements(self):
        self.assertIsNone(has_unique_elements([1, 2, 3]))  # Valid
        with self.assertRaises(ValidationError):
            has_unique_elements([1, 2, 2])  # Invalid

    # Advanced Validators
    def test_is_uuid(self):
        self.assertIsNone(is_uuid("550e8400-e29b-41d4-a716-446655440000"))  # Valid
        with self.assertRaises(ValidationError):
            is_uuid("not-a-uuid")  # Invalid

    def test_is_url(self):
        self.assertIsNone(is_url("http://example.com"))  # Valid
        with self.assertRaises(ValidationError):
            is_url("not-a-url")  # Invalid


if __name__ == "__main__":
    unittest.main()
