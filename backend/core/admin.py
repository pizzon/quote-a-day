from django.contrib import admin
from .models import Quotes, SecondaryEmail, PhoneNumber
from django.contrib.auth.models import User


admin.site.register(Quotes)
admin.site.unregister(User)
admin.site.register(User)
admin.site.register(SecondaryEmail)
admin.site.register(PhoneNumber)

