from django.apps import AppConfig
from django.core.exceptions import ImproperlyConfigured
from django.db import connection
from django.db.utils import DatabaseError


class LivesettingsConfig(AppConfig):
    name = 'livesettings'
    verbose_name = 'Livesettings'

    def ready(self):
        self._fill_in_settings()

    def _fill_in_settings(self):
        from livesettings.models import Setting
        from livesettings import settings as _settings
        from livesettings import types as _types
        # whether Setting has been installed or not
        try:
            Setting.objects.exists()
        except DatabaseError:
            connection._rollback()
            return
        for key, tpe, description in _settings.CONF:
            if tpe not in _types.TYPES:
                raise ImproperlyConfigured('Livesettings is improperly configured.')
            if Setting.objects.filter(key=key).update(tpe=tpe, description=description) == 0:
                Setting.objects.create(key=key, tpe=tpe, description=description)
        Setting.objects.exclude(key__in=[conf[0] for conf in _settings.CONF]).delete()
