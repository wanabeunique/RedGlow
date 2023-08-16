from rest_framework import serializers
from apps.authentication.models import User
from apps.authentication.code import sendLink, connectToRedis

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

class ForgotPasswordLinkSerializer(serializers.Serializer):
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
        sendLink(email,username,"Ссылка для смены пароля на нашей платформе")

class HashSerializer(serializers.Serializer):
    key = serializers.CharField(max_length=255)
    def validate(self, data):
        r = connectToRedis()
        if not r.exists(data['key'].split("+")[-1]):
            raise serializers.ValidationError(
                'Неверная ссылка или срок действия ссылки истек',code=404
            )
        r.close()
        return data

class ForgotPasswordChangeSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, min_length=8)
    confirmPassword = serializers.CharField(max_length=255, min_length=8)
    key = serializers.CharField(max_length=255)
    def validate(self, data):
        email = data['key'].split("+")[-1]
        if data.get('password') is None:
            raise serializers.ValidationError(
                {"password":'Пароль обязателен'}
            )

        r = connectToRedis()
        if not r.exists(email):
            raise serializers.ValidationError(
                'Срок действия ссылки истек'
            )
        if r.exists(email):
            actualkey = r.get(email).decode('utf-8')
            if actualkey != data['key']:
                raise serializers.ValidationError(
                    'Некорректная ссылка'
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
        email = self.validated_data['key'].split("+")[-1]
        r = connectToRedis()
        r.delete(email)
        r.close()
        user = User.objects.get(email=email)
        user.set_password(self.validated_data['password'])
        user.save()