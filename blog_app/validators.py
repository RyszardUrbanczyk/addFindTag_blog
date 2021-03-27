from django.core.exceptions import ValidationError


def check_length(value):
    if len(value) < 0:
        raise ValidationError("za krótkie")
