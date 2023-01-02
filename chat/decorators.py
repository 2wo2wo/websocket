from django.http import HttpResponse


def auth_user_chat_room(func):
    def wrapper_func(request, contact_id, user_id):
        if request.user.id == user_id:
            return func(request, contact_id, user_id)
        else:
            return HttpResponse('you are not allowed')
    return wrapper_func
