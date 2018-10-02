from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    choices = (
        ('STUDENT','Student'),
        ('TEACHER','Teacher'),
        ('ADMIN','Admin'),
    )
    usertype = models.CharField(max_length=50,choices=choices)

    def __str__(self):
        return self.username