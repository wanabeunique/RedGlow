from django.urls import path
from .views import *

urlpatterns = [
    path('test/mm', testView),
    path('user/behavior', RetrieveUserBehaviorView.as_view()),
    path('mm/games', ListGamesAPIView.as_view())
]
