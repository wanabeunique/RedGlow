from rest_framework import serializers
from apps.authentication.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    steamIdExists = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('username','phoneNumber','email','decency','reports','photo','background','subExpiresIn','date_joined','steamIdExists')
    
    def get_steamIdExists(self, obj):
        return obj.steamId is not None
    
class UserForeignSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','photo','background','subExpiresIn','date_joined')

class UserPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('photo',)

class UserBackgroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('background',)

class UserSteamSerializer(serializers.ModelSerializer):
    steamId = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('steamId',)