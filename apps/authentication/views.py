from django.contrib.auth import login, logout, authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from .serializers import UserSignUpSerializer, UserLogInSerializer, CodeSerializer
from rest_framework import status
from apps.passwordChange.permissions import NotAuthenticated
from .code import sendEmailCode

userForSignUp : UserSignUpSerializer = None

class SignUpAPI(APIView):
    permission_classes = (NotAuthenticated,)
    serializer_class = UserSignUpSerializer
    def post(self,request):
        user = request.data
        serializer = self.serializer_class(data=user,context={'request':request})
        serializer.is_valid(raise_exception=True)
        sendEmailCode(user['email'],user['username'],"Код для прохождения регистрации на нашей платформе")
        return Response({"detail":"Код был выслан на почту"},status=status.HTTP_202_ACCEPTED)

class CheckCodeEmailAPI(APIView):
    permission_classes = (NotAuthenticated,)
    serializer_class = CodeSerializer
    def post(self, request):
        code = request.data.get('code')
        user = request.data.get('user')
        serializer = CodeSerializer(data={"code":code,**user},context={'request':request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request,user)
        return Response(serializer.data,status=status.HTTP_200_OK)

class LogInAPI(APIView):
    permission_classes = (NotAuthenticated,)
    authentication_classes = (SessionAuthentication,)
    serializer_class = UserLogInSerializer
    def post(self,request):
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        login(request,serializer.validated_data)
        dataToResponse = serializer.data
        del dataToResponse['password']
        return Response(dataToResponse, status=status.HTTP_200_OK)
    
class LogOutAPI(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        logout(request)
        return Response(status=status.HTTP_200_OK)