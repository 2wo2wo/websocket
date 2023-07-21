from django.contrib import admin
from .models import Contact, Message, Unique_room, VerificationUser

admin.site.register(Contact)
admin.site.register(Message)
admin.site.register(Unique_room)
admin.site.register(VerificationUser)