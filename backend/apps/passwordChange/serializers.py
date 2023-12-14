import json
from rest_framework import serializers
from apps.authentication.models import User
from django.core.cache import cache
from django.contrib.auth.hashers import make_password
from apps.tools.tasks import sendInfo, sendLink
import hashlib


class ChangePasswordSerializer(serializers.Serializer):
    currentPassword = serializers.CharField(max_length=255, min_length=8)
    newPassword = serializers.CharField(max_length=255, min_length=8)
    def validate(self, data):
        if data.get('currentPassword') is None:
            raise serializers.ValidationError(
                {'currentPassword':'Поле не может быть пустым'}
            )
        if data.get('newPassword') is None:
            raise serializers.ValidationError(
                {"newPassword":'Поле не может быть пустым'}
            )
        return data

class ForgotPasswordEmailSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)

    def validate(self, data):
        email = data.get('email')
        if email is None:
            raise serializers.ValidationError(
                "Почта обязательна"
            )
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "Неправильный адрес электронной почты"
            )
        
        key = hashlib.sha256(email.encode('utf-8')).hexdigest()
        if cache.get(key):
            raise serializers.ValidationError(
                'Повторите попытку снова, когда срок предыдущей ссылки закончится'
            )

        return data
    def save(self):
        email = self.validated_data.get('email')
        username = User.objects.get(email=email).username
        sendLink.delay(
            username,"Ссылка для смены пароля на нашей платформе.",
            "Восстановление пароля",{"email":email},"/forgot/password/"
        )


class EmailCodeSerializer(serializers.Serializer):
    email = serializers.CharField()
    code = serializers.CharField()

    def validate(self, data):
        code = data.get('code')
        email = data.get('email')
        if code is None:
            raise serializers.ValidationError(
                "Некорректная ссылка"
            )
        if email is None:
            raise serializers.ValidationError(
                "Некорректная ссылка"
            )
        key = hashlib.sha256(email.encode('utf-8')).hexdigest()
        if not cache.get(key):
            raise serializers.ValidationError(
                "Срок действия ссылки истёк"
            )
        if not cache.get(code + key):
            raise serializers.ValidationError(
                "Срок действия ссылки истёк"
            )
        
        return data

class ForgotPasswordChangeSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, min_length=8,write_only=True)
    code = serializers.CharField(max_length=255)
    email = serializers.CharField(max_length=255)

    def validate(self, data):
        code = data.get('code')
        email = data.get('email')
        password = data.get('password')
        if email is None:
            raise serializers.ValidationError(
                'Некорректная ссылка'
            )
        if code is None:
            raise serializers.ValidationError(
                'Некорректная ссылка'
            )
        if password is None:
            raise serializers.ValidationError(
                'Пароль обязателен'
            )
        
        email = hashlib.sha256(email.encode('utf-8')).hexdigest()
        if not cache.get(email):
            raise serializers.ValidationError(
                'Срок действия ссылки истек'
            )
        if not cache.get(code+email):
            raise serializers.ValidationError(
                'Срок действия ссылки истек'
            )
        cache.delete(email)
        cache.delete(code+email)

        return data
    
    def save(self):
        user = User.objects.get(email=self.validated_data['email'])
        user.set_password(self.validated_data['password'])
        user.save()
        sendInfo.delay(self.validated_data['email'],user.username,
                info="Пароль от вашего аккаунта был изменён",
                subject='Смена пароля'
        )