from django.contrib import auth
from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework.exceptions import AuthenticationFailed
from django.db import IntegrityError, transaction
from rest_framework import serializers
from rest_framework.settings import api_settings
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from .models import BBUser


class CreateBBUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания пользователя
    """
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = BBUser
        fields = ('id', 'email', 'phone', 'password')

    def validate(self, attrs):
        """
        Валидация телефона и пароля, для регистрации простых пользователей
        """
        user = BBUser(**attrs)
        password = attrs.get('password')
        phone = attrs.get('phone')
        if not len(phone):
            raise serializers.ValidationError({'phone': 'Phone not an empty field'})
        try:
            validate_password(password, user)
        except exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
            )
        return attrs

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")
        return user

    def perform_create(self, validated_data):
        with transaction.atomic():
            user = BBUser.objects.create_user(**validated_data)
        return user


class CreateStaffBBUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания пользователя с правами stuff
    """
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = BBUser
        fields = ('id', 'email', 'password')

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")
        return user

    def perform_create(self, validated_data):
        with transaction.atomic():
            user = BBUser.objects.create_stuff_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """
    Сериализатор для аутентификации пользователя
    """
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)

    class Meta:
        model = BBUser
        fields = ('email', 'password')

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again ' + str(email))

        if user.is_blocked:
            raise AuthenticationFailed('User is blocked, contact Admin')

        if not user.is_active:
            raise AuthenticationFailed('Account is not active')

        update_last_login(None, user)

        tokens = RefreshToken.for_user(user)

        return {
            'refresh': str(tokens),
            'access': str(tokens.access_token)
        }

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs


    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')