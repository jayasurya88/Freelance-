from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ('freelancer', 'Freelancer'),
        ('client', 'Client'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE_CHOICES)

    def __str__(self):
        return self.user.username
