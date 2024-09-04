from django.forms.widgets import Select
from django.utils.safestring import mark_safe
from django.forms import CheckboxInput, Select, SelectMultiple, NumberInput, TextInput

class DatePicker(TextInput):
    template_name = 'datepicker.html'

    def __init__(self, attrs=None, placeholder=None):
        if attrs is None:
            attrs = {}
        if placeholder:
            attrs['placeholder'] = placeholder
        super().__init__(attrs)


class DateTimePicker(TextInput):
    template_name = 'datetimepicker.html'

    def __init__(self, attrs=None, placeholder=None):
        if attrs is None:
            attrs = {}
        if placeholder:
            attrs['placeholder'] = placeholder
        super().__init__(attrs)

class choicedownloadwidget(Select):
    def __init__(
            self,

            *args,
            **kwargs
    ):
        if 'download_link' in kwargs:
            self.download_link = kwargs.pop('download_link')

        super().__init__(*args, **kwargs)




    def render(self, name, value, attrs=None, renderer=None):

        html = super().render(name, value, attrs)

        html += '<a target="_blank" href="{}" download="proposed_file_name">Download {}</a>'.format(self.download_link,name,)

        return mark_safe(html)