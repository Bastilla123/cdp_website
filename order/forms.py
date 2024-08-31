from .models import *
from django.forms import ModelForm
from django import forms
from django.utils.translation import gettext as _
from bibliothek.cdc import *
from django.forms import ValidationError
from bibliothek.widgets import *
from django.utils.translation import gettext_lazy as _

class preselection_Form(forms.ModelForm):
    expected_consumption = forms.IntegerField(required=True)

    class Meta:
        model = CustomerInfo
        fields = ["zip"]
        labels = {'zip': _('ZIP'), 'expected_consumption': _('Expected Consumption in kwh')}


class product_Form(forms.Form):
    products = forms.ModelChoiceField(queryset=Product.objects.all())


class CustomerInfoForm(forms.ModelForm):
    class Meta:
        model = CustomerInfo
        exclude = ['zip']




class ConsentForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        consentlist = get_list_constenstatements()

        for key, value in consentlist['preferences'].items():

            if 'de' in value["langs"]:

                legal = get_legal_statment('de', key)

                if '1' in legal['legalStatements']['versions']:
                    if 'documentUrl' in legal['legalStatements']['versions']['1']:
                        self.fields["{}_boolean".format(key)] = forms.ChoiceField(widget=choicedownloadwidget(
                            download_link=legal['legalStatements']['versions']['1']['documentUrl']), choices=(
                            (0, '-----',), (1, _('Agree')),))
                        self.fields["{}_url".format(key)] = forms.CharField(widget=forms.HiddenInput(), required=False,
                                                                            initial=
                                                                            legal['legalStatements']['versions']['1'][
                                                                                'documentUrl'])
                    else:
                        self.fields["{}_boolean".format(key)] = forms.ChoiceField(choices=(
                            (0, '-----',), (1, _('Agree')), (2, _('Not Agree')),))
                else:
                    self.fields["{}_boolean".format(key)] = forms.ChoiceField(choices=(
                        (0, '-----',), (1, _('Agree')), (2, _('Not Agree'))))

                #if value["isMandatory"] == True:
                    #self.fields["{}_boolean".format(key)].label = "{} *".format(key)
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






