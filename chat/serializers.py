from rest_framework import serializers
from .models import Contact
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'last_login']


class ContactSerializer(serializers.ModelSerializer):
    contact_id = UserSerializer(many=True)
    contact_owner_id = UserSerializer()

    class Meta:
        model = Contact
        fields = ['contact_owner_id', 'contact_id']


