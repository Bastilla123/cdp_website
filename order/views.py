from customers.models import UserDocument
from django.contrib import messages
from django.views.generic.edit import FormView
from django.shortcuts import render
from formtools.wizard.views import CookieWizardView, SessionWizardView
from formtools.wizard.forms import ManagementForm
from .forms import  *
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
from .models import Product
from django.contrib.auth.models import User
import secrets
from customers.models import *
import json
from django.core.mail import EmailMultiAlternatives
import urllib
from urllib.parse import urlparse
import re
from urllib.request import urlretrieve
import requests
from django.template.loader import render_to_string
import datetime
from django.shortcuts import redirect
from collections import OrderedDict

def show_message_form_condition(wizard):
    return cleaned_data.get('CustomerTypeform', True)




def summary(request):
     productentry = Product.objects.filter(id=1).first()

     context = {'context':{'zip': '52080', 'expected_consumption': 4000,'products':productentry,'firstname': 'Sebastian', 'lastname': 'Jung', 'street': 'Verlautenheidener Str.', 'housenumber': '144a', 'city': 'Aachen', 'email': 'sebastian.jung@intense.de', 'birthday': '2024-08-25 20:41:16.645066', 'phone': '+49789549', 'iban': 'DE128340282','terms.AGB_1_boolean': '1', 'terms.AGB_1_url': 'https://intenseag-my.sharepoint.com/:b:/g/personal/sebastian_jung_intense_de/ETACJjdpxzRFvMjg8dzezgABgP0nW4ZAzT3upFEOmIZ_4w?e=yvzRGj', 'privacy.Privacy_1_boolean': '1', 'privacy.Privacy_1_url': 'https://intenseag-my.sharepoint.com/:w:/g/personal/sebastian_jung_intense_de/EZueD4lr_B9Nr0Wa0p4DZ48BpzOY8kFFu5yTVC2BIk8SXw?e=sZ1yN1', 'Widerruf_boolean': '1', 'Widerruf_url': 'https://accounts.eu1.gigya.com/accounts.store.downloadPublicConsentDocument?docID=31857958_101769715074_a45706c7e6b44d00a786d8cf8ad2e73a.pdf', 'Newsletter_boolean': '2'}}
     context_json = {'zip': '52080', 'expected_consumption': 4000, 'product_id': productentry.id, 'firstname': 'Sebastian',
                     'lastname': 'Jung', 'street': 'Verlautenheidener Str.', 'housenumber': '144a', 'city': 'Aachen',
                     'email': 'sebastian.jung@intense.de', 'birthday': '2024-08-25',
                     'phone': '+49789549', 'iban': 'DE128340282', 'terms.AGB_1_boolean': '1',
                     'terms.AGB_1_url': 'https://intenseag-my.sharepoint.com/:b:/g/personal/sebastian_jung_intense_de/ETACJjdpxzRFvMjg8dzezgABgP0nW4ZAzT3upFEOmIZ_4w?e=yvzRGj',
                     'privacy.Privacy_1_boolean': '1',
                     'privacy.Privacy_1_url': 'https://intenseag-my.sharepoint.com/:w:/g/personal/sebastian_jung_intense_de/EZueD4lr_B9Nr0Wa0p4DZ48BpzOY8kFFu5yTVC2BIk8SXw?e=sZ1yN1',
                     'Widerruf_boolean': '1',
                     'Widerruf_url': 'https://accounts.eu1.gigya.com/accounts.store.downloadPublicConsentDocument?docID=31857958_101769715074_a45706c7e6b44d00a786d8cf8ad2e73a.pdf',
                     'Newsletter_boolean': '2'}
     jsoncontext = json.dumps(context_json)
     print("Conext "+str(jsoncontext))
     context.update({'json':jsoncontext})

     return render(request,'summary.html',context=context)

