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



#
# def summary(request):
#      productentry = Product.objects.filter(id=1).first()
#
#      context = {'context':{'zip': '52080', 'expected_consumption': 4000,'products':productentry,'firstname': 'Sebastian', 'lastname': 'Jung', 'street': 'Verlautenheidener Str.', 'housenumber': '144a', 'city': 'Aachen', 'email': 'sebastian.jung@intense.de', 'birthday': '2024-08-25 20:41:16.645066', 'phone': '+49789549', 'iban': 'DE128340282','terms.AGB_1_boolean': '1', 'terms.AGB_1_url': 'https://intenseag-my.sharepoint.com/:b:/g/personal/sebastian_jung_intense_de/ETACJjdpxzRFvMjg8dzezgABgP0nW4ZAzT3upFEOmIZ_4w?e=yvzRGj', 'privacy.Privacy_1_boolean': '1', 'privacy.Privacy_1_url': 'https://intenseag-my.sharepoint.com/:w:/g/personal/sebastian_jung_intense_de/EZueD4lr_B9Nr0Wa0p4DZ48BpzOY8kFFu5yTVC2BIk8SXw?e=sZ1yN1', 'Widerruf_boolean': '1', 'Widerruf_url': 'https://accounts.eu1.gigya.com/accounts.store.downloadPublicConsentDocument?docID=31857958_101769715074_a45706c7e6b44d00a786d8cf8ad2e73a.pdf', 'Newsletter_boolean': '2'}}
#      context_json = {'zip': '52080', 'expected_consumption': 4000, 'product_id': productentry.id, 'firstname': 'Sebastian',
#                      'lastname': 'Jung', 'street': 'Verlautenheidener Str.', 'housenumber': '144a', 'city': 'Aachen',
#                      'email': 'sebastian.jung@intense.de', 'birthday': '2024-08-25',
#                      'phone': '+49789549', 'iban': 'DE128340282', 'terms.AGB_1_boolean': '1',
#                      'terms.AGB_1_url': 'https://intenseag-my.sharepoint.com/:b:/g/personal/sebastian_jung_intense_de/ETACJjdpxzRFvMjg8dzezgABgP0nW4ZAzT3upFEOmIZ_4w?e=yvzRGj',
#                      'privacy.Privacy_1_boolean': '1',
#                      'privacy.Privacy_1_url': 'https://intenseag-my.sharepoint.com/:w:/g/personal/sebastian_jung_intense_de/EZueD4lr_B9Nr0Wa0p4DZ48BpzOY8kFFu5yTVC2BIk8SXw?e=sZ1yN1',
#                      'Widerruf_boolean': '1',
#                      'Widerruf_url': 'https://accounts.eu1.gigya.com/accounts.store.downloadPublicConsentDocument?docID=31857958_101769715074_a45706c7e6b44d00a786d8cf8ad2e73a.pdf',
#                      'Newsletter_boolean': '2'}
#      jsoncontext = json.dumps(context_json)
#      print("Conext "+str(jsoncontext))
#      context.update({'json':jsoncontext})
#
#      return render(request,'summary.html',context=context)

