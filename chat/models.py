from django.db import models
from django.contrib.auth.models import User
import uuid
class Message(models.Model):
    text = models.TextField('Text')
    time_created = models.DateTimeField(auto_now=True)
    sent_id = models.ForeignKey(User, models.CASCADE, related_name='sent_to')
    owner_id = models.ForeignKey(User, models.CASCADE, related_name='owner')

    def __str__(self):
        return self.text

class Contact(models.Model):
    contact_id = models.ManyToManyField(User)
    contact_owner_id = models.ForeignKey(User, models.CASCADE, related_name='contact_owner')

    def __str__(self):
        return User.objects.get(pk=self.contact_owner_id.id).username + " 's contacts"


class Unique_room(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    first_user = models.ForeignKey(User, models.CASCADE, related_name='first_user')
    second_user = models.ForeignKey(User, models.CASCADE, related_name='second_user')

    def __str__(self):
        first = User.objects.get(pk=self.first_user.id).username
        second = User.objects.get(pk=self.second_user.id).username
        return first + ' and ' + second

