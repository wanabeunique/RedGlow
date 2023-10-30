from django.urls import path
from .views import *

urlpatterns = [
    path('user/info', RetrieveUserProfileView.as_view()),
    path('user/<str:username>/info',RetirieveForeignUserProfileView.as_view()),
    path('user/photo/', UpdateUserPhotoView.as_view()),
    path('user/<str:username>/photo', RetrieveUserPhotoView.as_view()),
    path('user/background/', UpdateUserBackgroundView.as_view()),
    path('user/<str:username>/background', RetrieveUserBackgroundView.as_view()),
    path('user/steamId/', UpdateSteamIdView.as_view()),
    path('user/<str:username>/steamName',RetrieveUserSteamNameView.as_view()),
    path('user/behavior', RetrieveUserBehaviorView.as_view())
]