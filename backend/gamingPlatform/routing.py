from django.urls import path, include
from apps.friends.consumers import FriendConsumer
from apps.matchmaking.consumers import MatchQueueConsumer

websocker_urlpatterns = [
    path('ws/friend', FriendConsumer.as_asgi()),
    path('ws/match_queue', MatchQueueConsumer.as_asgi()),
]
