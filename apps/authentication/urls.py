from django.urls import path
from . import views

urlpatterns = [
    path("users/",views.SignUpView.as_view()),
    path("key/<str:key>/",views.CheckKeyView.as_view()),
    path("users/confirm/",views.ConfirmSignUpView.as_view()),
    path('user/session/',views.SessionView.as_view({"post":"create","put":"update"})),
]