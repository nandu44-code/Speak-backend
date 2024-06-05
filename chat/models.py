from django.db import models
from user.models import CustomUser
# Create your models here.
class Message(models.Model):

    sender = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    receiver = models.Foreignkey(CustomUser, on_delete = models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"From: {self.sender.first_name} To: {self.receiver.first_name}"