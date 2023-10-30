from django.urls import path
from . import views

urlpatterns = [
    path("user/password/",views.ChangePasswordAPI.as_view()),
    path("user/help/link/", views.ForgotPasswordAPI.as_view()),
    path("email/<str:email>/code/<str:code>",views.CheckKeyView.as_view()),
    path("user/help/password/", views.ChangeForgotPasswordAPI.as_view())
]