from django.urls import path
from . import views

urlpatterns = [
    path("users",views.SignUpAPI.as_view()),
    path("user/code/",views.CheckCodeEmailAPI.as_view()),
    path('user/login/',views.LogInAPI.as_view()),
    path('user/logout/',views.LogOutAPI.as_view())
]