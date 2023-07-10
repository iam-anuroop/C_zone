from django.contrib.auth.models import AbstractUser
from django.db import models

class UserDetails(AbstractUser):
    fullname = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    mail_activation = models.BooleanField(default=False,null=True)

    def __str__(self):
        return self.fullname
    
