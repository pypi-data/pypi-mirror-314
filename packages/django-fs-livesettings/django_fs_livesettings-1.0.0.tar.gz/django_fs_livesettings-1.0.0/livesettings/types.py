from django.forms import fields
from django.forms import widgets
from django.contrib.admin import widgets as admin_widgets


TYPE_BOOLEAN = 'boolean'
TYPE_CHAR = 'char'
TYPE_DATE = 'date'
TYPE_DATETIME = 'datetime'
TYPE_DECIMAL = 'decimal'
TYPE_EMAIL = 'email'
TYPE_FILE = 'file'
TYPE_IMAGE = 'image'
TYPE_INTEGER = 'integer'
TYPE_TIME = 'time'
TYPE_URL = 'url'


TYPES = (
    TYPE_BOOLEAN,
    TYPE_CHAR,
    TYPE_DATE,
    TYPE_DATETIME,
    TYPE_DECIMAL,
    TYPE_EMAIL,
    TYPE_FILE,
    TYPE_IMAGE,
    TYPE_INTEGER,
    TYPE_TIME,
    TYPE_URL,
)


TYPE_FIELD = {
    TYPE_BOOLEAN: fields.BooleanField,
    TYPE_CHAR: fields.CharField,
    TYPE_DATE: fields.DateField,
    TYPE_DATETIME: fields.SplitDateTimeField,
    TYPE_DECIMAL: fields.DecimalField,
    TYPE_EMAIL: fields.EmailField,
    TYPE_FILE: fields.FileField,
    TYPE_IMAGE: fields.ImageField,
    TYPE_INTEGER: fields.IntegerField,
    TYPE_TIME: fields.TimeField,
    TYPE_URL: fields.URLField,
}


TYPE_WIDGET = {
    TYPE_BOOLEAN: widgets.CheckboxInput,
    TYPE_CHAR: admin_widgets.AdminTextInputWidget,
    TYPE_DATE: admin_widgets.AdminDateWidget,
    TYPE_DATETIME: admin_widgets.AdminSplitDateTime,
    TYPE_DECIMAL: admin_widgets.AdminTextInputWidget,
    TYPE_EMAIL: admin_widgets.AdminTextInputWidget,
    TYPE_FILE: admin_widgets.AdminFileWidget,
    TYPE_IMAGE: admin_widgets.AdminFileWidget,
    TYPE_INTEGER: admin_widgets.AdminIntegerFieldWidget,
    TYPE_TIME: admin_widgets.AdminTimeWidget,
    TYPE_URL: admin_widgets.AdminURLFieldWidget,
}
