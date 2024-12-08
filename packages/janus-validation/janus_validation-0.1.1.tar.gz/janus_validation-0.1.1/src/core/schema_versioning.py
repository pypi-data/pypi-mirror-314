from .validator import SchemaValidator

class SchemaVersioning:
    """Handles schema versioning for API compatibility and migrations."""
    def __init__(self):
        self.versions = {}
        self.migrations = {}

    def register_schema(self, version, schema):
        if version in self.versions:
            raise ValueError(f"Schema version {version} already exists.")
        self.versions[version] = schema

    def add_migration(self, from_version, to_version, migration_function):
        self.migrations[(from_version, to_version)] = migration_function

    def migrate(self, data, from_version, to_version):
        # Check if the target schema is registered
        if to_version not in self.versions:
            raise ValueError(f"Target schema version '{to_version}' is not registered.")
        # Check if the migration is registered
        if (from_version, to_version) not in self.migrations:
            raise ValueError(f"No migration registered from {from_version} to {to_version}.")
        # Perform the migration
        return self.migrations[(from_version, to_version)](data)

    def get_schema(self, version):
        if version not in self.versions:
            raise ValueError(f"Schema version {version} not found.")
        return self.versions[version]

    def validate_with_version(self, version, data):
        schema = self.get_schema(version)
        validator = SchemaValidator(schema)
        return validator.validate(data)
