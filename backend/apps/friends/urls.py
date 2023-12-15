from django.urls import path
from .views import *

urlpatterns = [
    path('user/friendship/<str:username>/',GetFriendshipStatusView.as_view()),
    path('user/<str:username>/friend/page/<int:page>',FriendListView.as_view()),
    path('user/invite/in/page/<int:page>',InviteInListView.as_view()),
    path('user/invite/out/page/<int:page>',InviteOutListView.as_view()),
    path('user/prefix/<str:value>/page/<int:page>',SearchUserView.as_view()),
    path('user/<str:username>/friend/prefix/<str:value>/page/<int:page>', SearchFriendView.as_view()),
    path('user/invite/in/prefix/<str:value>/page/<int:page>', SearchInviteInView.as_view()),
    path('user/invite/out/prefix/<str:value>/page/<int:page>', SearchInviteOutView.as_view()),
    path('user/<str:username>/friend/common', RetrieveCommonFriendsView.as_view()),
    path('user/<str:username>/friend/common/prefix/<str:value>', SearchCommonFriendsView.as_view()),
    path('test',test)
]