import re
from prompt_toolkit.validation import ValidationError

from inferless_cli.utils.constants import (
    FRAMEWORKS,
    MACHINE_TYPE_SERVERS,
    UPLOAD_METHODS,
)


def validate_framework(choice):
    if choice not in FRAMEWORKS:
        raise ValidationError(
            message=f"Invalid choice. Please select from {', '.join(FRAMEWORKS)}"
        )
    return choice


def validate_machine_types(choice, machines):
    if choice not in machines:
        raise ValidationError(
            message=f"Invalid choice. Please select from {', '.join(machines)}"
        )
    return choice


def validate_machine_types_server(choice):
    if choice not in MACHINE_TYPE_SERVERS:
        raise ValidationError(
            message=f"Invalid choice. Please select from {', '.join(MACHINE_TYPE_SERVERS)}"
        )
    return choice


def validate_upload_method(choice):
    if choice not in UPLOAD_METHODS:
        raise ValidationError(
            message=f"Invalid choice. Please select from {', '.join(UPLOAD_METHODS)}"
        )
    return choice


def validate_model_name(text):
    if not re.match(r"^[a-zA-Z0-9_-]+$", text):
        raise ValidationError(
            message="Model Name can only contain alphanumeric characters, underscores, and dashes."
        )
    if len(text) > 32:
        raise ValidationError(
            message="Character limit is reached (maximum 32 characters)."
        )
    return text


def validate_url(url):
    # Use a regular expression to check if the input matches a valid URL pattern
    url_pattern = re.compile(r"^(https?|ftp)://[^\s/$.?#].[^\s]*$", re.IGNORECASE)
    if not url_pattern.match(url):
        raise ValidationError(message="Invalid URL. Please enter a valid URL.")
    return url


def validate_region_types(choice, regions):
    if choice not in regions:
        raise ValidationError(
            message=f"Invalid choice. Please select from {', '.join(regions)}"
        )
    return choice
