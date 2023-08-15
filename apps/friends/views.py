from .serializers import RelationSerializer
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from apps.authentication.models import User

class InviteFriendView(ViewSet):
    serializer_class = RelationSerializer
    permission_classes = (IsAuthenticated,)
    def create(self,request):
        user_1 = request.user
        user_2 = User.objects.get(username=request.data['targetName'])
        serializer = self.serializer_class(data={'user_1':user_1,'user_2':user_2})
        serializer.is_valid(raise_exception=True)
        return serializer.create()
    def update(self,request):
        user_1 = request.user
        user_2 = User.objects.get(username=request.data['targetName'])
        serializer = self.serializer_class(data={'user_1':user_1,'user_2':user_2})
        serializer.is_valid(raise_exception=True)
        return serializer.update()