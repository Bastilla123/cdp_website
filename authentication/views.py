from customers.models import Profile
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm, SignUpForm
from django.http import JsonResponse
from customers.forms import ContactForm
from app.bibliothek import new_ingest
from django.conf import settings
from django.utils.translation import gettext_lazy as _

cdp_event_list = settings.CDP_EVENT_LIST


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, user=request.user)

        if form.is_valid():
            print(request.user.profile.address)
            if request.user.is_authenticated:
                if (request.user.profile.zip is None):
                    zip = 0
                else:
                    zip = str(request.user.profile.zip)
                if (request.user.profile.address is None):
                    street = ""
                else:
                    street = str(request.user.profile.address)
                if (request.user.profile.number is None):
                    number = ""
                else:
                    number = str(request.user.profile.number)
                if (request.user.profile.city is None):
                    city = ""
                else:
                    city = str(request.user.profile.address)
                data = {
                    "email": request.user.email,
                    "subject": form.cleaned_data['subject'],
                    "message": form.cleaned_data['message'],
                    "firstname": request.user.first_name,
                    "lastname": request.user.last_name,
                    "street": street + " " + number,
                    "zip": zip,
                    "city": city


                }
            else:
                data = {
                "email": form.cleaned_data['email'],
                "subject": form.cleaned_data['subject'],
                "message": form.cleaned_data['message'],
                "firstname": form.cleaned_data['first_name'],
                "lastname": form.cleaned_data['last_name'],
                "street": form.cleaned_data['street'],
                "zip": form.cleaned_data['zip'],
                "city": form.cleaned_data['city'],


            }

            new_ingest(cdp_event_list["new_contact"],data) #Insert a new contact event in cdp
            # Process the form data here...
            return JsonResponse({'success': True})
        else:
            print("Errors: ".format(form.errors))
            return JsonResponse({'success': False, 'errors': form.errors})

    return redirect('/')

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            print("User "+str(user))
            if user is not None:
                login(request, user)

                if hasattr(request.user,'profile'):

                    if request.user.profile.address is None:

                        messages.error(request, _("Please enter complete profile data!"))
                        return redirect("/customers/profile/")
                    else:
                        p
                        return redirect("/home")
                        messages.error(request, _("Please enter complete profile data!"))
                        return redirect("/customers/profile/")
                else:

                    print("Else")
                    Profile(user=request.user).save()
                    messages.error(request, _("Please enter complete profile data!"))
                    print("Redirect")
                    return redirect("/customers/profile/")

            else:
                print("Invalid")
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'
            print("Error validating form")
    contactform = ContactForm()

    return render(request, "accounts/login.html", {"form": form, "msg": msg, "contactform": contactform})

from django.contrib.auth.models import User
def register_user(request):
    msg = None
    success = False

    if request.method == "POST":

        form = SignUpForm(request.POST)
        if form.is_valid():

            user = form.save()

            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")


            msg = 'User created - please <a href="/login">login</a>.'
            success = True

            #return redirect("/login/")

        else:

            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})
