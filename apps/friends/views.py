from itertools import chain
from .serializers import FriendshipSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.authentication.models import User
from rest_framework.response import Response
from rest_framework import status
from .models import Friendship
from django.db.models import Q
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.shortcuts import render

class InviteFriendView(ViewSet):
    serializer_class = FriendshipSerializer
    permission_classes = (IsAuthenticated,)
    def create(self,request):
        inviter = request.user.username
        accepter = request.data['accepter']
        serializer = self.serializer_class(data={'inviter': inviter,'accepter': accepter})
        serializer.is_valid(raise_exception=True)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(f"friends_{accepter}",{'type':'friend.invite','invite':{'username':inviter}})
        return serializer.create(serializer.validated_data)
    def update(self,request):
        serializer = self.serializer_class(data={'inviter':request.user.username,'accepter':request.data['accepter']})
        serializer.is_valid(raise_exception=True)
        return serializer.update(serializer.validated_data)


class GetFriendshipStatusView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, username=None):
        try:
            return Response({"status":Friendship.objects.get(inviter=request.user.id,accepter=User.objects.get(username=username).id).get_status_display()},status=status.HTTP_200_OK)
        except Friendship.DoesNotExist:
            try:
                friendship = Friendship.objects.get(inviter=User.objects.get(username=username).id,accepter=request.user.id).get_status_display()
                if Friendship == "Заявка отправлена":
                    return Response({"status":"Есть входящая заявка"},status=status.HTTP_200_OK)
                return Response({"status":friendship},status=status.HTTP_200_OK)
            except Friendship.DoesNotExist:
                return Response({"status":"Ничего"},status=status.HTTP_200_OK)
        
class FriendListView(APIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer
    def get(self, request, username=None):
        try:
            targetId = User.objects.get(username=username).id
            friendships = Friendship.objects.filter(
                (Q(inviter=targetId) | Q(accepter=targetId)) & Q(status=1)
            )

            friends = [
                {
                    'username': friendship.inviter.username if friendship.inviter != request.user else friendship.accepter.username,
                }
                for friendship in friendships
            ]

            return Response(friends, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'detail':"Not found"},status=status.HTTP_404_NOT_FOUND)
        
class FindUserView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = UserSerializer
    def get(self, request,value=None):
        users = User.objects.filter(username__startswith=value).exclude(id=request.user.id) 
        if not users.exists():
            return Response({"detail":"Not found"},status=status.HTTP_404_NOT_FOUND)
        return Response(users.values('username','photo'),status=status.HTTP_200_OK)
        

def test(request):
    return render(request,template_name='test.html')
    