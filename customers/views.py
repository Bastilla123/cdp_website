from django.db.models import Func

from django.db.models.functions import Greatest
from django.contrib.postgres.search import TrigramSimilarity,TrigramDistance
import secrets
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from customers.forms import ProfileForm, form_validation_error
from customers.models import Profile
from app.bibliothek import new_ingest
from django.conf import settings
from rest_framework.views import APIView
from .serializers import ProfileSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from .forms import  ContactForm
from jarowinkler import jarowinkler_similarity

from app.bibliothek import log
def appendList(l,element):
    l.append(element)
    return l
#gehe durch alle Profile und mache einen fuzzy search nach der jaro winkler Methode und gebe wenn ein Datensatz existiert mit einem Mindestscore > score_cutoff
    #den Höchstwert zurück
def fuzzy_search_profile(post_firstname,post_lastname,post_zip,post_city,post_email,score_cutoff):

    allprofiles = Profile.objects.all()
    newtable = []

    for profile in allprofiles:
        searchstring1 = "{} {} {} {}".format(profile.user.first_name,profile.user.last_name,profile.zip,profile.city)
        searchstring2 = "{} {} {} {}".format(post_firstname, post_lastname, post_zip, post_city)
        jaroscore = jarowinkler_similarity(searchstring1, searchstring2)
        if jaroscore > score_cutoff:


            templist = [profile.id,jaroscore]
            appendList(newtable,templist)

        searchstring1 = "{} {}".format(profile.user.email, profile.user.last_name)
        searchstring2 = "{} {} ".format(post_email, post_lastname)
        jaroscore = jarowinkler_similarity(searchstring1, searchstring2)

        if jaroscore > score_cutoff:
            templist = [profile.id, jaroscore]

            appendList(newtable,templist)

    #Rückgabe der id mit dem höchsten Score
    if len(newtable) > 0:
        return max(newtable, key=lambda x: x[1])
    else:
        return []






def pretty_request(request):
    headers = ''
    for header, value in request.META.items():
        if not header.startswith('HTTP'):
            continue
        header = '-'.join([h.capitalize() for h in header[5:].lower().split('_')])
        headers += '{}: {}\n'.format(header, value)

    return (
        '{method} HTTP/1.1\n'
        'Content-Length: {content_length}\n'
        'Content-Type: {content_type}\n'
        '{headers}\n\n'
        '{body}'
    ).format(
        method=request.method,
        content_length=request.META['CONTENT_LENGTH'],
        content_type=request.META['CONTENT_TYPE'],
        headers=headers,
        body=request.body,
    )
