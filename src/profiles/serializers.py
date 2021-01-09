from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.conf import settings
from django.db import IntegrityError, transaction
from rest_framework import serializers
from rest_framework.settings import api_settings

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