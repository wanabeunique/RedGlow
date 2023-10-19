from .serializers import FriendshipSerializer, FriendSerializer
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from apps.authentication.models import User
from rest_framework.response import Response
from rest_framework import status
from .models import Friendship
from django.db.models import Q
from django.shortcuts import render

class InviteFriendView(ViewSet):
    serializer_class = FriendshipSerializer
    permission_classes = (IsAuthenticated,)
    def create(self,request):
        inviter = request.user
        accepter = request.data['accepter']
        accepterId = User.objects.get(username=accepter).id
        if Friendship.objects.filter(inviter=inviter.id,accepter=accepterId).exists():
            return Response(data={'non_field_errors':['Заявка уже отправлена']},status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data={'inviter': inviter.username,'accepter': accepter})
        serializer.is_valid(raise_exception=True)
        return serializer.create(serializer.validated_data)
    def update(self,request):
        serializer = self.serializer_class(data={'inviter':request.user.username,'accepter':request.data['accepter']})
        serializer.is_valid(raise_exception=True)
        return serializer.update(serializer.validated_data)
    def retrieve(self,request):
        try:
            targetId = request.user.id
            friendships = Friendship.objects.filter(
                (Q(inviter=targetId) | Q(accepter=targetId)) & Q(status=1)
            )

            friends = [
                friendship.inviter if friendship.inviter.id != targetId else friendship.accepter
                
                for friendship in friendships
            ]
            serializer = FriendSerializer(data=friends,many=True)
            serializer.is_valid()

            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'detail':"Not found"},status=status.HTTP_404_NOT_FOUND)


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
    serializer_class = FriendSerializer
    def get(self, request, username=None):
        try:
            targetId = User.objects.get(username=username).id
            friendships = Friendship.objects.filter(
                (Q(inviter=targetId) | Q(accepter=targetId)) & Q(status=1)
            )

            friends = [
                friendship.inviter if friendship.inviter.id != targetId else friendship.accepter
                
                for friendship in friendships
            ]
            serializer = self.serializer_class(data=friends,many=True)
            serializer.is_valid()

            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'detail':"Not found"},status=status.HTTP_404_NOT_FOUND)

class InvitesListView(APIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = FriendSerializer
    def get(self,request,typeFlag=None):
        currentUserId = request.user.id
        if typeFlag == 'in':
            try:
                friendships = Friendship.objects.filter(
                    Q(accepter=currentUserId) & Q(status=0)
                ).values_list('inviter',flat=True)
                users = [
                    User.objects.get(id=user_id)
                    for user_id in friendships
                ]
                serializer = self.serializer_class(data=users,many=True)
                serializer.is_valid()
                return Response(serializer.data, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'detail':"Not found"},status=status.HTTP_404_NOT_FOUND)
        elif typeFlag == 'out':
            try:
                friendships = Friendship.objects.filter(
                    Q(inviter=currentUserId) & Q(status=0)
                ).values_list('accepter',flat=True)
                users = [
                    User.objects.get(id=user_id)
                    for user_id in friendships
                ]
                serializer = self.serializer_class(data=users,many=True)
                serializer.is_valid()
                return Response(serializer.data, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'detail':"Not found"},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'detail':"Неправильный тип"},status=status.HTTP_400_BAD_REQUEST)

class FindUserView(APIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = FriendSerializer
    def get(self, request,value=None,page=None):
        users = User.objects.filter(username__startswith=value).exclude(id=request.user.id)[page*10 - 10: page*10]
        if not users.exists():
            return Response({"detail":"Not found"},status=status.HTTP_404_NOT_FOUND)
        return Response(users.values('username','email'),status=status.HTTP_200_OK)
        

def test(request):
    return render(request,template_name='test.html')
    