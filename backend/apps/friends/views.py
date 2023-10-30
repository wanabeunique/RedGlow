from .serializers import FriendshipSerializer
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from apps.authentication.models import User
from rest_framework.response import Response
from rest_framework import status
from .models import Friendship
from django.db.models import Q, F, When, Case, ExpressionWrapper, BigIntegerField
from django.shortcuts import render
from django.utils.decorators import method_decorator
from apps.caching.decorator import cache_response
from apps.caching.tools import delete_cache, get_cache_key, CachedResponse
from django.core.cache import cache
from itertools import chain


def deleteFriendCache(**kwargs):
    accepter = kwargs.get('accepter')
    inviter = kwargs.get('inviter')
    args = [
        ('friendshipStatus',f'/user/friendship/{accepter}/', inviter),
        ('friendshipStatus',f'/user/friendship/{inviter}/', accepter),
        ('friendList',f'/user/{inviter}/friend', None, True),
        ('friendList',f'/user/{accepter}/friend', None, True),
        ('inviteOutList','/user/invite/out',inviter),
        ('inviteOutList','/user/invite/out',accepter),
        ('inviteInList','/user/invite/in',inviter),
        ('inviteInList','/user/invite/in',accepter),
    ]
    for item in range(len(args)):
        args[item] = get_cache_key(*args[item])
    cache.delete_many(args)



class InviteFriendView(ViewSet):
    serializer_class = FriendshipSerializer
    permission_classes = (IsAuthenticated,)
    def create(self,request):
        inviter = request.user
        accepter = request.data['accepter']
        accepterId = User.objects.get(username=accepter).id
        serializer = self.serializer_class(data={'inviter': inviter.username,'accepter': accepter})
        serializer.is_valid(raise_exception=True)
        #deleteFriendCache(accepter=accepter,inviter=inviter.username)
        return serializer.create(serializer.validated_data)
    def update(self,request):
        accepter = request.data['accepter']
        inviter = request.user.username
        serializer = self.serializer_class(data={'inviter':inviter,'accepter': accepter})
        serializer.is_valid(raise_exception=True)
        #deleteFriendCache(accepter=accepter,inviter=inviter)
        return serializer.update(serializer.validated_data)

#@method_decorator(cache_response(start_name='friendshipStatus'), name='get')
class GetFriendshipStatusView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, username=None):
        inviter = request.user.id
        try:
            accepter = User.objects.get(username=username).id
        except User.DoesNotExist:
            return Response({'detail': 'Not found'},code=status.HTTP_404_NOT_FOUND)
        if inviter == accepter:
            return Response({'detail': 'Отправитель и приниматель должны быть разные'},code=status.HTTP_400_BAD_REQUEST)
        try:
            return Response({"status":Friendship.objects.get(inviter=inviter,accepter=accepter).get_status_display()})
        except Friendship.DoesNotExist:
            try:
                friendship = Friendship.objects.get(inviter=accepter,accepter=inviter).get_status_display()
                if friendship == "Заявка отправлена":
                    return Response({"status":"Есть входящая заявка"})
                return Response({"status":friendship})
            except Friendship.DoesNotExist:
                return Response({"status":"Ничего"})
            
#@method_decorator(cache_response(start_name='friendList',for_all=True), name='get')
class FriendListView(APIView):
    permission_classes = (IsAuthenticated, )
    
    def get(self, request, username=None,page=None):
        try:
            targetId = User.objects.get(username=username).id
            friends = Friendship.objects.filter(
                (Q(accepter=targetId) | Q(inviter=targetId)) & Q(status=1)
            ).prefetch_related('inviter', 'accepter').order_by(Case(
                    When(accepter__id=targetId, then=F('inviter__username')),
                    default=F('accepter__username')
                )
            ).values(
            username=Case(
                    When(accepter__id=targetId, then=F('inviter__username')),
                    default=F('accepter__username')
                ),
            photo=Case(
                    When(accepter__id=targetId, then=F('inviter__photo')),
                    default=F('accepter__photo')
                )
            )[page * 20 - 20: page * 20]
            return Response(friends)
        except User.DoesNotExist:
            return Response({'detail':"Not found"},code=status.HTTP_404_NOT_FOUND)
        
#@method_decorator(cache_response(start_name='inviteInList'), name='get')
class InviteInListView(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self,request,page=None):
        currentUserId = request.user.id

        friendships = Friendship.objects.filter(
            Q(accepter=currentUserId) & Q(status=0)
        ).prefetch_related('inviter').order_by('inviter__username').values(
            username = F('inviter__username'),
            photo = F('inviter__photo')
        )[page*20 - 20: page*20]
        return Response(friendships)


#@method_decorator(cache_response(start_name='inviteOutList'), name='get')
class InviteOutListView(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self,request,page=None):
        currentUserId = request.user.id

        friendships = Friendship.objects.filter(
            Q(inviter=currentUserId) & Q(status=0)
        ).prefetch_related('accepter').order_by('accepter__username').values(
            username = F('accepter__username'),
            photo = F('accepter__photo')
        )[page*20 - 20: page*20]
        return Response(friendships)

