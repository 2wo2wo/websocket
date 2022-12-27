from django.http import HttpResponse
def chat_auth(func):
    def wrap_func(request, contact_id, user_id):
        if request.user.id == user_id:
            return func(request, contact_id, user_id)
        else:
            return HttpResponse('you are not allowed')
    return wrap_func