@permission_classes([IsAuthenticated])
class APIProfileView(APIView):

    def get(self, request, *args, **kwargs):

        result = Profile.objects.all()
        serializers = ProfileSerializer(result, many=True, context={"request": request},)
        return Response({'status': 'success', "students": serializers.data}, status=200)


    def post(self, request):


        info = 'APIProfileView POST Request Request {}'.format(request.data)
        log('i', info)

        post_firstname = request.data.get('first_name', None)
        post_lastname = request.data.get('last_name', None)
        post_zip = request.data.get('zip', None)
        post_city = request.data.get('city', None)
        post_email = request.data.get('email', None)


        if (post_lastname is None or post_firstname is None):

            error = {"status": "error",
                     "data": "Please send last_name and first_name with Post"}
            log('e', error)
            return Response(error,
                            status=status.HTTP_400_BAD_REQUEST)
        if ((post_lastname is None and post_email is None ) or (post_firstname is None and post_email is None ) or (post_zip is None and post_email is None ) or ( post_city is None and post_email is None )
        ) :

            error = {"status": "error",
                     "data": "Please send (first_name and last_name and zip and city ) or (last_name and email) with Post"}
            log('e', error)

            return Response(error,
                            status=status.HTTP_400_BAD_REQUEST)



        fuzzyprofiles = fuzzy_search_profile(post_firstname, post_lastname, post_zip, post_city, post_email, 0.95)


        #Update
        if fuzzyprofiles:

            profileentry = Profile.objects.filter(id=fuzzyprofiles[0]).first()

            if not profileentry:
                error = {"status": "error",
                         "data": "Profile can't be found with first_name {} last_name {}".format(post_firstname, post_lastname)}
                log('e', error)

                return Response(error, status=status.HTTP_400_BAD_REQUEST)

            serializer = ProfileSerializer(profileentry, data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.user = profileentry.user
                serializer.save()
                info = {"Update":"Update dataset because existing dataset are found with fuzzy search","status": "success", "data": serializer.data}
                log('i', info)

                return Response(info, status=status.HTTP_200_OK)
        #Insert
        else:
            counter = 0
            while 1:
                if counter == 5:
                    error = {"status": "error", "Error": "Es wurde versucht 5 mal einen random Username erfolglos zu erstellen. Versuchen Sie es nochmals"}
                    log('e', error)

                    return Response(error, status=status.HTTP_400_BAD_REQUEST)
                username = secrets.token_urlsafe(13)
                userentry = User.objects.filter(username=username).first()

                #when username is free then exit loop
                if not userentry:
                    break
                if userentry is None:
                    break
            password = secrets.token_urlsafe(13)
            try:
                userentry = User.objects.create_user(username=username,
                                                         first_name=request.data["first_name"], last_name=request.data["last_name"],
                                                         email='',
                                                         password=password)
                userentry.save()
            except Exception as e:
                error = {"status": "error", "Error": "Error on saving User {}".format(e)}
                log('e', error)

                return Response(error, status=status.HTTP_400_BAD_REQUEST)
            serializer = ProfileSerializer(data=request.data, context={"request": request})

            if serializer.is_valid(raise_exception=True):

                serializer.save(user=userentry)

                info = {"Insert":"Insert new dataset because no existing dataset are found with fuzzy search","status": "success", "data": serializer.data}
                log('i', info)

                return Response(info, status=status.HTTP_200_OK)
            else:
                error = {"status": "error", "data": serializer.errors}
                log('e', error)

                return Response(error, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(login_required(login_url='login'), name='dispatch')
class ProfileView(View):
    profile = None

    def dispatch(self, request, *args, **kwargs):
        self.profile, __ = Profile.objects.get_or_create(user=request.user)
        return super(ProfileView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        contactform = ContactForm(request.POST, user=request.user)

        context = {'contactform':contactform,'profile': self.profile,'profileform' :ProfileForm(instance=request.user.profile), 'segment': 'profile'}

        if (settings.BASE_TEMPLATE =='layouts/base-dark.html'):
            return render(request, 'customers/profile_dark.html', context)
        return render(request, 'customers/profile_light.html', context)





    def post(self, request):
        form = ProfileForm(request.POST, request.FILES, instance=self.profile)


        passwort_1 = request.POST.get('passwort_1',None)
        passwort_2 = request.POST.get('passwort_2',None)


        if form.is_valid():


             # here form has old password and we update new passwrd before saving form.  Yes you have rightonce we update passwrd and agaig
             #just save the form.save(() ) then passwrd is reverted with form password did you get it?~
            profile = form.save()
            profile.user.first_name = form.cleaned_data.get('first_name')
            profile.user.last_name = form.cleaned_data.get('last_name')
            profile.user.email = form.cleaned_data.get('email')
            profile.user.save()

            if (passwort_1 is not None  and passwort_1 != "" and passwort_2 is not None and passwort_2 != ""):
                u = User.objects.get(id=request.user.id)
                # import pdb;pdb.set_trace() try now
                u.set_password(passwort_1)
                u.save()
                messages.success(request, 'Password is successfully changed')
            cdp_event_list = settings.CDP_EVENT_LIST

            data = {

                "email": form.cleaned_data.get('email'),

                "firstname": form.cleaned_data.get('first_name'),
                "lastname": form.cleaned_data.get('last_name'),

                "gender":form.cleaned_data.get('gender'),
                "phone": form.cleaned_data.get('phone'),
                "street": form.cleaned_data.get('address'),
                "housenumber": form.cleaned_data.get('number'),
                "city": form.cleaned_data.get('city'),
                "zip": form.cleaned_data.get('zip'),



            }
            data['skype'] = form.cleaned_data['skype']
            data['facebook'] = form.cleaned_data['facebook']
            data['twitter'] = form.cleaned_data['twitter']
            data['linkedin'] = form.cleaned_data['linkedin']
            data['instagram'] = form.cleaned_data['instagram']
            data['dribble'] = form.cleaned_data['dribble']
            data['pinterest'] = form.cleaned_data['pinterest']

            birthdate = form.cleaned_data.get('birthday', None)
            if birthdate is not None:
                 data['birthdate'] = str(birthdate.isoformat())

            new_ingest(cdp_event_list["change_profile"], data)  # Insert new event change_profile in cdp

            messages.success(request, 'Profile saved successfully')
        else:

            messages.error(request, form_validation_error(form))
        return redirect('profile')
@login_required(login_url='/login/')
def home(request):
    return render(request, 'home.html')