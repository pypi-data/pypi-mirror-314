from django.db import models

from picklefield import fields as picklefields

from livesettings import fields as _fields
from livesettings import types as _types


class Setting(models.Model):
    """
    """

    TYPE_CHOICES = zip(_types.TYPES, _types.TYPES)

    key = _fields.KeyField(verbose_name='key', primary_key=True)
    tpe = models.CharField(verbose_name='type', max_length=255, choices=TYPE_CHOICES, blank=True, null=True)
    value = picklefields.PickledObjectField(verbose_name='value', editable=True, blank=True, null=True)
    description = models.CharField(verbose_name='description', max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'setting'
        verbose_name_plural = 'settings'

    def __str__(self):
        return self.key

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Setting, self).save(*args, **kwargs)
