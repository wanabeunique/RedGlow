from django.urls import path
from .views import *

urlpatterns = [
    path('user/friend/',InviteFriendView.as_view({"post":"create","put":"update"})),
    path('user/friend/<str:targetName>/',GetRelationStatusView.as_view())
]