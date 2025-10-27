from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, OTP

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)
    email2 = serializers.EmailField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'email2', 'password', 'password2')
    
    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        if attrs.get('email2') and attrs.get('email') != attrs.get('email2'):
            raise serializers.ValidationError({"email": "Email fields didn't match."})
        
        # validate username here unwanted characters also
        
        if User.objects.filter(username=attrs.get('username')).exists():
            raise serializers.ValidationError({"username": "Username is already taken."})

        if not attrs.get('username'):
            raise serializers.ValidationError({"username": "Username is required."})
        
        # accept only allowed characters in username
        if not attrs.get('username').isalnum():
            raise serializers.ValidationError({"username": "Username can only contain alphanumeric characters."})
        
        if len(attrs.get('username')) < 5:
            raise serializers.ValidationError({"username": "Username must be at least 5 characters long."})

        if User.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError({"email": "Email is already registered."})
        
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        validated_data.pop('email2', None)
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        return user

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id', 
            'first_name', 
            'last_name', 
            'username', 
            'email',   # <-- ADD THIS HERE
        )


class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ('code', 'purpose')

class PhoneVerificationSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    code = serializers.CharField(max_length=6)

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)
    
    def validate(self, attrs):
        if not attrs.get('email') and not attrs.get('phone_number'):
            raise serializers.ValidationError("Either email or phone number must be provided.")
        return attrs

class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])
    new_password2 = serializers.CharField()
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs