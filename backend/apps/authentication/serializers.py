from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
from apps.tools.tasks import sendLink, sendInfo
from django.core.cache import cache
import hashlib


class UserSignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def validate(self, data):
        email = data.get('email')
        if email is None:
            raise serializers.ValidationError(
                "Некорректные данные"
            )
        if User.objects.filter(username=data.get('username')).exists():
            raise serializers.ValidationError(
                "Данное имя пользователя занято"
            )
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "Данный адрес электронной почты уже зарегистрирован"
            )
        if cache.get(hashlib.sha256(email.encode('utf-8')).hexdigest()):
            raise serializers.ValidationError(
                "Повторите ещё раз, когда срок действия предыдущей ссылки истечёт"
            )
        return data

    def save(self):
        sendLink.delay(
            self.validated_data['username'],
            "Ссылка для завершения регистрации на нашей платформе", "Завершение регистрации на нашей платформе",
            self.validated_data, '/signUp/confirm'
        )


class KeySignUpSerializer(serializers.Serializer):
    email = serializers.CharField(required=False)
    code = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True, required=False)
    country = serializers.CharField(required=False, write_only=True)

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
        email = hashlib.sha256(email.encode('utf-8')).hexdigest()
        key = code+email
        data = cache.get(key)
        if not data:
            raise serializers.ValidationError(
                'Код неверный или срок его действия истек'
            )
        cache.delete(email)
        cache.delete(key)

        return data

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        sendInfo.delay(user.email, user.username,
                       info="Вы успешно зарегистрировались на нашей платформе!",
                       subject='Успешная регистрция на нашей платформе'
                       )
        return user


class UserLogInSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        if password is None:
            raise serializers.ValidationError(
                'Имя пользователя обязательно'
            )
        if username is None:
            raise serializers.ValidationError(
                'Пароль обязателен'
            )

        user = authenticate(
            self.context['request'], username=username, password=password)

        if user is None:
            raise serializers.ValidationError(
                'Неправильное имя пользователя или пароль'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'Ваш аккаунт деактивирован'
            )

        return user


class UserCheckerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'photo')

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