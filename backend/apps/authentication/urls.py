from django.urls import path
from . import views

urlpatterns = [
    path("users/",views.SignUpView.as_view({"post":"create","put":"update"})),
    path('user/session/',views.SessionView.as_view({"post":"create","put":"update"})),
    path('user/checker/',views.AuthCheckerView.as_view()),
]