from django.urls import path
from .views import *

urlpatterns = [
    path('user/friend/',InviteFriendView.as_view({"post":"create","put":"update","get":"retrieve"}))
]