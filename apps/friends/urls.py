from django.urls import path
from .views import InviteFriendView, GetFriendshipStatusView, FriendListView, FindUserView

urlpatterns = [
    path('user/friend/',InviteFriendView.as_view({"post":"create","put":"update"})),
    path('user/friendship/<str:username>/',GetFriendshipStatusView.as_view()),
    path('user/<str:username>/friend',FriendListView.as_view()),
    path('user/prefix/<str:value>/',FindUserView.as_view())
]