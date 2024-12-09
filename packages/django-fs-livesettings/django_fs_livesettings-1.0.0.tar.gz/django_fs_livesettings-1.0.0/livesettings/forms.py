from django import forms

from livesettings import types as _types


class SettingAdminForm(forms.ModelForm):
    """
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        value_field = self.fields['value']
        kwargs = {
            'required': value_field.required,
            'label': value_field.label,
            'help_text': value_field.help_text,
            'widget': _types.TYPE_WIDGET.get(self.instance.tpe),
        }
        self.fields['value'] = _types.TYPE_FIELD.get(self.instance.tpe)(**kwargs)
