from rest_framework import serializers
from apps.authentication.models import User
import redis
from rest_framework import status

class ChangePasswordSerializer(serializers.Serializer):
    currentPassword = serializers.CharField(max_length=255,min_length=8)
    newPassword = serializers.CharField(max_length=255,min_length=8)
    confirmNewPassword = serializers.CharField(max_length=255,min_length=8)

    def validate(self, data):
        if data.get('newPassword') != data.get('confirmNewPassword'):
            raise serializers.ValidationError(
                'Поля Новый пароль, Подтвердите новый пароль должный совпадать'
            )
        return data

class ForgotPasswordCodeSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)

    def validate(self, data):
        email = data.get('email')
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"email":"Неправильный адрес электронной почты"}
            )
        return data
    
class ForgotPasswordChangeSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, min_length=8)
    confirmPassword = serializers.CharField(max_length=255, min_length=8)
    email = serializers.CharField(max_length=255)
    def validate(self, data):
        password = data.get('password')
        confirmPassword = data.get('confirmPassword')
        
        if password != confirmPassword:
            raise serializers.ValidationError(
                'Пароли должны совпадать'
            )
        return data