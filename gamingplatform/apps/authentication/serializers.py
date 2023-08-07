from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from .models import User
import redis

class UserSignUpSerializer(serializers.ModelSerializer):
    confirmPassword = serializers.CharField(max_length=128,min_length=8,write_only=True)
    password = serializers.CharField(max_length=128,min_length=8,write_only=True)
    class Meta:
        model = User
        fields = ('username','password','confirmPassword','email','phoneNumber')

    def validate(self,data):
        if data['password'] != data['confirmPassword']:
            raise serializers.ValidationError(
                "Пароли должны совпадать!"
            )
        r = redis.StrictRedis(host='localhost', port=6379, db=0, password='SeMeN4565', socket_timeout=None, connection_pool=None, charset='utf-8', errors='strict', unix_socket_path=None)
        if r.exists(data["email"]):
            raise serializers.ValidationError(
                "Повторите ещё раз, когда срок действия предыдущего кода истечёт"
            )
        return data
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSignUpSerializer, self).create(validated_data)

class CodeSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    code = serializers.CharField()
    doDelete = serializers.BooleanField()

    def validate(self, data):
        email = data.get('email')
        code = data.get('code')
        doDelete = data.get('doDelete')
        r = redis.StrictRedis(host='localhost', port=6379, db=0, password='SeMeN4565', socket_timeout=None, connection_pool=None, charset='utf-8', errors='strict', unix_socket_path=None)
        if r.exists(email):
            actualCode = r.get(email).decode('utf-8')

            if code == actualCode:
                if doDelete:
                    r.delete(email)
            else:
                raise serializers.ValidationError(
                    {"code":"Неверный код"}
                )
        else:
            raise serializers.ValidationError(
                {"code":"Время действия кода истекло. Попробуйте ещё раз"}
            )
        r.close()
        return data

class UserLogInSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255,min_length=8)

    def validate(self,data):
        username = data['username']
        password = data['password']

        if username is None:
            raise serializers.ValidationError(
                'Имя пользователя обязательно для авторизации'
            )
        
        if password is None:
            raise serializers.ValidationError(
                'Пароль обязателен для авторизации'
            )

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