def execute_order(request):
    context = request.POST.get('order_context')

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
    profileentry = Profile.objects.create(user=userentry,phone =context['phone'],address =context['address'],number =context['number'],
                                              city =context['city'],zip =context['zip'],iban =context['iban'])
    profileentry.save()

    # runterladen der ganzen PDF Dokumente aus dem CDC in das 'media/customers/{}/documents/'.format(userentry.id) dir

    consent_list = get_last_consent()

    newconsent = []
    dir = 'media/customers/{}/documents/'.format(userentry.id)
    try:

        os.makedirs(dir)
    except Exceptions as e:
        pass
    for consent in consent_list:



        filenamenew = "{}.pdf".format("{}_{}".format(consent['key'],datetime.datetime.now()))

        consent['filename'] = filenamenew

        if 'downloadurl' in consent:
            try:

                urlretrieve(consent['downloadurl'], "{}{}".format(dir,filenamenew))
            except Exception as e:
                messages.error(request, "Urlretrieve from Url {} Error {}".format(consent['downloadurl'],e))
                return render(request, 'order_execute.html')

            # eintragen in die Documents Liste
            userdocumententity = UserDocument(document="{}{}".format(dir,filenamenew), user_link=userentry,filename=filenamenew)
            userdocumententity.save()
    product_id = context['product_id']
    productentry = Product.objects.filter(id=product_id).first()
    #insert order in database
    try:
        orderentity = order.objects.create(user_link =userentry,product_link =productentry,expected_consumption =context['expected_consumption'])
        orderentity.save()
    except Exception as e:
        messages.error(request, "Problem on save orderentity Error {}".format(e))
        return render(request, 'order_execute.html')


    if settings.SEND_EMAIL:

        #send Email with Consent Attachments

        subject = 'Neuer Vertrag'
        from_email = 'postmaster@beelze-solutions.de'
        to = 'sebastian.jung2@gmx.de'
        text_content = 'That’s your plain text.'


        template_name = "email_template.html"

        base_url = "{0}://{1}".format(request.scheme, request.get_host(),)
        context['products'] = productentry
        context['password'] = password
        context['username'] = username
        context['url'] = base_url
        context['order'] = orderentity
        convert_to_html_content = render_to_string(
            template_name=template_name,
            context=context
        )
        html_content = convert_to_html_content
        message = EmailMultiAlternatives(subject, text_content, from_email, [to])
        message.attach_alternative(html_content, "text/html")

        #und danach anhängen dieser Dokumente
        for consent in consent_list:
            if 'downloadurl' in consent:

                message.attach_file("{}{}".format(dir,consent['filename']), 'application/pdf')
        try:

            message.send()
        except Exception as e:

            messages.error(request, "Message send Error {}".format(e))
            return render(request, 'summary.html',context=context)

    #insert in cdc a new user with consent data

    preferences = '{'

    for count,consent in enumerate(consent_list):

        if count > 0:

            preferences += ","


        splitentrys = consent['key'].split(".")

        if len(splitentrys) == 2:

            preferences += '"{}":'.format(splitentrys[0])
            preferences += '{'
            preferences += '"{}":'.format(splitentrys[1])

        else:

            preferences += '"{}":'.format(splitentrys[0])
        preferences += '{"isConsentGranted": true, "actionTimestamp": "2024-08-12T14:24:11.707Z","lastConsentModified": "2024-08-12T14:24:11.707Z"}'
        #preferences += ',"customdata":[{"key": "order_id","value": "1234"}]}'
        #orderentity.id


        if len(splitentrys) == 2:
             preferences += '}'

    preferences += '}'
    accountdata = {"address":(str(context["address"])+str(context["number"])),"firstName":context["firstname"], "lastName":context["lastname"], "email": context["email"],"city":context['city'],"zip": context['zip']}

    payload = {

        'UID': str(userentry.id),
        'profile': str(accountdata)

    }
    if preferences is not None:

        payload["preferences"] = str(preferences)
    print("Payload "+str(payload))
    try:
        insert_FullAccount(payload)

    except Exception as e:

        messages.error(request, "Insert Fullaccount Error {}".format(e))
        return render(request, 'summary.html',context=context)
    if settings.SEND_EMAIL:
        messages.info(request, "Wir haben ihre Bestellung erhalten. Sie haben von uns eine E-Mail mit den zugehörigen Vertragsdaten und Zugangsdaten zu dem Login Bereich erhalten")
    else:
        messages.info(request, "Wir haben ihre Bestellung erhalten und melden uns bei ihnen")

    return redirect('home')


class order_line(CookieWizardView):

    form_list = [preselection_Form,product_Form, CustomerInfoForm,ConsentForm]


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
        step = self.get_step_index()

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

        context['step'] = step

        jsoncontext = json.dumps(context_json)

        context.update({'json': jsoncontext})


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

