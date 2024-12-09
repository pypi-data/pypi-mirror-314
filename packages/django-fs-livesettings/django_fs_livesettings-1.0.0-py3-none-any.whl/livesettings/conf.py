from livesettings.models import Setting


class Livesettings(object):
    """
    """

    def __getattr__(self, name):
        try:
            setting = Setting.objects.get(key=name)
            return setting.value
        except Setting.DoesNotExist:
            raise AttributeError(f'\'{type(self).__name__}\' object has no attribute \'{name}\'')


livesettings = Livesettings()
