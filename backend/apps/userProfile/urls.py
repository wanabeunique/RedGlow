from django.urls import path
from .views import *

urlpatterns = [
    path('user', RetrieveUserProfileView.as_view()),
    path('user/<str:username>',RetirieveForeignUserProfileView.as_view()),
    path('user/photo/', UpdateUserPhotoView.as_view()),
    path('user/<str:username>/photo', RetrieveUserPhotoView.as_view()),
    path('user/background/', UpdateUserBackgroundView.as_view()),
    path('user/<str:username>/background', RetrieveUserBackgroundView.as_view()),
    path('user/steamId/', UpdateSteamIdView.as_view()),
    path('user/<str:username>/steamName/',RetrieveUserSteamNameView.as_view()),
    path('user/<str:username>/steamGame/<str:game>', RetrieveUserOwnsGameView.as_view())
]