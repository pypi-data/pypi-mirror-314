import unittest
import sys
import os

# Add the project root directory to sys.path to allow importing from `src`
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from src.core.schema_versioning import SchemaVersioning
from src.core.errors import ValidationError
from src.utils.validators import is_required, is_type


class TestSchemaVersioning(unittest.TestCase):
    def setUp(self):
        self.versioning = SchemaVersioning()

        # Define schemas
        self.schema_v1 = {
            "name": [is_required, is_type(str)],
            "age": [is_required, is_type(int)],
        }

        self.schema_v2 = {
            "name": [is_required, is_type(str)],
            "age": [is_required, is_type(int)],
            "email": [is_required, is_type(str)],
        }

        # Register schemas
        self.versioning.register_schema("v1", self.schema_v1)
        self.versioning.register_schema("v2", self.schema_v2)

    def test_register_schema(self):
        self.assertIn("v1", self.versioning.versions)
        self.assertIn("v2", self.versioning.versions)

    def test_register_existing_schema(self):
        with self.assertRaises(ValueError):
            self.versioning.register_schema("v1", self.schema_v1)

    def test_get_schema(self):
        self.assertEqual(self.versioning.get_schema("v1"), self.schema_v1)

    def test_get_nonexistent_schema(self):
        with self.assertRaises(ValueError):
            self.versioning.get_schema("v3")

    def test_validate_with_version_v1(self):
        data = {"name": "John", "age": 30}
        validated_data = self.versioning.validate_with_version("v1", data)
        self.assertEqual(validated_data, data)

    def test_validate_with_version_v2(self):
        data = {"name": "John", "age": 30, "email": "john@example.com"}
        validated_data = self.versioning.validate_with_version("v2", data)
        self.assertEqual(validated_data, data)

    def test_schema_version_not_found(self):
        with self.assertRaises(ValueError):
            self.versioning.validate_with_version("v3", {"name": "John"})

    def test_validation_error(self):
        data = {"name": "John", "email": "john@example.com"}  # Missing age
        with self.assertRaises(ValidationError):
            self.versioning.validate_with_version("v2", data)

    # Migration tests
    def test_add_migration(self):
        def migration(data):
            data["email"] = "default@example.com"
            return data

        self.versioning.add_migration("v1", "v2", migration)
        self.assertIn(("v1", "v2"), self.versioning.migrations)

    def test_migrate_data(self):
        def migration(data):
            data["email"] = "default@example.com"
            return data

        self.versioning.add_migration("v1", "v2", migration)
        data = {"name": "John", "age": 30}
        migrated_data = self.versioning.migrate(data, "v1", "v2")
        self.assertEqual(migrated_data, {"name": "John", "age": 30, "email": "default@example.com"})

    def test_migrate_data_no_migration(self):
        data = {"name": "John", "age": 30}
        with self.assertRaises(ValueError):
            self.versioning.migrate(data, "v1", "v3")

    def test_migrate_data_target_schema_not_registered(self):
        def migration(data):
            data["email"] = "default@example.com"
            return data

        self.versioning.add_migration("v1", "v3", migration)
        data = {"name": "John", "age": 30}
        with self.assertRaises(ValueError):
            self.versioning.migrate(data, "v1", "v3")

if __name__ == "__main__":
    unittest.main()
