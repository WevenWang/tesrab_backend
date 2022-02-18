from socket import send_fds
from django.db.models.signals import pre_save
from django.contrib.auth.models import User

# this function sets the username to user email whenver user updates profile and save
def updateUser(sender, instance, **kwargs):
    user = instance
    if user.email != '':
        user.username = user.email

pre_save.connect(updateUser, sender=User)
