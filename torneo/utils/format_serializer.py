from typing import Any
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList

def format_serializer_errors(errors):
    if isinstance(errors, dict):
        formatted = {}
        for field, value in errors.items():
            formatted[field] = format_serializer_errors(value)
        return formatted

    if isinstance(errors, list):
        if all(isinstance(item, str) for item in errors):
            return " ".join(errors)
        return [format_serializer_errors(item) for item in errors]

    return str(errors)
