from .models import Friendship
from apps.authentication.models import User
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

class FriendshipSerializer(serializers.ModelSerializer):
    inviter = serializers.SlugRelatedField(queryset=User.objects.all(),slug_field='username')
    accepter = serializers.SlugRelatedField(queryset=User.objects.all(),slug_field='username')
    class Meta:
        model = Friendship
        fields = ('inviter','accepter')

    def validate(self,data):
        user_1 = data['inviter']
        user_2 = data['accepter']
        
        if user_1 == user_2:
            raise serializers.ValidationError(
                'Отправитель и получатель должны быть разные'
            )
        return data

    def create(self, validated_data):
        user_1 = validated_data['inviter']
        user_2 = validated_data['accepter']
        if Friendship.objects.filter(inviter=user_2,accepter=user_1).exists():
            Friendship.objects.filter(inviter=user_2,accepter=user_1).update(status=Friendship.Status.FRIENDS)
            return Response({"detail":'Заявка успешно принята'},status=status.HTTP_202_ACCEPTED)
        else:
            if Friendship.objects.filter(inviter=user_1,accepter=user_2).exists():
                return Response(data={'errors':['Заявка уже отправлена']},status=status.HTTP_400_BAD_REQUEST)
            Friendship.objects.create(inviter=user_1,accepter=user_2,status=Friendship.Status.INVITED)
            return Response({"detail":'Заявка успешно отправлена'},status=status.HTTP_201_CREATED)

    def update(self, validated_data):
        user_1 = validated_data['inviter']
        user_2 = validated_data['accepter']
        if Friendship.objects.filter(inviter=user_1,accepter=user_2).exists():
            friendship = Friendship.objects.get(inviter=user_1,accepter=user_2)
            if friendship.status == Friendship.Status.INVITED:
                friendship.delete()
                return Response({"detail":'Заявка успешно отменена'},status=status.HTTP_200_OK)
            if friendship.status == Friendship.Status.FRIENDS:
                Friendship.objects.filter(inviter=user_1,accepter=user_2).update(status=Friendship.Status.INVITED,inviter=user_2,accepter=user_1)
                return Response({"detail":"Пользователь успешно удален из друзей"}, status=status.HTTP_202_ACCEPTED)

        elif Friendship.objects.filter(inviter=user_2,accepter=user_1).exists():
            friendship = Friendship.objects.get(inviter=user_2,accepter=user_1)
            if friendship.status == Friendship.Status.INVITED:
                friendship.delete()
                return Response({"detail":'Заявка успешно отменена'},status=status.HTTP_200_OK)
            if friendship.status == Friendship.Status.FRIENDS:
                Friendship.objects.filter(inviter=user_1,accepter=user_2).update(status=Friendship.Status.INVITED,inviter=user_1,accepter=user_2)
                return Response({"detail":"Пользователь успешно удален из друзей"}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'detail':'Нечего удалять'},status=status.HTTP_404_NOT_FOUND)
        

class FriendSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    photo = serializers.ImageField()