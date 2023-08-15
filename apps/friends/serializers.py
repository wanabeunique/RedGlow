from .models import Relation
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

class RelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relation
        fields = ('user_1','user_2',)
        depth = 1
        optional_fields = ['status', ]


    def create(self, validated_data):
        user_1 = validated_data['user_1']
        user_2 = validated_data['user_2']
        if Relation.objects.filter(user_1=user_2,user_2=user_1).exists():
            Relation.objects.filter(user_1=user_2,user_2=user_1).update(status=Relation.Status.FRIENDS)
            return Response('Заявка успешно принята',status=status.HTTP_202_ACCEPTED)
        else:
            Relation.objects.create(user_1=user_1,user_2=user_2,status=Relation.Status.INVITED)
            return Response('Заявка успешно создана',status=status.HTTP_201_CREATED)

    def update(self, validated_data):
        user_1 = validated_data['user_1']
        user_2 = validated_data['user_2']
        relation = Relation.objects.get(user_1=user_2,user_2=user_1)
        if relation.status == Relation.Status.INVITED:
            relation.delete()
            return Response('Заявка успешно отменена',status=status.HTTP_200_OK)
        if relation.status == Relation.Status.FRIENDS:
            relation.status = Relation.Status.INVITED
            relation.user_1 = user_2
            relation.user_2 = user_1
            relation.save()
            return Response("Пользователь успешно удален из друзей", status=status.HTTP_202_ACCEPTED)