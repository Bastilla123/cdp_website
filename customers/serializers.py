import logging
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
from rest_framework.response import Response
from rest_framework import status

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id","birthday", "gender", "phone", "address", "number", "city", "zip", "user"]
        extra_kwargs = {

            'user': {'required': False},
        }

    def create(self, validated_data):

        return Profile.objects.create(**validated_data)

    def validate(self, data):
        request = self.context["request"]
        if request.method == "POST":
            username = '{}_{}'.format(request.data["first_name"], request.data["last_name"])
            password = 'secrets.token_urlsafe(13)'
            try:
                userentry = User.objects.create_user(username=username,
                                                 first_name=request.data["first_name"], last_name=request.data["last_name"],
                                                 email='',
                                                 password=password)
                userentry.save()
            except Exception as e:
                error = {"status": "error", "Error": "Error on saving User {}".format(e)}
                logging.exception(error)
                return Response(error, status=status.HTTP_400_BAD_REQUEST)

            data["user"] = userentry

        return data




