from rest_framework import serializers
from apps.authentication.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','phoneNumber','email','photo','decency','reports','subExpiresIn')

class UserPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('photo')