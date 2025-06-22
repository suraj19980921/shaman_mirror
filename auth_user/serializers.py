from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import SignupTempSession, User
import random, socket

class SignupTempSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignupTempSession
        fields = ['first_name', 'last_name', 'email', 'phone', 'password']
        extra_kwargs = {
            'otp': {'read_only': True},  # don't require it from user input
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        validated_data['otp'] = random.randint(10000, 99999)
        validated_data['client_id'] = 1 # add whitelable client table and get data from there
        validated_data['xda_device_id'] = 1 # correct it later
        validated_data['ip_address'] = socket.gethostbyname(socket.gethostname())
        return SignupTempSession.objects.create(**validated_data)