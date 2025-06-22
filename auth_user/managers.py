from django.contrib.auth.models import BaseUserManager
import socket

class UserManager(BaseUserManager):
    def create_user(self, email_or_phone, password=None, **extra_fields):
        if not email_or_phone:
            raise ValueError("The Email or Phone must be set")

        if '@' in email_or_phone:
            extra_fields['email'] = email_or_phone
        else:
            extra_fields['phone'] = email_or_phone

        user = self.model(**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields |= {
            'is_staff': True,
            'is_superuser': True,
            'client_id': 1,
            'xda_device_id': 1,
            'access_level': 0,
            'ip_address': socket.gethostbyname(socket.gethostname())
        }
        return self.create_user(email, password=password, **extra_fields)
