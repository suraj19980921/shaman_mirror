from django.contrib import admin
from .models import SignupTempSession, User
# Register your models here.

admin.site.register(SignupTempSession)
admin.site.register(User)