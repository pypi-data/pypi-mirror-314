import re

from django.db.models.fields import CharField
from django.core.validators import RegexValidator


key_re = re.compile(r'^[a-zA-Z0-9_]+$')
validate_key = RegexValidator(key_re, 'Enter a valid key.', 'invalid')


class KeyField(CharField):
    """
    """

    default_validators = [validate_key]

    def __init__(self, *args, **kwargs):
        assert kwargs.get('primary_key', False) is True, f'{self.__class__.__name__}s must have primary_key=True.'
        kwargs['max_length'] = kwargs.get('max_length', 255)
        CharField.__init__(self, *args, **kwargs)
