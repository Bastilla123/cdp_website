from django.forms.widgets import Select
from django.utils.safestring import mark_safe
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