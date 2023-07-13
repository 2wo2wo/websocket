from .models import Contact
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ContactSerializer, UserSerializer


class ContactApi(APIView):

    def get(self, request, format=None, *args, **kwargs):
        user = request.user
        contacts = Contact.objects.get(contact_owner_id=user)
        contact_serializer = ContactSerializer(contacts)
        return Response(contact_serializer.data)

