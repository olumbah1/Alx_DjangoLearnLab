from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError as DjangoValidationError

CustomUser = get_user_model()  # Get the custom user model dynamically

class UserRegistrationSerializer(serializers.ModelSerializer):  # Serializer for user registration
    password = serializers.CharField(write_only=True, min_length=6)  # Password field (write-only)
    password_confirm = serializers.CharField(write_only=True)  # Confirm password field (write-only)

    class Meta:
        model = CustomUser  # Use the custom user model
        fields = ['username', 'first_name', 'last_name', 'email', 'bio', 'password', 'password_confirm']  # Fields to serialize
        extra_kwargs = {
            'email': {'required': True},  # Email is required
            'username': {'required': True}  # Username is required
        }

    def validate_password(self, value):  # Validate password strength
        try:
            validate_password(value)  # Use Django's built-in validator
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages)  # Raise error if invalid
        return value  # Return validated password

    def validate_email(self, value):  # Check for duplicate email
        if CustomUser.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exist.")  # Raise error if email exists
        return value  # Return validated email

    def validate(self, attrs):  # Validate that passwords match
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("passwords don't match.")  # Raise error if not matching
        return attrs  # Return validated data

    def create(self, validated_data):  # Create a new user
        validated_data.pop('password_confirm')  # Remove password_confirm before saving
        user = get_user_model().objects.create_user(**validated_data)  # Create user with validated data
        Token.objects.create(user=user)  # Create auth token for the user
        return user  # Return created user

class UserLoginSerializer(serializers.Serializer):  # Serializer for login
    username = serializers.CharField()  # Username input
    password = serializers.CharField(write_only=True)  # Password input (write-only)

    def validate(self, attrs):  # Custom validation
        username = attrs.get('username')  # Get username
        password = attrs.get('password')  # Get password

        if username and password:  # Ensure both are provided
            user = authenticate(username=username, password=password)  # Authenticate user
            if not user:
                raise serializers.ValidationError("Invalid username and password")  # Invalid credentials
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled")  # Inactive user
            attrs['user'] = user  # Add user to validated data
            return attrs  # Return validated data
        else:
            raise serializers.ValidationError("Must include username and password")  # Missing fields

class UserProfileSerializer(serializers.ModelSerializer):  # Serializer for user profile
    followers_count = serializers.SerializerMethodField()  # Custom field for followers count
    following_count = serializers.SerializerMethodField()  # Custom field for following count
    is_following = serializers.SerializerMethodField()  # Whether current user is following this user

    class Meta:
        model = CustomUser  # Use custom user model
        fields = [  # Fields to include in the profile
            'id', 
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'bio', 
            'profile_picture',
            'followers_count',
            'following_count',
            'is_following',
            'date_joined'
        ]
        read_only_fields = ['id', 'username', 'date_joined', 'followers_count', 'following_count']  # Fields that can't be modified

    def get_followers_count(self, obj): return obj.followers.count()  # Count number of followers

    def get_following_count(self, obj): return obj.following.count()  # Count number of following

    def get_is_following(self, obj):  # Check if current user follows this user
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.is_following(obj)
        return False

class FollowSerializer(serializers.Serializer):  # Serializer for following/unfollowing
    user_id = serializers.IntegerField()  # User ID field

    def validate_user_id(self, value):  # Validate that user exists
        try:
            user = CustomUser.objects.get(id=value)  # Try to get user by ID
            return user  # Return user if found
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User does not exist")  # Raise error if not found

class UserListSerializer(serializers.ModelSerializer):  # Serializer for listing users
    followers_count = serializers.SerializerMethodField()  # Custom field for followers count
    following_count = serializers.SerializerMethodField()  # Custom field for following count
    is_following = serializers.SerializerMethodField()  # Whether current user is following this user

    class Meta:
        model = CustomUser  # Use custom user model
        fields = [  # Fields to show in user list
            'id',
            'username',
            'first_name',
            'last_name',
            'bio',
            'profile_picture',
            'followers_count',
            'following_count',
            'is_following'
        ]

    def get_followers_count(self, obj): return obj.followers.count()  # Count followers

    def get_following_count(self, obj): return obj.following.count()  # Count following

    def get_is_following(self, obj):  # Check if current user follows this user
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.is_following(obj)
        return False
