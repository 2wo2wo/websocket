from .models import Contact
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ContactSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication


class ContactApi(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, format=None, *args, **kwargs):
        user = request.user
        contacts = Contact.objects.get(contact_owner_id=user)
        contact_serializer = ContactSerializer(contacts)
        return Response({
            'user': contact_serializer.data['contact_owner_id'],
            'contacts': contact_serializer.data['contact_id']
        })

# class

