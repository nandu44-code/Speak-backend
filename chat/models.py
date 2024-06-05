from django.db import models
from Users.models import CustomUser
# Create your models here.
class Message(models.Model):

    sender = models.ForeignKey(CustomUser, on_delete = models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(CustomUser, on_delete = models.CASCADE,related_name='reciever')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"From: {self.sender.first_name} To: {self.receiver.first_name}"