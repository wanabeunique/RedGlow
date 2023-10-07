from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
from .sending import connectToRedis
from .tasks import sendLink, sendInfo
from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings
import json
import requests
from celery import current_app

class UserSignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255,write_only=True)

    class Meta:
        model = User
        fields = ('username','password','email')

    def validate(self,data):
        r = connectToRedis()
        if r.exists(data["email"]):
            raise serializers.ValidationError(
                {"detail":"Повторите ещё раз, когда срок действия предыдущей ссылки истечёт"}
            )
        return data
    def save(self):
        sendLink.delay(
            self.validated_data['username'],
            "Ссылка для завершения регистрации на нашей платформе","Завершение регистрации на нашей платформе",
            self.validated_data, '/signUp/confirm'
        )

class KeySerializer(serializers.Serializer):
    key = serializers.CharField()
    code = serializers.CharField()

    def validate(self, data):
        code = data.get('code')
        key = data.get('key')
        if code is None:
            raise serializers.ValidationError(
                {"detail":"Некорректная ссылка"}
            )
        if key is None:
            raise serializers.ValidationError(
                {"detail":"Некорректная ссылка"}
            )
        r = connectToRedis()
        if not r.exists(code):
            raise serializers.ValidationError(
                {"detail":"Срок действия ссылки истёк"}
            )
        
        f = Fernet(settings.CR_KEY)
        try:
            emailTmp = f.decrypt(bytes(key,encoding='utf-8')).decode()
        except InvalidToken as error:
            raise serializers.ValidationError(
                {"detail":"Некорректная ссылка"}
            )
        
        email = json.loads(r.get(code)).get('email')
        if emailTmp != email:
            raise serializers.ValidationError(
                {"detail":"Срок действия ссылки истёк"}
            )
        
        r.close()
        return data
    

class KeySignUpSerializer(serializers.Serializer):
    key = serializers.CharField(required=False)
    code = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True,required=False)
    email = serializers.CharField(required=False)
    country = serializers.CharField(required=False, write_only=True)

    def validate(self, data):
        code = data.get('code')
        key = data.get('key')

        if code is None:
            raise serializers.ValidationError(
                "Некорректная ссылка"
            )
        if key is None:
            raise serializers.ValidationError(
                "Некорректная ссылка"
            )

        r = connectToRedis()
        if not r.exists(code):
            raise serializers.ValidationError(
                'Код неверный или срок его действия истек'
            )
        tmpData = json.loads(r.get(code))
        
        
        if key is None:
            raise serializers.ValidationError(
                "Некорректная ссылка"
            )
        f = Fernet(settings.CR_KEY)
        try:
            email = f.decrypt(bytes(key,encoding='utf-8')).decode()
        except InvalidToken as error:
            raise serializers.ValidationError(
                "Некорректная ссылка"
            )
        
        if email != tmpData.get('email'):
            raise serializers.ValidationError(
                'Ссылка некорректная или срок её действия истек'
            )

        data |= {"country":None}

        r.delete(code)
        r.close()
        return data
    
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        sendInfo.delay(user.email, user.username,
                info="Вы успешно зарегистрировались на нашей платформе!",
                subject='Успешная регистрция на нашей платформе'
        )
        return user

class UserLogInSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255,write_only=True)

    def validate(self,data):
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

        user = authenticate(self.context['request'],username=username,password=password)

        if user is None:
            raise serializers.ValidationError(
                'Неправильное имя пользователя или пароль'
            )
        
        if not user.is_active:
            raise serializers.ValidationError(
                'Ваш аккаунт деактивирован'
            )
        
        return user