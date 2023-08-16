from django.urls import path
from . import views

urlpatterns = [
    path("user/password/",views.ChangePasswordAPI.as_view()),
    path("user/forgot/link/", views.ForgotPasswordAPI.as_view()),
    path('user/forgot/key/<str:key>/', views.CheckHashAPI.as_view()),
    path("user/forgot/password/", views.ChangeForgotPasswordAPI.as_view())
]