from django.urls import path
from . import views

urlpatterns = [
    path("user/password",views.ChangePasswordAPI.as_view()),
    path("user/forgot/code/", views.ForgotPasswordAPI.as_view({"post":"create","put":"update"})),
    path("user/forgot/password/", views.ChangeForgotPasswordAPI.as_view())
]