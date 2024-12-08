import sys
import os
import re
from datetime import datetime
from uuid import UUID

# Add the project root directory to sys.path to allow importing from `src`
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from src.core.errors import ValidationError

# Basic Validators
def is_required(value):
    if value is None:
        raise ValidationError("Value is required.")


def is_type(expected_type):
    def validator(value):
        if not isinstance(value, expected_type):
            raise ValidationError(f"Value must be of type {expected_type.__name__}.")
    return validator


def is_in_range(min_value, max_value):
    def validator(value):
        if not (min_value <= value <= max_value):
            raise ValidationError(f"Value must be between {min_value} and {max_value}.")
    return validator


def is_email(value):
    if not isinstance(value, str):
        raise ValidationError("Invalid email format. Value must be a string.")
    if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
        raise ValidationError("Invalid email format.")


# String Validators
def max_length(max_len):
    def validator(value):
        if not isinstance(value, str):
            raise ValidationError("Value must be a string.")
        if len(value) > max_len:
            raise ValidationError(f"Value exceeds maximum length of {max_len}.")
    return validator


def min_length(min_len):
    def validator(value):
        if not isinstance(value, str):
            raise ValidationError("Value must be a string.")
        if len(value) < min_len:
            raise ValidationError(f"Value must be at least {min_len} characters long.")
    return validator


def matches_regex(pattern):
    def validator(value):
        if not isinstance(value, str):
            raise ValidationError("Value must be a string.")
        if not re.match(pattern, value):
            raise ValidationError(f"Value does not match the required pattern: {pattern}")
    return validator


# Numerical Validators
def is_positive(value):
    if not isinstance(value, (int, float)):
        raise ValidationError("Value must be a number.")
    if value <= 0:
        raise ValidationError("Value must be positive.")


def is_negative(value):
    if not isinstance(value, (int, float)):
        raise ValidationError("Value must be a number.")
    if value >= 0:
        raise ValidationError("Value must be negative.")


def is_integer(value):
    if not isinstance(value, int):
        raise ValidationError("Value must be an integer.")


# Date and Time Validators
def is_date(format="%Y-%m-%d"):
    def validator(value):
        if not isinstance(value, str):
            raise ValidationError("Value must be a string.")
        try:
            datetime.strptime(value, format)
        except ValueError:
            raise ValidationError(f"Value must be a valid date in the format {format}.")
    return validator


def is_before_date(limit_date, format="%Y-%m-%d"):
    def validator(value):
        if not isinstance(value, str):
            raise ValidationError("Value must be a string.")
        try:
            date = datetime.strptime(value, format)
            limit = datetime.strptime(limit_date, format)
            if date >= limit:
                raise ValidationError(f"Date must be before {limit_date}.")
        except ValueError:
            raise ValidationError(f"Value must be a valid date in the format {format}.")
    return validator


def is_after_date(limit_date, format="%Y-%m-%d"):
    def validator(value):
        if not isinstance(value, str):
            raise ValidationError("Value must be a string.")
        try:
            date = datetime.strptime(value, format)
            limit = datetime.strptime(limit_date, format)
            if date <= limit:
                raise ValidationError(f"Date must be after {limit_date}.")
        except ValueError:
            raise ValidationError(f"Value must be a valid date in the format {format}.")
    return validator


# Collection Validators
def is_in_list(allowed_values):
    def validator(value):
        if value not in allowed_values:
            raise ValidationError(f"Value must be one of {allowed_values}.")
    return validator


def has_unique_elements(value):
    if not isinstance(value, list):
        raise ValidationError("Value must be a list.")
    if len(value) != len(set(value)):
        raise ValidationError("List must have unique elements.")


# Advanced Validators
def is_uuid(value):
    try:
        UUID(str(value))
    except ValueError:
        raise ValidationError("Value must be a valid UUID.")


def is_url(value):
    if not isinstance(value, str):
        raise ValidationError("Value must be a string.")
    if not re.match(r"https?://[^\s/$.?#].[^\s]*", value):
        raise ValidationError("Value must be a valid URL.")
