from .models import Unique_room, Message, Contact
from asgiref.sync import sync_to_async

@sync_to_async
def save_message(unique_room, user_id, message):
    uniq_room = Unique_room.objects.get(id=unique_room)
    for user in uniq_room.users.all():
        if user.id == user_id:
            owner = user
        else:
            contact = user
    message = Message(text=message, sent_id=contact, owner_id=owner)
    message.save()
