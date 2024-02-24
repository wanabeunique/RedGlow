from django.urls import path
from . import views

urlpatterns = [
    path("users/",views.SignUpView.as_view({"post":"create","put":"update"})),
    path('user/session/',views.SessionView.as_view({"post":"create","put":"update"})),
    path('user/checker/',views.AuthCheckerView.as_view()),
    path("user/password/",views.ChangePasswordAPI.as_view()),
    path("user/help/link/", views.ForgotPasswordAPI.as_view()),
    path("email/<str:email>/code/<str:code>",views.CheckKeyView.as_view()),
    path("user/help/password/", views.ChangeForgotPasswordAPI.as_view())
]