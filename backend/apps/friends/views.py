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
from apps.tools.caching import cache_response, CachedResponse, delete_cache
from django.shortcuts import get_object_or_404

@method_decorator(cache_response(start_name='friendship_status'), 'get')
class GetFriendshipStatusView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, username=None):
        if not User.objects.filter(username=username).exists():
            return Response({'detail': 'Not found'}, code=status.HTTP_404_NOT_FOUND)

        inviter = request.user.id

        accepter = User.objects.get(username=username).id

        if inviter == accepter:
            return CachedResponse({'detail': 'Отправитель и приниматель должны быть разные'}, code=status.HTTP_400_BAD_REQUEST)

        if Friendship.objects.filter(inviter=inviter, accepter=accepter).exists():
            return CachedResponse({"status": Friendship.objects.get(inviter=inviter, accepter=accepter).get_status_display()})

        if Friendship.objects.filter(inviter=accepter, accepter=inviter).exists():
            friendship = Friendship.objects.get(
                inviter=accepter, accepter=inviter).get_status_display()

            if friendship == "Заявка отправлена":
                return CachedResponse({"status": "Есть входящая заявка"})

            return CachedResponse({"status": friendship})

        return CachedResponse({"status": "Ничего"})


class FriendListView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, username=None, page=None):
        if not User.objects.filter(username=username).exists():
            return Response({'detail': "Not found"}, code=status.HTTP_404_NOT_FOUND)

        targetId = User.objects.get(username=username).id
        friends = Friendship.objects.filter(
            (Q(accepter=targetId) | Q(inviter=targetId)) & Q(status=Friendship.Status.FRIENDS)
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


class InviteInListView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, page=None):

        friendships = Friendship.objects.filter(
            Q(accepter=request.user.id) & Q(status=Friendship.Status.INVITED)
        ).prefetch_related('inviter').order_by('inviter__username').values(
            username=F('inviter__username'),
            photo=F('inviter__photo')
        )[page*20 - 20: page*20]
        return Response(friendships)


class InviteOutListView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, page=None):

        friendships = Friendship.objects.filter(
            Q(inviter=request.user.id) & Q(status=Friendship.Status.INVITED)
        ).prefetch_related('accepter').order_by('accepter__username').values(
            username=F('accepter__username'),
            photo=F('accepter__photo')
        )[page*20 - 20: page*20]
        return Response(friendships)


class SearchUserView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, value=None, page=None):
        targetId = request.user.id
        output = User.objects.filter(
            username__startswith=value
        ).exclude(id=targetId).exclude(id__in=Friendship.objects.filter(Q(inviter=targetId) | Q(accepter=targetId)).values(
            idCustom=Case(
                When(accepter=targetId, then=ExpressionWrapper(
                    F('inviter'), output_field=BigIntegerField())),
                default=ExpressionWrapper(
                    F('accepter'), output_field=BigIntegerField())
            ),
        )).order_by('username').values('username', 'photo')[page*20-20:page*20]

        return Response(output)


class SearchFriendView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, username=None, value=None, page=None):
        target_user = get_object_or_404(User, username=username)
        targetId = target_user.id
        friends = Friendship.objects.prefetch_related('inviter', 'accepter').filter(
            ((Q(accepter=targetId) & Q(accepter__username__startswith=value)) | (
                Q(inviter=targetId) & Q(inviter__username__startswith=value))) & Q(status=Friendship.Status.FRIENDS)
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

        friendships = Friendship.objects.prefetch_related('inviter', 'accepter').filter(
            Q(accepter=request.user.id) & Q(
                accepter__username__startswith=value) & Q(status=Friendship.Status.INVITED)
        ).order_by('inviter__username').values(
            username=F('inviter__username'),
            photo=F('inviter__photo')
        )[page*20 - 20: page*20]
        return Response(friendships)


class SearchInviteOutView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, value=None, page=None):

        friendships = Friendship.objects.prefetch_related('inviter', 'accepter').filter(
            Q(inviter=request.user.id) & Q(
                inviter__username__startswith=value) & Q(status=Friendship.Status.INVITED)
        ).order_by('accepter__username').values(
            username=F('accepter__username'),
            photo=F('accepter__photo')
        )[page*20 - 20: page*20]
        return Response(friendships)


class RetrieveCommonFriendsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, username=None):
        if not User.objects.filter(username=username).exists():
            return Response({'detail': "Not found"}, code=status.HTTP_404_NOT_FOUND)

        targetId = User.objects.get(username=username).id
        currentUserId = request.user.id

        targetFriends = Friendship.objects.prefetch_related('inviter', 'accepter').filter((Q(inviter=targetId) | Q(accepter=targetId)) & Q(status=Friendship.Status.FRIENDS)).values(
            username=Case(
                When(accepter__id=targetId, then=F('inviter__username')),
                default=F('accepter__username')
            ),
            photo=Case(
                When(accepter__id=targetId, then=F('inviter__photo')),
                default=F('accepter__photo')
            )
        )

        currentUserFriends = Friendship.objects.prefetch_related('inviter', 'accepter').filter((Q(inviter=currentUserId) | Q(accepter=currentUserId)) & Q(status=Friendship.Status.FRIENDS)).values(
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

    def get(self, request, username=None, value=None):
        target_user = get_object_or_404(User, username=username)
        targetId = target_user.id

        currentUserId = request.user.id

        targetFriends = Friendship.objects.prefetch_related('inviter', 'accepter').filter(
            ((Q(inviter=targetId) & Q(inviter__username__startswith=value)) | (
                Q(accepter=targetId) & Q(accepter__username__startswith=value))) & Q(status=Friendship.Status.FRIENDS)
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

        currentUserFriends = Friendship.objects.prefetch_related('inviter', 'accepter').filter(
            ((Q(inviter=currentUserId) & Q(inviter__username__startswith=value)) | (
                Q(accepter=currentUserId) & Q(accepter__username__startswith=value))) & Q(status=Friendship.Status.FRIENDS)
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
    return render(request, template_name='test.html')
