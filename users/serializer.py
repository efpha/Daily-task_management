'''
    convertion of userprofile model instances
    to json for APIs and back to model instanxce
'''

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import UserProfile
from django.contrib.auth.hashers import make_password

class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'name', 'email', 'password', 'date_created']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # password hashing before saving to db
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserProfileSerializer, self).create(validated_data)
