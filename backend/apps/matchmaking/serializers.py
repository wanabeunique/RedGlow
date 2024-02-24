from rest_framework import serializers
from .models import UserBehavior, Game

class UserBehaviorSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBehavior
        fields = ('decency', 'reportsOwned', 'reportsGot')

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'