from django.conf import settings


CONF = getattr(settings, 'LIVESETTINGS_CONF', {})
