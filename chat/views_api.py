from drf_yasg.utils import swagger_auto_schema

from .models import Contact, VerificationUser, Message
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (ContactSerializer,
                          UserSerializer,
                          RegistrationSerializer,
                          VerificationSerializer,
                          MessageSerializer,
                          MessageSimpleSerializer)
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from . import views
from django.contrib.auth import get_user_model
from rest_framework import status
from .tasks import send_mail
import string
import random
from .views import chat_room_name
from .pagination import CustomNumberPagination
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics


User = get_user_model()


class ContactApi(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(responses={200: ContactSerializer(many=True)})
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
        # keyword = request.data['keyword']
        keyword = request.query_params.get('keyword', request.user.email)
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


def send_verification(to_email, ver_code):
    title = 'Chat App Confirmation'
    html_address = 'chat/email_template.html'
    context = {
        'ver_code': ver_code
    }
    send_mail(
        title=title,
        html_address=html_address,
        context=context,
        to_email=to_email
    )


def user_unactivated(email):
    user = User.objects.get(email=email)
    user.is_active = False
    user.save()
    verification_code, created = VerificationUser.objects.get_or_create(user=user)
    random_number = ''.join(random.choice(string.digits) for x in range(6))
    verification_code.ver_code = random_number
    verification_code.save()
    return random_number


class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(responses={200: RegistrationSerializer()})
    def post(self, request, format=None, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data['email']
            ver_code = user_unactivated(email)
            send_verification(email, ver_code)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def check_ver_codes(email, code):
    user = User.objects.get(email=email)
    ver_code = VerificationUser.objects.get(user=user).ver_code
    if str(ver_code) == str(code):
        user.is_active = True
        user.save()
        return True
    return False


class EmailVerificationAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(responses={200: VerificationSerializer()})
    def post(self, request, format=None, *args, **kwargs):
        serializer = VerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            ver_code = serializer.validated_data['ver_code']
            if check_ver_codes(email, code=ver_code):
                return Response({'message': 'success'}, status=status.HTTP_202_ACCEPTED)
            return Response({'message': 'Did not match'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({'message': 'not valid inputs'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class UsernameIconAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def put(self, request, format=None, *args, **kwargs):
        if User.objects.filter(username=request.data['username']).exists():
            return Response({'message': 'User exists'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': "Something went wrong"}, status=status.HTTP_502_BAD_GATEWAY)


class GetUniqueRoomAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, contact_id, format=None, *args, **kwargs):
        room_name = str(chat_room_name(contact_id, request.user.id))
        return Response({
            'room_name': room_name
        })


class UserMessagesHistory(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, format=None, *args, **kwargs):
        queryset = self.get_chats(request.user)
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_chats(self, user_id):
        q_user = Message.objects.filter(owner_id=user_id).order_by('-time_created')
        q_sent = Message.objects.filter(sent_id=user_id).order_by('-time_created')
        mes_u, mes_s = self.get_by_max_time(q_user), self.get_by_max_time(q_sent)
        return self.remove_duplicates(mes_u, mes_s)

    def remove_duplicates(self, fir_arr, sec_arr):
        i, j = 0, 0
        while j < len(sec_arr) and i < len(fir_arr):
            if fir_arr[i].sent_id.pk > sec_arr[j].owner_id.pk:
                fir_arr.insert(i, sec_arr[j])
                j, i = j + 1, i + 1
            elif fir_arr[i].sent_id.pk < sec_arr[j].owner_id.pk:
                i += 1
            else:
                fir_arr[i] = fir_arr[i] if fir_arr[i].time_created > sec_arr[j].time_created else sec_arr[j]
                j, i = j + 1, i + 1
        if j < len(sec_arr):
            fir_arr.extend(sec_arr[j:])
        fir_arr.sort(key=lambda x: x.time_created, reverse=True)
        return fir_arr

    def get_by_max_time(self, queryset, sender=True):
        user_history, cur = list(), 0
        for message in queryset:
            if message.sent_id == cur and sender:
                continue
            if message.owner_id == cur and not sender:
                continue
            cur = message.sent_id if sender else message.owner_id
            user_history.append(message)
        user_history.sort(key=lambda x: x.sent_id.pk if sender else x.owner_id.pk)
        return user_history

class MessageBetweenUsers(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = MessageSimpleSerializer
    pagination_class = CustomNumberPagination

    def get_queryset(self):
        contact_id = self.kwargs.get('contact_id')
        queryset_user = Message.objects.filter(owner_id=self.request.user, sent_id=contact_id)
        queryset_contact = Message.objects.filter(owner_id=contact_id, sent_id=self.request.user,)
        queryset = queryset_contact | queryset_user
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        page = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page)
