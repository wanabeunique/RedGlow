import json
from rest_framework import serializers
from apps.authentication.models import User
from apps.authentication.sending import connectToRedis
from apps.authentication.tasks import sendInfo, sendLink
from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings

class ChangePasswordSerializer(serializers.Serializer):
    currentPassword = serializers.CharField(max_length=255, min_length=8)
    newPassword = serializers.CharField(max_length=255, min_length=8)
    def validate(self, data):
        if data.get('currentPassword') is None:
            raise serializers.ValidationError(
                'Поле "Текущий пароль" не может быть пустым'
            )
        if data.get('newPassword') is None:
            raise serializers.ValidationError(
                'Поле "Новый пароль" не может быть пустым'
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
        r = connectToRedis()
        if r.exists(email):
            raise serializers.ValidationError(
                'Повторите попытку снова, когда срок предыдущей ссылки закончится'
            )
        r.close()
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "Неправильный адрес электронной почты"
            )
        return data
    def save(self):
        email = self.validated_data.get('email')
        username = User.objects.get(email=email).username
        sendLink.delay(
            username,"Ссылка для смены пароля на нашей платформе.",
            "Восстановление пароля",{"email":email},"/forgot/password/"
        )

class ForgotPasswordChangeSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, min_length=8,write_only=True)
    code = serializers.CharField()


    def validate(self, data):
        code = data.get('code')
        password = data.get('password')
        if code is None:
            raise serializers.ValidationError(
                'Некорректная ссылка'
            )
        if password is None:
            raise serializers.ValidationError(
                'Пароль обязателен'
            )

        r = connectToRedis()
        if not r.exists(code):
            raise serializers.ValidationError(
                'Срок действия ссылки истек'
            )
        data['email'] = json.loads(r.get(code)).get('email')
        r.delete(code)

        r.close()

        return data
    
    def save(self):
        user = User.objects.get(email=self.validated_data['email'])
        user.set_password(self.validated_data['password'])
        user.save()
        sendInfo.delay(user.email,user.username,
                info="Пароль от вашего аккаунта был изменён",
                subject='Смена пароля'
        )