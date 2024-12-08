import unittest
import sys
import os

# Add the project root directory to sys.path to allow importing from `src`
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from src.core.serializer import JSONSerializer, YAMLSerializer
from src.core.errors import SerializationError

class TestJSONSerializer(unittest.TestCase):
    def test_json_serialization(self):
        serializer = JSONSerializer()
        data = {"name": "John", "age": 30}
        json_data = serializer.serialize(data)
        self.assertEqual(serializer.deserialize(json_data), data)

    def test_invalid_serialization(self):
        serializer = JSONSerializer()
        with self.assertRaises(SerializationError):
            serializer.serialize(set([1, 2, 3]))  # YAML does not support sets

    def test_invalid_deserialization(self):
        serializer = JSONSerializer()
        with self.assertRaises(SerializationError):
            serializer.deserialize("invalid json string")


class TestYAMLSerializer(unittest.TestCase):
    def test_yaml_serialization(self):
        serializer = YAMLSerializer()
        data = {"name": "John", "age": 30}
        yaml_data = serializer.serialize(data)
        self.assertEqual(serializer.deserialize(yaml_data), data)

    def test_invalid_serialization(self):
        serializer = YAMLSerializer()
        with self.assertRaises(SerializationError):
            serializer.serialize(set([1, 2, 3]))  

    def test_invalid_deserialization(self):
        serializer = YAMLSerializer()
        with self.assertRaises(SerializationError):
            serializer.deserialize("!!invalid yaml string")


if __name__ == "__main__":
    unittest.main()
