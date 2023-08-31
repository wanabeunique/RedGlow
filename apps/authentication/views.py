from django.contrib.auth import login, logout
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import UserSignUpSerializer, UserLogInSerializer, KeySerializer, KeySignUpSerializer
from apps.passwordChange.permissions import NotAuthenticated
from rest_framework import status
from apps.passwordChange.permissions import NotAuthenticated

class SignUpView(ViewSet):
    permission_classes = (NotAuthenticated,)
    serializer_class = UserSignUpSerializer
    def create(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail":"Ссылка для подтверждения регистрации отправлена вам на почту"},status=status.HTTP_202_ACCEPTED)
    def update(self, request):
        serializer = KeySignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request,user)
        return Response(serializer.data,status=status.HTTP_200_OK)

class CheckKeyView(APIView):
    permission_classes = (NotAuthenticated, )
    serializer_class = KeySerializer
    def get(self, request,key=None):
        serializer = self.serializer_class(data={"key":key})
        if serializer.is_valid():
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)

class SessionView(ViewSet):
    permission_classes = (AllowAny,)
    serializer_class = UserLogInSerializer
    def create(self,request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        login(request,serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def update(self, request):
        if bool(request.user and request.user.is_authenticated):
            logout(request)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)
    
class AuthCheckerView(APIView):
    permission_classes = (AllowAny, )
    def get(self,request):
        if bool(request.user and request.user.is_authenticated):
            return Response(None,status=status.HTTP_200_OK)
        return Response(None, status=status.HTTP_403_FORBIDDEN)