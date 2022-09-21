from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    """validate that year is smaller or equal to current."""
    if value <= timezone.now().year:
        return value
    raise ValidationError("Enter a valid year.")
