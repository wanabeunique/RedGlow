from django.urls import path, re_path
from apps.friends.consumers import FriendConsumer
from apps.matchmaking.consumers import MatchQueueConsumer

websocker_urlpatterns = [
    path('ws/friend', FriendConsumer.as_asgi()),
    re_path(r'ws/match_queue/(?P<game_id>\w+)/$', MatchQueueConsumer.as_asgi()),
]
