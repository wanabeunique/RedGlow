from .models import Relation
from apps.authentication.models import User
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

class RelationSerializer(serializers.ModelSerializer):
    inviter = serializers.SlugRelatedField(queryset=User.objects.all(),slug_field='username')
    accepter = serializers.SlugRelatedField(queryset=User.objects.all(),slug_field='username')
    class Meta:
        model = Relation
        fields = ('inviter','accepter')

    def validate(self,data):
        user_1 = data['inviter']
        user_2 = data['accepter']
        
        if user_1 == user_2:
            raise serializers.ValidationError(
                'Нельзя быть своим другом'
            )
        return data

    def create(self, validated_data):
        user_1 = validated_data['inviter']
        user_2 = validated_data['accepter']
        if Relation.objects.filter(inviter=user_2,accepter=user_1).exists():
            Relation.objects.filter(inviter=user_2,accepter=user_1).update(status=Relation.Status.FRIENDS)
            return Response({"detail":'Заявка успешно принята'},status=status.HTTP_202_ACCEPTED)
        else:
            Relation.objects.create(inviter=user_1,accepter=user_2,status=Relation.Status.INVITED)
            return Response({"detail":'Заявка успешно отправлена'},status=status.HTTP_201_CREATED)

    def update(self, validated_data):
        user_1 = validated_data['inviter']
        user_2 = validated_data['accepter']
        relation = Relation.objects.get(inviter=user_1,accepter=user_2)
        if relation.status == Relation.Status.INVITED:
            relation.delete()
            return Response({"detail":'Заявка успешно отменена'},status=status.HTTP_200_OK)
        if relation.status == Relation.Status.FRIENDS:
            relation.status = Relation.Status.INVITED
            relation.inviter = user_2
            relation.accepter = user_1
            relation.save()
            return Response({"detail":"Пользователь успешно удален из друзей"}, status=status.HTTP_202_ACCEPTED)