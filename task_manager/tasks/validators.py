from django.core.exceptions import ValidationError
from django.utils import timezone

from core.constants import Errors


def validate_deadline(date: timezone) -> timezone:
    """Валидатор для поля deadline."""
    if date < timezone.now():
        raise ValidationError(Errors.DEADLINE_CANNOT_BE_IN_THE_PAST)
    else:
        return date
