from django.db import models
from django.contrib.auth import get_user_model
import uuid


User = get_user_model()


class Message(models.Model):
    text = models.TextField('Text')
    time_created = models.DateTimeField(auto_now=True)
    sent_id = models.ForeignKey(User, models.CASCADE, related_name='sent_to')
    owner_id = models.ForeignKey(User, models.CASCADE, related_name='owner')

    def __str__(self):
        return self.text


class Contact(models.Model):
    contact_id = models.ManyToManyField(User, blank=True)
    contact_owner_id = models.ForeignKey(User, models.CASCADE, related_name='contact_owner', null=True)

    def __str__(self):
        return User.objects.get(pk=self.contact_owner_id.id).email + " 's contacts"


class Unique_room(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    users = models.ManyToManyField(User)

    def __str__(self):
        return str(self.id)


class VerificationUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    ver_code = models.CharField(max_length=6)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{ self.user.email }'s"