def execute_order(request):
    context = request.POST.get('order_context')
    print("Context "+str(context))
    context = json.loads(context)

    #new django user
    while 1:
        username = secrets.token_urlsafe(13)

        userentry = User.objects.filter(username=username).first()

        # when username is free then exit loop
        if not userentry:
            break
        if userentry is None:
            break


    password = secrets.token_urlsafe(13)
    try:
            userentry = User.objects.create_user(username=username,
                                         first_name=context["firstname"], last_name=context["lastname"],
                                         email=context['email'],
                                         password=password)
            userentry.save()

    except Exception as e:
            messages.error(request, "Error on saving User {}".format(e))
    profileentry = Profile.objects.create(user=userentry,phone =context['phone'],address =context['street'],number =context['housenumber'],
                                              city =context['city'],zip =context['zip'],iban =context['iban'])
    profileentry.save()

    # runterladen der ganzen PDF Dokumente aus dem CDC in das 'media/customers/{}/documents/'.format(userentry.id) dir

    consentdownloadlist = get_last_consent(request)

    newconsent = []
    dir = 'media/customers/{}/documents/'.format(userentry.id)
    try:

        os.makedirs(dir)
    except Exceptions as e:
        pass
    for consent in consentdownloadlist:



        filenamenew = "{}.pdf".format("{}_{}".format(consent[0],datetime.datetime.now()))


        extendconsent= [consent[0],consent[1],consent[2],filenamenew]
        newconsent.append(extendconsent)
        try:

            urlretrieve(consent[2], "{}{}".format(dir,filenamenew))
        except Exception as e:
            messages.error(request, "Urlretrieve from Url {} Error {}".format(consent[2],e))
            return render(request, 'order_execute.html')

        # eintragen in die Documents Liste
        userdocumententity = UserDocument(document="{}{}".format(dir,filenamenew), user_link=userentry,filename=filenamenew)
        userdocumententity.save()




    if settings.SEND_EMAIL:

        #send Email with Consent Attachments

        subject = 'Neuer Vertrag'
        from_email = 'postmaster@beelze-solutions.de'
        to = 'sebastian.jung2@gmx.de'
        text_content = 'That’s your plain text.'


        template_name = "email_template.html"
        product_id = context['product_id']
        productentry = Product.objects.filter(id=product_id).first()
        base_url = "{0}://{1}".format(request.scheme, request.get_host(),)
        context['products'] = productentry
        context['password'] = password
        context['username'] = username
        context['url'] = base_url
        convert_to_html_content = render_to_string(
            template_name=template_name,
            context=context
        )
        html_content = convert_to_html_content
        message = EmailMultiAlternatives(subject, text_content, from_email, [to])
        message.attach_alternative(html_content, "text/html")

        #und danach anhängen dieser Dokumente
        for consent in newconsent:

            message.attach_file("{}{}".format(dir,consent[3]), 'application/pdf')
        try:

            message.send()
        except Exception as e:

            messages.error(request, "Message send Error {}".format(consent[2], e))
            return render(request, 'summary.html',context=context)

    #insert in cdc a new user with consent data

    preferences = '{'

    for count,consent in enumerate(newconsent):

        if count > 0:

            preferences += ","


        splitentrys = consent[0].split(".")

        if len(splitentrys) == 2:

            preferences += '"{}":'.format(splitentrys[0])
            preferences += '{'
            preferences += '"{}":'.format(splitentrys[1])

        else:

            preferences += '"{}":'.format(splitentrys[0])
        preferences += '{"isConsentGranted": true, "actionTimestamp": "2024-08-12T14:24:11.707Z","lastConsentModified": "2024-08-12T14:24:11.707Z"}'
        if len(splitentrys) == 2:
            preferences += '}'



    accountdata = {"address":(str(context["street"])+str(context["housenumber"])),"firstName":context["firstname"], "lastName":context["lastname"], "email": context["email"],"city":context['city'],"zip": context['zip']}

    try:
        insert_FullAccount(str(userentry.id),
                       accountdata,preferences)

    except Exception as e:

        messages.error(request, "Insert Fullaccount Error {}".format(e))
        return render(request, 'summary.html',context=context)
    if settings.SEND_EMAIL:
        messages.info(request, "Wir haben ihre Bestellung erhalten. Sie haben von uns eine E-Mail mit den zugehörigen Vertragsdaten und Zugangsdaten zu dem Login Bereich erhalten")
    else:
        messages.info(request, "Wir haben ihre Bestellung erhalten und melden uns bei ihnen")
    return redirect('home')


