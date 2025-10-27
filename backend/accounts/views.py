from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
import random
from django.conf import settings

from .models import User, OTP, PasswordResetToken
from .serializers import (
    UserRegistrationSerializer, UserSerializer, OTPSerializer,
    PhoneVerificationSerializer, PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer
)

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    print(serializer.is_valid())
    if serializer.is_valid():
        user = serializer.save()
        # Send OTP for phone verification
        send_otp(user, 'phone_verification')
        return Response({
            'message': 'User registered successfully. Please verify your phone number.',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def send_otp(user, purpose):
    # Generate 6-digit OTP
    code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    expires_at = timezone.now() + timedelta(minutes=settings.OTP_EXPIRY_MINUTES)
    
    # Create OTP record
    OTP.objects.create(
        user=user,
        code=code,
        purpose=purpose,
        expires_at=expires_at
    )
    
    # In production, integrate with SMS service like Twilio
    print(f"OTP for {user.phone_number}: {code}")  # Remove this in production
    
    # TODO: Integrate with actual SMS service
    # send_sms(user.phone_number, f"Your OTP is: {code}")

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_phone(request):
    serializer = PhoneVerificationSerializer(data=request.data)
    if serializer.is_valid():
        phone_number = serializer.validated_data['phone_number']
        code = serializer.validated_data['code']
        
        try:
            user = User.objects.get(phone_number=phone_number)
            otp = OTP.objects.filter(
                user=user,
                code=code,
                purpose='phone_verification',
                expires_at__gt=timezone.now()
            ).first()
            
            if otp:
                user.is_phone_verified = True
                user.save()
                otp.delete()
                return Response({'message': 'Phone number verified successfully.'})
            else:
                return Response({'error': 'Invalid or expired OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def request_password_reset(request):
    serializer = PasswordResetRequestSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data.get('email')
        phone_number = serializer.validated_data.get('phone_number')
        
        try:
            if email:
                user = User.objects.get(email=email)
            else:
                user = User.objects.get(phone_number=phone_number)
            
            # Send OTP for password reset
            send_otp(user, 'password_reset')
            return Response({'message': 'Password reset OTP sent successfully.'})
            
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    serializer = PasswordResetConfirmSerializer(data=request.data)
    if serializer.is_valid():
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']
        
        try:
            reset_token = PasswordResetToken.objects.get(
                token=token,
                expires_at__gt=timezone.now()
            )
            user = reset_token.user
            user.set_password(new_password)
            user.save()
            reset_token.delete()
            return Response({'message': 'Password reset successfully.'})
            
        except PasswordResetToken.DoesNotExist:
            return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user