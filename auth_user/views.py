from django.shortcuts import render
from rest_framework import mixins, viewsets, status
from .serializers import SignupTempSessionSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User, SignupTempSession
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q

# Create your views here.
class UserViewset(viewsets.GenericViewSet):
    
    @action(detail=False, methods=['post'])
    def verify_user_email(self, request):
        email = request.data.get('email')
        phone = request.data.get('phone')
        user_contact = User.objects.filter(Q(email=email) | Q(phone=phone))
        if email and user_contact.email == email:
            return Response({'error_message': 'Email already exist'}, status=status.HTTP_400_BAD_REQUEST)
        if phone and user_contact.phone == phone:
            return Response({'error_message': 'Phone number already exist'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = SignupTempSessionSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save()
            # Send Otp on mail after registration and Login api will be completed
            return Response({"otp" : instance.otp}, status=status.HTTP_201_CREATED)
    

    @action(detail=False, methods=['post'])
    def verify_otp(self, request):
        client_otp = request.data.get('otp')
        email = request.data.get('email')
        if not client_otp:
            return Response({'error_message': 'OTP missing'}, status=status.HTTP_400_BAD_REQUEST)
        signup_temp_data = SignupTempSession.objects.filter(client_id = 1, otp = client_otp, email=email).values('first_name', 'last_name', 'email', 'phone', 'password', 'client_id', 'xda_device_id', 'android_app_package_version_id', 'date_created', 'access_level', 'signup_l2_intent', 'phone_verified', 'ip_address').first()
        if signup_temp_data:
            User.objects.create(**signup_temp_data)
            return Response({'success_message': 'User created successfully'},status=status.HTTP_201_CREATED)
        else:
            return Response({'error_message': 'OTP is not correct'}, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['post'])
    def login(self, request):
        email_or_phone = request.data.get('email')
        if not email_or_phone:
            email_or_phone = request.data.get('phone')
        if not email_or_phone:
            return Response({'error_message': 'email or phone is required'})
        
        password = request.data.get('password')
        if not password:
            return Response({'error_message': 'password is required'})
        
        user = authenticate(request, username=email_or_phone, password=password)
        if user:
            # Generate JWT token
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'phone': user.phone,
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error_message': 'No user found with these credentilas'})
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({'error_message': 'Refersh token is required'})
        
        try:
            refresh_token = RefreshToken(refresh_token)
            refresh_token.blacklist()
            return Response({"detail": "Logout successful."}, status= status.HTTP_200_OK)
        except:
            return Response({'error_message' : 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)