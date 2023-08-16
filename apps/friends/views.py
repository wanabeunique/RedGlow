from .serializers import RelationSerializer
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from apps.authentication.models import User
from rest_framework.response import Response
from rest_framework import status
from .models import Relation

class InviteFriendView(ViewSet):
    serializer_class = RelationSerializer
    permission_classes = (IsAuthenticated,)
    def create(self,request):
        serializer = self.serializer_class(data={'inviter':request.user.username,'accepter':request.data['targetName']})
        serializer.is_valid(raise_exception=True)
        return serializer.create(serializer.validated_data)
    def update(self,request):
        serializer = self.serializer_class(data={'inviter':request.user.username,'accepter':request.data['targetName']})
        serializer.is_valid(raise_exception=True)
        return serializer.update(serializer.validated_data)


class GetRelationStatusView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, targetName=None):
        try:
            return Response({"status":Relation.objects.get(inviter=request.user.id,accepter=User.objects.get(username=targetName).id).status.label},status=status.HTTP_200_OK)
        except:
            return Response({"status":Relation.objects.get(inviter=User.objects.get(username=targetName).id,accepter=request.user.id).status.label},status=status.HTTP_200_OK)