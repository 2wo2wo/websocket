from django.http import HttpResponse
from .models import Contact

def auth_user_chat_room(func):
    def wrapper_func(request, contact_id, user_id):
        if request.user.id == user_id:
            return func(request, contact_id, user_id)
        else:
            return HttpResponse('you are not allowed')
    return wrapper_func


def contacts_exists(func):
    def wrapper_func(request, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except Contact.DoesNotExist:
            contact = Contact.objects.create(contact_owner_id=request.user)
            contact.save()
            return func(request)
    return wrapper_func
