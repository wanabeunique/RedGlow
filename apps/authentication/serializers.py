from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from .models import User
from .code import connectToRedis

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
        r = connectToRedis()
        if r.exists(data["email"]):
            raise serializers.ValidationError(
                "Повторите ещё раз, когда срок действия предыдущего кода истечёт"
            )
        return data
    
class CodeSerializer(serializers.ModelSerializer):
    code = serializers.CharField(write_only=True)
    confirmPassword = serializers.CharField(max_length=128,min_length=8,write_only=True)
    password = serializers.CharField(max_length=128,min_length=8,write_only=True)
    class Meta:
        model = User
        fields = ('username','password','confirmPassword','email','phoneNumber','code')

    def validate(self, data):
        email = data.get('email')
        code = data.get('code')

        r = connectToRedis()
        if r.exists(email):
            actualCode = r.get(email).decode('utf-8')

            if code == actualCode:
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
        del data['confirmPassword']
        del data['code']
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