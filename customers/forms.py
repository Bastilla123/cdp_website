from django import forms
from django.forms import ModelForm
from customers.models import Profile
from .models import Contact
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        labels = {
            "first_name": _("Firstname"),
            "email": _("E-Mail"),
            "last_name": _("Lastname"),
            "street": _("Street"),
            "zip": _("ZIP"),
            "city": _("City"),
            "message": _("Message"),
            "subject": _("Subject"),
        }


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields.pop('email')
            self.fields.pop('first_name')
            self.fields.pop('last_name')
            self.fields.pop('street')
            self.fields.pop('zip')
            self.fields.pop('city')

        self.fields.pop('user_link')

        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=255,label=_("Firstname"))
    last_name = forms.CharField(max_length=255,label= _("Lastname"),)
    email = forms.EmailField()
    birthday = forms.DateField(widget=forms.DateInput(format = '%d.%m.%Y'), input_formats=settings.DATE_INPUT_FORMATS,label = _("Birthday"),required=False)

    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']
        labels = {
            "mobile_number": _("Mobile Number"),
            "email": _("E-Mail"),
            "phone": _("Phone"),
            "street": _("Street"),
            "zip": _("ZIP"),
            "city": _("City"),
            "message": _("Message"),
            "subject": _("Subject"),
            "gender": _("Gender"),
            "address": _("Straße"),
            "number": _("Hausnummer"),

        }
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name
        self.fields['email'].initial = self.instance.user.email
        for field in iter(self.fields):

            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


def form_validation_error(form):
    msg = ""
    for field in form:
        for error in field.errors:
            msg += "%s: %s \\n" % (field.label if hasattr(field, 'label') else 'Error', error)
    return msg
