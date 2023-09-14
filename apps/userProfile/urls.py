from django.urls import path
from .views import UpdateUserPhotoView, RetrieveUserProfileView, RetrieveUserPhotoView

urlpatterns = [
    path('user', RetrieveUserProfileView.as_view()),
    path('user/photo/', UpdateUserPhotoView.as_view()),
    path('user/<str:username>/photo', RetrieveUserPhotoView.as_view())
]