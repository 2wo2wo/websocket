from django.db import models
from django.contrib.auth.models import User

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

