from .models import *
from django.forms import ModelForm
from django import forms
from django.utils.translation import gettext as _
from bibliothek.cdc import *
from django.forms import ValidationError
from bibliothek.widgets import *
from django.utils.translation import gettext_lazy as _
from customers.models import Profile
from bibliothek.widgets import DatePicker


class preselection_Form(forms.ModelForm):
    expected_consumption = forms.IntegerField(required=True)

    class Meta:
        model = Profile
        fields = ["zip"]
        labels = {'zip': _('ZIP'), 'expected_consumption': _('Expected Consumption in kwh')}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
class product_Form(forms.Form):
    products = forms.ModelChoiceField(queryset=Product.objects.all())


class CustomerInfoForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['zip','image','user','skype','facebook','twitter','linkedin','instagram','dribble','pinterest']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['firstname'] = forms.CharField(required=True)
        self.fields['lastname'] = forms.CharField(required=True)
        self.fields['email'] = forms.CharField(required=True)
        self.fields['address'].required = True
        self.fields['address'].label = "Straße"
        self.fields['number'].required = True
        self.fields['city'].required = True

        self.fields['firstname'].initial = "Sebastian"
        self.fields['lastname'].initial = "Jung"
        self.fields['email'].initial = "s@s.de"
        self.fields['city'].initial = "2434234"
        self.fields['number'].initial = "32112321"
        self.fields['address'].initial = "43223443"

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ConsentForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        consent_list = get_last_consent()

        for consent in consent_list:
            key=consent['key']
            if 'downloadurl' in consent:
                self.fields["{}_boolean".format(key)] = forms.ChoiceField(initial=1, widget=choicedownloadwidget(
                                download_link=consent['downloadurl']), choices=(
                                 (0, '-----',), (1, _('Agree'))))
                self.fields["{}_url".format(key)] = forms.CharField(widget=forms.HiddenInput(), required=False,
                                                                                 initial=
                                                                                 consent['downloadurl'])
            else:
                self.fields["{}_boolean".format(key)] = forms.ChoiceField(initial=1, choices=(
                                         (0, '-----',), (1, _('Agree')), (2, _('Not Agree')),))
            if consent['isMandatory'] == True:

                self.fields["{}_boolean".format(key)].required = True

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean(self):
        data = super().clean()

        consentlist = get_list_constenstatements()
        for key, value in data.items():

            if '_boolean' in key:

                key = key.replace("_boolean", "")
                if key in consentlist['preferences']:

                    if consentlist['preferences'][key]["isMandatory"] == True:

                        if value == str(0):
                            raise ValidationError(_("Field {} is mandatory").format(key))
                else:

                    raise ValidationError(
                        _("Key {} not found in consentlist {}").format(key, consentlist['preferences']))


        return data






