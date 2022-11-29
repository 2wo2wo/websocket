from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    text = models.TextField('Text')
    time_created = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, models.CASCADE)

    def __str__(self):
        return self.text