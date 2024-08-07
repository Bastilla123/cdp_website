
from rest_framework import serializers
from .models import *


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id","birthday", "gender", "phone", "address", "number", "city", "zip", "user"]
        extra_kwargs = {

            'user': {'required': False},
        }

    def create(self, validated_data):

        return Profile.objects.create(**validated_data)






