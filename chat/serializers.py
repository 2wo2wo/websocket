from rest_framework import serializers
from .models import Contact, Message
from django.contrib.auth import get_user_model
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'last_login', 'first_name', 'last_name', 'photo_url', 'icon_id', 'username']


class ContactSerializer(serializers.ModelSerializer):
    contact_id = UserSerializer(many=True)
    contact_owner_id = UserSerializer()

    class Meta:
        model = Contact
        fields = ['contact_owner_id', 'contact_id']


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {
            'email': {'required': True},
            'password': {'required': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class VerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    ver_code = serializers.CharField()


class MessageSerializer(serializers.ModelSerializer):
    contact = serializers.SerializerMethodField('get_friend')

    class Meta:
        model = Message
        fields = ['id', 'text', 'time_created', 'contact']

    def get_friend(self, obj):
        user_id = self.context.get("user_id")
        if obj.owner_id.pk == user_id.pk:
            res = obj.sent_id
        else:
            res = obj.owner_id
        return UserSerializer(res).data


class MessageSimpleSerializer(serializers.ModelSerializer):
    message = serializers.CharField(source='text')

    class Meta:
        model = Message
        fields = ['id', 'message', 'time_created', 'owner_id', 'sent_id']

