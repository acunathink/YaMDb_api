from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def validate_year(value):
    current_year = timezone.now().year
    if value > current_year or value < 0:
        raise ValidationError(
            _('%(value)s больше/меньше значения текущего года'),
            params={'value': value},
        )
