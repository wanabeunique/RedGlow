from django.contrib.auth import login, logout
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from .serializers import UserSignUpSerializer, UserLogInSerializer, KeySerializer, KeySignUpSerializer
from apps.passwordChange.permissions import NotAuthenticated
from rest_framework import status
from apps.passwordChange.permissions import NotAuthenticated

class SignUpView(APIView):
    permission_classes = (NotAuthenticated,)
    serializer_class = UserSignUpSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail":"Ссылка для подтверждения регистрации отправлена вам на почту"},status=status.HTTP_202_ACCEPTED)

class CheckKeyView(APIView):
    permission_classes = (NotAuthenticated, )
    serializer_class = KeySerializer
    def get(self, request,key=None):
        serializer = self.serializer_class(data={"key":key})
        if serializer.is_valid():
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)

class ConfirmSignUpView(APIView):
    permission_classes = (NotAuthenticated,)
    serializer_class = KeySignUpSerializer
    def put(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request,user)
        return Response(serializer.data,status=status.HTTP_200_OK)

class SessionView(ViewSet):
    authentication_classes = (NotAuthenticated,)
    serializer_class = UserLogInSerializer
    def create(self,request):
        if bool(not request.user.is_authenticated):
            user = request.data
            serializer = self.serializer_class(data=user)
            serializer.is_valid(raise_exception=True)
            login(request,serializer.validated_data)
            dataToResponse = serializer.data
            return Response(dataToResponse, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)
    def update(self, request):
        if bool(request.user and request.user.is_authenticated):
            logout(request)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)
        