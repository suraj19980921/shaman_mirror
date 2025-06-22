# accounts/auth_backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailOrPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = None
        if username:
            try:
                if '@' in username:
                    user = User.objects.get(email=username)
                else:
                    user = User.objects.get(phone=username)
            except User.DoesNotExist:
                return None

            if user.check_password(password):
                return user
        return None
