from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from django.utils.timezone import now


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    '''
    AbstractBaseUser, which is a minimal base class — it only includes:
        password
        last_login
        is_active, is_staff, etc. (if you include PermissionsMixin)
    '''
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    client_id = models.IntegerField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    xda_device_id = models.IntegerField()
    android_app_package_version_id = models.IntegerField(null=True)
    date_created = models.DateTimeField(default=now, editable=False)
    access_level = models.DecimalField(max_digits=2, decimal_places=0, default=9)
    signup_l2_intent = models.IntegerField(null=True)
    phone_verified = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField()

    objects = UserManager()

    '''
    When you define a custom Django user model, USERNAME_FIELD is required — even if you're not
    using it in authentication directly.
    
    It's a special attribute that tells Django:
    “This is the primary field used to identify a user.”
    Django uses it in:
        Admin login
        createsuperuser command
        AbstractBaseUser logic
        Some serializers or forms that rely on the user model
    '''

    USERNAME_FIELD = 'email'  # required, but we'll override login logic
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email or self.phone
    

class SignupTempSession(models.Model):
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    password = models.CharField(max_length=255)
    client_id = models.IntegerField()
    xda_device_id = models.IntegerField()
    android_app_package_version_id = models.IntegerField(null=True)
    date_created = models.DateTimeField(default=now, editable=False)
    access_level = models.DecimalField(max_digits=2, decimal_places=0, default=9)
    signup_l2_intent = models.IntegerField(null=True)
    phone_verified = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField()
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email or self.phone

