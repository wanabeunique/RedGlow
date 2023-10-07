from django.contrib.auth import login, logout
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSignUpSerializer, UserLogInSerializer, KeySerializer, KeySignUpSerializer
from apps.passwordChange.permissions import NotAuthenticated
from rest_framework import status
from django.http import HttpRequest
from .sending import connectToRedis
import requests

class SignUpView(ViewSet):
    permission_classes = (NotAuthenticated,)
    serializer_class = UserSignUpSerializer
    def create(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail":"Ссылка для подтверждения регистрации отправлена вам на почту"},status=status.HTTP_202_ACCEPTED)
    def update(self, request):
        serializer = KeySignUpSerializer(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request,user)
        return Response(serializer.data,status=status.HTTP_200_OK)

class CheckKeyView(APIView):
    permission_classes = (NotAuthenticated, )
    serializer_class = KeySerializer
    def get(self, request,key=None, code=None):
        r = connectToRedis()
        a = r.get(code).decode()
        serializer = self.serializer_class(data={"key":key,"code":code})
        if serializer.is_valid():
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response({"a":a},status=status.HTTP_404_NOT_FOUND)

class SessionView(ViewSet):
    permission_classes = (AllowAny,)
    serializer_class = UserLogInSerializer
    def create(self,request):
        if not bool(request.user.is_authenticated):
            user = request.data
            serializer = self.serializer_class(data=user,context={"request":request})
            serializer.is_valid(raise_exception=True)
            login(request,serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)
    def update(self, request):
        if bool(request.user and request.user.is_authenticated):
            logout(request)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)
    
class AuthCheckerView(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self,request:HttpRequest):
        return Response({'username': request.user.username},status=status.HTTP_202_ACCEPTED)
