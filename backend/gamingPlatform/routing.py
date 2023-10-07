from django.urls import path,include
from apps.friends.consumers import FriendConsumer

websocker_urlpatterns = [
    path('ws/friend',FriendConsumer.as_asgi())
]