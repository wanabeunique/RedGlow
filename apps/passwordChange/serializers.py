from rest_framework import serializers
from apps.authentication.models import User
from apps.authentication.sending import sendLink, connectToRedis
from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings

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

class ForgotPasswordEmailSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)

    def validate(self, data):
        email = data.get('email')
        r = connectToRedis()
        if r.exists(email):
            raise serializers.ValidationError(
                'Повторите попытку снова, когда срок предыдущей ссылки закончится'
            )
        r.close()
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"email":"Неправильный адрес электронной почты"}
            )
        return data
    def save(self):
        email = self.validated_data.get('email')
        username = User.objects.get(email=email).username
        sendLink(
            email,username,"Ссылка для смены пароля на нашей платформе.",
            "Восстановление пароля",username,"/forgot/password/"
        )

class ForgotPasswordChangeSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, min_length=8)
    confirmPassword = serializers.CharField(max_length=255, min_length=8)
    key = serializers.CharField()

    def validate(self, data):
        key = data.get('key')
        f = Fernet(settings.CR_KEY)
        try:
            email = f.decrypt(bytes(key,encoding='utf-8')).decode()
        except InvalidToken as error:
            raise serializers.ValidationError(
                "Срок действия кода истёк"
            )
        r = connectToRedis()
        if r.exists(email):
            data['email'] = email
            r.delete(email)
        else:
            raise serializers.ValidationError(
                "Срок действия кода истёк"
            )
        r.close()

        password = data.get('password')
        confirmPassword = data.get('confirmPassword')
        
        if password != confirmPassword:
            raise serializers.ValidationError(
                'Пароли должны совпадать'
            )
        
        return data
    
    def save(self):
        user = User.objects.get(email=self.validated_data['email'])
        user.set_password(self.validated_data['password'])
        user.save()