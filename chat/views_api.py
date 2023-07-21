from .models import Contact
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ContactSerializer, UserSerializer, RegistrationSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from . import views
from django.contrib.auth.models import User
from rest_framework import status
from .tasks import send_mail
import string
import random


class ContactApi(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, format=None, *args, **kwargs):
        user = request.user
        contacts, created = Contact.objects.get_or_create(contact_owner_id=user)
        contact_serializer = ContactSerializer(contacts)
        return Response({
            'user': contact_serializer.data['contact_owner_id'],
            'contacts': contact_serializer.data['contact_id']
        })


class ContactSearchApi(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, format=None, *args, **kwargs):
        keyword = request.data['keyword']
        users_found = views.search_by_key(keyword)
        user_serializer = UserSerializer(users_found, many=True)
        return Response({
         "users": user_serializer.data
        })


class AddUserContactApi(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, format=None, *args, **kwargs):
        user_id = request.data['user_id']
        try:
            user_add = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'message': 'user not found'})
        user_contacts, created = Contact.objects.get_or_create(contact_owner_id=request.user)
        user_contacts.contact_id.add(user_add)
        return Response({'message': 'user_added'})


def send_verification(username, to_email):
    title = 'Chat App Confirmation'
    html_address = 'chat/email_template.html'
    ver_code = ''.join(random.choice(string.digits) for x in range(6))
    context = {
        'username': username,
        'ver_code': ver_code
    }
    send_mail(
        title=title,
        html_address=html_address,
        context=context,
        to_email=to_email
    )


def user_unactivated(username):
    user = User.objects.get(username=username)
    user.is_active = False
    user.save()


class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            username= serializer.validated_data['username']
            email = serializer.validated_data['email']
            user_unactivated(username)
            send_verification(username, email)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailVerificationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self):
        pass


