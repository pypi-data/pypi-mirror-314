
# Janus

![Latest Version](https://img.shields.io/pypi/v/janus-validation)
![Downloads](https://img.shields.io/pypi/dm/janus-validation)
![Status](https://img.shields.io/badge/status-alpha-orange)
![License: MIT](https://img.shields.io/badge/License-MIT-lightgrey.svg)

**Janus** is a modern Python library for data validation, serialization, and schema versioning. It provides developers with a flexible, performant, and extensible toolkit to handle input validation, data transformation, and API schema compatibility with ease.

[Click here for the documentation](https://github.com/altxriainc/janus/wiki)

---

## 🚀 Key Features

- **Robust Data Validation**: Includes a comprehensive set of validators for strings, numbers, dates, collections, and more.
- **Nested Schema Validation**: Supports complex and deeply nested data structures.
- **Schema Versioning**: Seamlessly handle schema evolution and data migration between API versions.
- **Serialization**: Convert Python objects to JSON or YAML formats with error handling.
- **Custom Validators**: Easily extend Janus with custom validation rules.
- **Open for Personal & Commercial Use**: Use Janus freely in personal and commercial projects (not for resale as a standalone product).

---

## 🛠️ How to Use Janus

### Step 1: Install Janus

Install Janus via pip:

```bash
pip install janus-validation
```

### Step 2: Validate Your First Data

Define a validation schema:

```python
from janus.utils.validators import is_required, is_type, is_email
from janus.core.validator import SchemaValidator

schema = {
    "name": [is_required, is_type(str)],
    "email": [is_required, is_email],
    "age": [is_type(int)],
}

validator = SchemaValidator(schema)

data = {"name": "Alice", "email": "alice@example.com", "age": 30}
validated_data = validator.validate(data)
print("Validated Data:", validated_data)
```

### Step 3: Use Schema Versioning

Manage schema evolution with ease:

```python
from janus.core.schema_versioning import SchemaVersioning

versioning = SchemaVersioning()

# Register schemas
versioning.register_schema("v1", {"name": [is_required]})
versioning.register_schema("v2", {"name": [is_required], "email": [is_email]})

# Validate data with specific schema versions
data = {"name": "Alice", "email": "alice@example.com"}
validated = versioning.validate_with_version("v2", data)
print("Validated:", validated)
```

### Step 4: Serialize Data

Convert Python objects to JSON or YAML:

```python
from janus.core.serializer import JSONSerializer, YAMLSerializer

serializer = JSONSerializer()
json_data = serializer.serialize({"name": "Alice", "age": 30})
print("Serialized JSON:", json_data)

yaml_serializer = YAMLSerializer()
yaml_data = yaml_serializer.serialize({"name": "Alice", "age": 30})
print("Serialized YAML:", yaml_data)
```

---

## 🔍 Project Status

![Issues Closed](https://img.shields.io/github/issues-closed/altxriainc/janus)
![Bug Issues](https://img.shields.io/github/issues/altxriainc/janus/bug)
![Enhancement Issues](https://img.shields.io/github/issues/altxriainc/janus/enhancement)

---

## 📜 License and Usage

Janus is free to use for both personal and commercial projects. However, Janus itself cannot be resold or distributed as a standalone product.

---

## 🤝 Contributors

Developed and maintained by **Altxria Inc.** with contributions from a growing community of passionate developers.

![Contributors](https://contrib.rocks/image?repo=altxriainc/janus)

[See All Contributors](https://github.com/altxriainc/janus/graphs/contributors)

---

## ❤️ Support Janus

If you find Janus useful, consider sponsoring us to support ongoing development and new features!

[![Sponsor Janus](https://img.shields.io/badge/Sponsor-Janus-blue?logo=github-sponsors)](https://github.com/sponsors/altxriainc)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/N4N516SMZ6)