class customerFormSubmission(CookieWizardView):

    form_list = [preselection_Form,product_Form, CustomerInfoForm,ConsentForm]
    #form_list = [preselection_Form,ConsentForm]

    # def post(self, *args, **kwargs):
    #
    #     """
    #     This method handles POST requests.
    #     The wizard will render either the current step (if form validation
    #     wasn't successful), the next step (if the current step was stored
    #     successful) or the done view (if no more steps are available)
    #     """
    #     # Look for a wizard_goto_step element in the posted data which
    #     # contains a valid step name. If one was found, render the requested
    #     # form. (This makes stepping back a lot easier).
    #     wizard_goto_step = self.request.POST.get('wizard_goto_step', None)
    #     if wizard_goto_step and wizard_goto_step in self.get_form_list():
    #         return self.render_goto_step(wizard_goto_step)
    #     # Check if form was refreshed
    #     management_form = ManagementForm(self.request.POST, prefix=self.prefix)
    #     if not management_form.is_valid():
    #         print("Management not valid")
    #         raise ValidationError(
    #             _('ManagementForm data is missing or has been tampered.'),
    #             code='missing_management_form',
    #         )
    #     form_current_step = management_form.cleaned_data['current_step']
    #     if (form_current_step != self.steps.current and
    #             self.storage.current_step is not None):
    #         # form refreshed, change current step
    #         self.storage.current_step = form_current_step
    #     # get the form for the current step
    #     form = self.get_form(data=self.request.POST, files=self.request.FILES)
    #     # and try to validate
    #     if form.is_valid():
    #         # if the form is valid, store the cleaned data and files.
    #         self.storage.set_step_data(self.steps.current, self.process_step(form))
    #         self.storage.set_step_files(self.steps.current, self.process_step_files(form))
    #         # check if the current step is the last step
    #         if self.steps.current == self.steps.last:
    #             print("Done")
    #             # no more steps, render done view
    #             return self.render_done(form, **kwargs)
    #         else:
    #
    #             # proceed to the next step
    #             return self.render_next_step(form)
    #
    #     return self.render(form)
    #
    # def render_done(self, form, **kwargs):
    #
    #     """
    #     This method gets called when all forms passed. The method should also
    #     re-validate all steps to prevent manipulation. If any form fails to
    #     validate, `render_revalidation_failure` should get called.
    #     If everything is fine call `done`.
    #     """
    #     final_forms = OrderedDict()
    #     # walk through the form list and try to validate the data again.
    #     for form_key in self.get_form_list():
    #         print("Step {} data {} ".format(form_key,self.storage.get_step_data(form_key)))
    #         form_obj = self.get_form(step=form_key,
    #                                  data=self.storage.get_step_data(form_key),
    #                                  files=self.storage.get_step_files(form_key))
    #         if not form_obj.is_valid():
    #             print("Failure form_key {} form_obj {} kwargs {}".format(form_key, form_obj, kwargs))
    #             return self.render_revalidation_failure(form_key, form_obj, **kwargs)
    #         final_forms[form_key] = form_obj
    #     # render the done view and reset the wizard before returning the
    #     # response. This is needed to prevent from rendering done with the
    #     # same data twice.
    #     done_response = self.done(final_forms.values(), form_dict=final_forms, **kwargs)
    #     self.storage.reset()
    #     print("Return "+str(done_response))
    #     return done_response

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        context['products_list'] = Product.objects.all()

        return context

    def get_template_names(self):

        if "product_Form" in str(self.get_form().__class__):
            return 'products.html'
        else:

            return 'forms.html'




    def done(self, form_list, **kwargs):
        print("Done")
        contextnew = {}
        for form in form_list:
            contextnew.update(form.cleaned_data)
        context = {'context': contextnew}

        context_json = dict(contextnew)
        if 'products' in contextnew:
            context_json['product_id'] = contextnew['products'].id
            context_json.pop('products')
        if 'birthday' in context_json:
            context_json.pop('birthday')


        jsoncontext = json.dumps(context_json)

        context.update({'json': jsoncontext})
        print("Json " + str(context))

        return render(self.request, 'summary.html', context=context)

    # productentry = Product.objects.filter(id=1).first()
    #
    # context = {
    #     'context': {'zip': '52080', 'expected_consumption': 4000, 'products': productentry, 'firstname': 'Sebastian',
    #                 'lastname': 'Jung', 'street': 'Verlautenheidener Str.', 'housenumber': '144a', 'city': 'Aachen',
    #                 'email': 'sebastian.jung@intense.de', 'birthday': '2024-08-25 20:41:16.645066',
    #                 'phone': '+49789549', 'iban': 'DE128340282', 'terms.AGB_1_boolean': '1',
    #                 'terms.AGB_1_url': 'https://intenseag-my.sharepoint.com/:b:/g/personal/sebastian_jung_intense_de/ETACJjdpxzRFvMjg8dzezgABgP0nW4ZAzT3upFEOmIZ_4w?e=yvzRGj',
    #                 'privacy.Privacy_1_boolean': '1',
    #                 'privacy.Privacy_1_url': 'https://intenseag-my.sharepoint.com/:w:/g/personal/sebastian_jung_intense_de/EZueD4lr_B9Nr0Wa0p4DZ48BpzOY8kFFu5yTVC2BIk8SXw?e=sZ1yN1',
    #                 'Widerruf_boolean': '1',
    #                 'Widerruf_url': 'https://accounts.eu1.gigya.com/accounts.store.downloadPublicConsentDocument?docID=31857958_101769715074_a45706c7e6b44d00a786d8cf8ad2e73a.pdf',
    #                 'Newsletter_boolean': '2'}}
    # context_json = {'zip': '52080', 'expected_consumption': 4000, 'product_id': productentry.id,
    #                 'firstname': 'Sebastian',
    #                 'lastname': 'Jung', 'street': 'Verlautenheidener Str.', 'housenumber': '144a', 'city': 'Aachen',
    #                 'email': 'sebastian.jung@intense.de', 'birthday': '2024-08-25',
    #                 'phone': '+49789549', 'iban': 'DE128340282', 'terms.AGB_1_boolean': '1',
    #                 'terms.AGB_1_url': 'https://intenseag-my.sharepoint.com/:b:/g/personal/sebastian_jung_intense_de/ETACJjdpxzRFvMjg8dzezgABgP0nW4ZAzT3upFEOmIZ_4w?e=yvzRGj',
    #                 'privacy.Privacy_1_boolean': '1',
    #                 'privacy.Privacy_1_url': 'https://intenseag-my.sharepoint.com/:w:/g/personal/sebastian_jung_intense_de/EZueD4lr_B9Nr0Wa0p4DZ48BpzOY8kFFu5yTVC2BIk8SXw?e=sZ1yN1',
    #                 'Widerruf_boolean': '1',
    #                 'Widerruf_url': 'https://accounts.eu1.gigya.com/accounts.store.downloadPublicConsentDocument?docID=31857958_101769715074_a45706c7e6b44d00a786d8cf8ad2e73a.pdf',
    #                 'Newsletter_boolean': '2'}
    # jsoncontext = json.dumps(context_json)
    # print("Conext " + str(jsoncontext))
    # context.update({'json': jsoncontext})

