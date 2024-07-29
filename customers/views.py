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
import logging
logging.basicConfig(filename='api.log', format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.DEBUG)


@permission_classes([IsAuthenticated])
class APIProfileView(APIView):

    def get(self, request, *args, **kwargs):

        result = Profile.objects.all()
        serializers = ProfileSerializer(result, many=True)
        return Response({'status': 'success', "students": serializers.data}, status=200)

    def put(self, request, pk=None, *args, **kwargs):
        info = 'APIProfileView PUT Request id {} POST Data {}'.format(id,request.POST)
        print(info)
        id = request.POST.get('id')
        logging.info(info)

        if id is None:
            error = {"status": "error", "data": "No id was send. Please send attribute id with Post"}
            logging.error(error.format(id, request.POST))
            return Response(error,
                            status=status.HTTP_400_BAD_REQUEST)

        profilentry = Profile.objects.filter(pk=id).first()
        if not profilentry:
            error = {"status": "error", "data": "Profile can't be found with pk {}".format(id)}
            logging.exception(error)
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProfileSerializer(profilentry,data=request.data)
        if serializer.is_valid():
            serializer.save()
            info = {"status": "success", "data": serializer.data}
            logging.info(info)
            return Response(info, status=status.HTTP_200_OK)
        else:
            error = {"status": "error", "data": serializer.errors}
            logging.exception(error)
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        return Response({'method': 'PUT'})
    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            info = {"status": "success", "data": serializer.data}
            logging.info(info)
            return Response(info, status=status.HTTP_200_OK)
        else:
            error = {"status": "error", "data": serializer.errors}
            logging.exception(error)
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
                "birthdate":str(form.cleaned_data.get('birthday').isoformat()),
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

            new_ingest(cdp_event_list["change_profile"], data)  # Insert new event change_profile in cdp

            messages.success(request, 'Profile saved successfully')
        else:

            messages.error(request, form_validation_error(form))
        return redirect('profile')
@login_required(login_url='/login/')
def home(request):
    return render(request, 'home.html')