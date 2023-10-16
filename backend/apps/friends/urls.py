from django.urls import path
from .views import InviteFriendView, GetFriendshipStatusView, FriendListView, FindUserView, test, InvitesListView

urlpatterns = [
    path('user/friend/',InviteFriendView.as_view({"post":"create","put":"update",'get':'retrieve'})),
    path('user/friendship/<str:username>/',GetFriendshipStatusView.as_view()),
    path('user/<str:username>/friend',FriendListView.as_view()),
    path('user/invite/<str:typeFlag>',InvitesListView.as_view()),
    path('user/prefix/<str:value>/page/<int:page>',FindUserView.as_view()),
    path('test',test)
]