from django.contrib.auth import login, logout
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from .serializers import UserSignUpSerializer, UserLogInSerializer, KeySignUpSerializer, UserCheckerSerializer
from rest_framework import status
from django.http import HttpRequest

class SignUpView(ViewSet):
    permission_classes = (AllowAny,)
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
        login(request, user)
        return Response({'username':user.username,'photo':user.photo_url},status=status.HTTP_200_OK)

class SessionView(ViewSet):
    permission_classes = (AllowAny,)
    serializer_class = UserLogInSerializer
    def create(self,request):
        if not bool(request.user.is_authenticated):
            data = request.data
            serializer = self.serializer_class(data=data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data
            login(request,user)
            return Response({'username':user.username,'photo':user.photo_url}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)
    def update(self, request):
        if bool(request.user and request.user.is_authenticated):
            logout(request)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)
    
class AuthCheckerView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = UserCheckerSerializer
    def get_object(self, queryset=None):  
        return self.request.user
