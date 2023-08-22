from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
from .sending import connectToRedis, sendLink
from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings
import json

class UserSignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(min_length=8,max_length=255)
    confirmPassword = serializers.CharField(max_length=255,min_length=8,write_only=True)
    password = serializers.CharField(max_length=255,min_length=8,write_only=True)

    class Meta:
        model = User
        fields = ('username','password','confirmPassword','email','phoneNumber')

    def validate(self,data):
        if data['password'] != data['confirmPassword']:
            raise serializers.ValidationError(
                "Пароли должны совпадать!"
            )
        r = connectToRedis()
        if r.exists(data["email"]):
            raise serializers.ValidationError(
                "Повторите ещё раз, когда срок действия предыдущего кода истечёт"
            )
        data.pop('confirmPassword')
        return data
    def save(self):
        sendLink(
            self.validated_data['email'],self.validated_data['username'],
            "Ссылка для завершения регистрации на нашей платформе","Завершение регистрации на нашей платформе",
            self.validated_data, '/signUp/confirm'
        )

class KeySerializer(serializers.Serializer):
    key = serializers.CharField()

    def validate(self, data):
        key = data.get('key')

        f = Fernet(settings.CR_KEY)
        try:
            email = f.decrypt(bytes(key,encoding='utf-8')).decode()
        except InvalidToken as error:
            raise serializers.ValidationError(
                "Неверный код"
            )
        r = connectToRedis()
        if not r.exists(email):
            raise serializers.ValidationError(
                "Срок действия кода истёк"
            )
        r.close()
        return data
    

class KeySignUpSerializer(serializers.Serializer):
    key = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True,required=False)
    email = serializers.CharField(required=False)
    phoneNumber = serializers.CharField(required=False)

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
            data = json.loads(r.get(email))
            r.delete(email)
        else:
            raise serializers.ValidationError(
                "Срок действия кода истёк"
            )
        r.close()
        return data
    
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserLogInSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255,min_length=8,write_only=True)

    def validate(self,data):
        username = data['username']
        password = data['password']

        user = authenticate(username=username,password=password)

        if user is None:
            raise serializers.ValidationError(
                'Неправильное имя пользователя или пароль'
            )
        
        if not user.is_active:
            raise serializers.ValidationError(
                'Ваш аккаунт деактивирован'
            )
        
        return user