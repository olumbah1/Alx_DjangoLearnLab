from rest_framework import serializers
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name','email', 'password_confirm','password']
        extra_kwargs = {
            'email': {'required':True},
            'username': {'required':True}     # Make email and username required
        }
    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
          raise serializers.ValidationError(e.messages)
        return value  
     
    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exist.")
        return value
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("passwords don't match.")
        return attrs
            
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = CustomUser.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user
        
    
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Invalid username and password")
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled")
            attrs['user']=user
            return attrs
        else:
            raise serializers.ValidationError("Must include username and password")
    
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'profile_picture', 'username', 'first_name', 'last_name', 'email', 'bio', 'password_confirm', 'password', 'date_joined']
        read_only_fields = ['id', 'username', 'date_joined']
