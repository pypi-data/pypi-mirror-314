from django.contrib import admin

from livesettings.forms import SettingAdminForm
from livesettings.models import Setting


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    """
    """

    list_display = ('key', 'tpe', 'value', 'description')
    fields = ('key', 'tpe', 'value', 'description')
    readonly_fields = ('key', 'tpe', 'description')
    actions = None
    form = SettingAdminForm

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
