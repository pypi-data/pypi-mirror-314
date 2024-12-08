import json
import yaml
from .errors import SerializationError

class BaseSerializer:
    """Abstract class for serialization."""
    def serialize(self, data):
        raise NotImplementedError("Subclasses must implement `serialize`.")

    def deserialize(self, data):
        raise NotImplementedError("Subclasses must implement `deserialize`.")


class JSONSerializer(BaseSerializer):
    """Handles JSON serialization."""
    def serialize(self, data):
        try:
            return json.dumps(data)
        except (TypeError, ValueError) as e:
            raise SerializationError(f"Serialization error: {e}")

    def deserialize(self, data):
        try:
            return json.loads(data)
        except json.JSONDecodeError as e:
            raise SerializationError(f"Deserialization error: {e}")


class YAMLSerializer(BaseSerializer):
    """Handles YAML serialization."""
    def serialize(self, data):
        try:
            if isinstance(data, set):
                raise TypeError("YAML does not support `set` type.")
            return yaml.dump(data)
        except (TypeError, yaml.YAMLError) as e:
            raise SerializationError(f"Serialization error: {e}")

    def deserialize(self, data):
        try:
            return yaml.safe_load(data)
        except yaml.YAMLError as e:
            raise SerializationError(f"Deserialization error: {e}")
