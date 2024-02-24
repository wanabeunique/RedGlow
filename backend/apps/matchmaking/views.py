from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserBehaviorSerializer, GameSerializer
from .models import Game
from django.utils.decorators import method_decorator
from apps.tools.caching import cache_response, CachedResponse

class RetrieveUserBehaviorView(RetrieveAPIView):
    serializer_class = UserBehaviorSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self, queryset=None):
        return self.request.user

@method_decorator(cache_response(timeout=None, start_name='mm_games', for_all=True), name='get')
class ListGamesAPIView(ListAPIView):
    serializer_class = GameSerializer
    permission_classes = (IsAuthenticated, )
    queryset = Game.objects.all()

    def get(self, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)

        return CachedResponse(data=serializer.data)


def testView(request, *args, **kwargs):
    return render(request, template_name='mm_test.html')