class SearchUserView(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request,value=None,page=None):
        targetId = request.user.id
        output = User.objects.filter(
            username__startswith=value
        ).exclude(id=targetId).exclude(id__in=Friendship.objects.filter(Q(inviter=targetId) | Q(accepter=targetId)).values(
            idCustom=Case(
                When(accepter=targetId, then=ExpressionWrapper(F('inviter'), output_field=BigIntegerField())),
                default=ExpressionWrapper(F('accepter'), output_field=BigIntegerField())
            ),
        )).order_by('username').values('username','photo')[page*20-20:page*20]
            
        return Response(output)
    
class SearchFriendView(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request, username=None, value=None, page=None):
        targetId = User.objects.get(username=username).id
        friends = Friendship.objects.prefetch_related('inviter', 'accepter').filter(
            ((Q(accepter=targetId) & Q(accepter__username__startswith=value)) | (Q(inviter=targetId) & Q(inviter__username__startswith=value))) & Q(status=1)
        ).order_by(Case(
                When(accepter__id=targetId, then=F('inviter__username')),
                default=F('accepter__username')
            )
        ).values(
            username=Case(
                    When(accepter__id=targetId, then=F('inviter__username')),
                    default=F('accepter__username')
                ),
            photo=Case(
                    When(accepter__id=targetId, then=F('inviter__photo')),
                    default=F('accepter__photo')
                )
        )[page * 20 - 20: page * 20]

        return Response(friends)

class SearchInviteInView(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request, value=None, page=None):
        currentUserId = request.user.id

        friendships = Friendship.objects.prefetch_related('inviter','accepter').filter(
            Q(accepter=currentUserId) & Q(accepter__username__startswith=value) & Q(status=0)
        ).order_by('inviter__username').values(
            username = F('inviter__username'),
            photo = F('inviter__photo')
        )[page*20 - 20: page*20]
        return Response(friendships)


class SearchInviteOutView(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request, value=None, page=None):
        currentUserId = request.user.id

        friendships = Friendship.objects.prefetch_related('inviter','accepter').filter(
            Q(inviter=currentUserId) & Q(inviter__username__startswith=value) & Q(status=0)
        ).order_by('accepter__username').values(
            username = F('accepter__username'),
            photo = F('accepter__photo')
        )[page*20 - 20: page*20]
        return Response(friendships)
    
class RetrieveCommonFriendsView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, username=None):
        targetId = User.objects.get(username=username).id
        currentUserId = request.user.id

        targetFriends = Friendship.objects.prefetch_related('inviter','accepter').filter((Q(inviter=targetId) | Q(accepter=targetId)) & Q(status=1)).values(
            username=Case(
                    When(accepter__id=targetId, then=F('inviter__username')),
                    default=F('accepter__username')
                ),
            photo=Case(
                    When(accepter__id=targetId, then=F('inviter__photo')),
                    default=F('accepter__photo')
                )
        )

        currentUserFriends = Friendship.objects.prefetch_related('inviter','accepter').filter((Q(inviter=currentUserId) | Q(accepter=currentUserId)) & Q(status=1)).values(
            username=Case(
                    When(accepter__id=currentUserId, then=F('inviter__username')),
                    default=F('accepter__username')
                ),
            photo=Case(
                    When(accepter__id=currentUserId, then=F('inviter__photo')),
                    default=F('accepter__photo')
                )
        )

        commonFriends = targetFriends.intersection(currentUserFriends)

        return Response(commonFriends)


class SearchCommonFriendsView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, username=None,value=None):
        targetId = User.objects.get(username=username).id
        currentUserId = request.user.id

        targetFriends = Friendship.objects.prefetch_related('inviter','accepter').filter(
                ((Q(inviter=targetId) & Q(inviter__username__startswith=value)) | (Q(accepter=targetId) & Q(accepter__username__startswith=value))) & Q(status=1)
            ).values(
            username=Case(
                    When(accepter__id=targetId, then=F('inviter__username')),
                    default=F('accepter__username')
                ),
            photo=Case(
                    When(accepter__id=targetId, then=F('inviter__photo')),
                    default=F('accepter__photo')
                )
        )

        currentUserFriends = Friendship.objects.prefetch_related('inviter','accepter').filter(
                ((Q(inviter=currentUserId) & Q(inviter__username__startswith=value)) | (Q(accepter=currentUserId) & Q(accepter__username__startswith=value))) & Q(status=1)
            ).values(
            username=Case(
                    When(accepter__id=currentUserId, then=F('inviter__username')),
                    default=F('accepter__username')
                ),
            photo=Case(
                    When(accepter__id=currentUserId, then=F('inviter__photo')),
                    default=F('accepter__photo')
                )
        )

        commonFriends = targetFriends.intersection(currentUserFriends)
        return Response(commonFriends)

def test(request):
    return render(request,template_name='test.html')
    