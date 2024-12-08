from .errors import ValidationError

class BaseValidator:
    """Abstract class for all validators."""
    def validate(self, data):
        raise NotImplementedError("Subclasses must implement `validate`.")

class SchemaValidator(BaseValidator):
    """Validates data against a defined schema."""
    def __init__(self, schema):
        self.schema = schema

    def validate(self, data):
        errors = {}
        for field, rules in self.schema.items():
            value = data.get(field)

            # If rules is a dictionary, handle as a nested schema
            if isinstance(rules, dict):
                try:
                    nested_validator = SchemaValidator(rules)
                    nested_validator.validate(value)
                except ValidationError as e:
                    errors[field] = e.message

            # If rules is a list, handle as validation rules
            elif isinstance(rules, list):
                for rule in rules:
                    try:
                        rule(value)
                    except ValidationError as e:
                        errors[field] = e.message

            else:
                errors[field] = f"Invalid schema definition for field '{field}'."

        if errors:
            raise ValidationError(f"Validation errors: {errors}")

        return data

class NestedValidator(BaseValidator):
    """Handles both flat and nested schemas."""
    def __init__(self, schema):
        """
        :param schema: The schema for validation. 
                       Can contain a mix of rules (lists) and nested schemas (dicts).
        """
        self.schema = schema

    def validate(self, data):
        """
        Recursively validates data against the schema.
        :param data: Input data to validate.
        :return: Validated data if successful.
        :raises ValidationError: If validation fails for any field.
        """
        if not isinstance(data, dict):
            raise ValidationError("Input data must be a dictionary.")

        errors = {}
        for key, field_schema in self.schema.items():
            if key not in data:
                errors[key] = "Field is missing."
                continue

            value = data[key]
            # Handle nested dictionary schemas
            if isinstance(field_schema, dict):
                try:
                    nested_validator = NestedValidator(field_schema)
                    nested_validator.validate(value)
                except ValidationError as e:
                    errors[key] = e.message

            # Handle flat validation rules (list of validators)
            elif isinstance(field_schema, list):
                for rule in field_schema:
                    try:
                        rule(value)
                    except ValidationError as e:
                        errors[key] = e.message
            else:
                errors[key] = f"Invalid schema definition for field '{key}'."

        if errors:
            raise ValidationError(f"Validation errors: {errors}")

        return data


