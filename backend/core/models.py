from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Quotes(models.Model):
    quote = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.quote

class PhoneNumber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.phone_number

class SecondaryEmail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    secondary_email = models.EmailField(max_length=254)

    def __str__(self):
        return self.secondary_email

    

