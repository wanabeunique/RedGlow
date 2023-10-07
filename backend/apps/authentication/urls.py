from django.urls import path
from . import views

urlpatterns = [
    path("users/",views.SignUpView.as_view({"post":"create","put":"update"})),
    path("key/<str:key>/code/<str:code>",views.CheckKeyView.as_view()),
    path('user/session/',views.SessionView.as_view({"post":"create","put":"update"})),
    path('user/checker/',views.AuthCheckerView.as_view()),
]