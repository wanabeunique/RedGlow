from django.contrib.auth import login, logout
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from .serializers import *
from rest_framework import status
from rest_framework import generics
from apps.authentication.models import User
from django.contrib.auth import authenticate, login
from apps.tools.tasks import sendInfo

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

class ChangePasswordAPI(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)
    
    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        if not self.object.check_password(serializer.data.get("currentPassword")):
            return Response(
                {"currentPassword": "Неправильный текущий пароль"}, status=status.HTTP_400_BAD_REQUEST
            )
        newPassword = serializer.data.get("newPassword")
        self.object.set_password(newPassword)
        self.object.save()
        sendInfo.delay(request.user.email,request.user.username,
                info="Пароль от вашего аккаунта был изменён",
                subject='Смена пароля'
        )
        userAuth = authenticate(username=self.object.username,password=newPassword)
        login(request,userAuth)

        return Response(
            {"detail":"Пароль был успешно изменён"},status=status.HTTP_200_OK
        )

class ForgotPasswordAPI(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ForgotPasswordEmailSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail":"Ссылка для восстановления пароля была выслана на почту"},status=status.HTTP_202_ACCEPTED
        )

class CheckKeyView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = EmailCodeSerializer
    def get(self, request,email=None, code=None):
        serializer = self.serializer_class(data={"email":email,"code":code})
        if serializer.is_valid():
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response({"detail":'Not found'},status=status.HTTP_404_NOT_FOUND)

class ChangeForgotPasswordAPI(APIView):
    serializer_class = ForgotPasswordChangeSerializer
    permission_classes = (AllowAny,)
    
    def put(self, request):
       
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail":"Пароль был успешно изменён. Войдите в аккаунт с новыми данными"},status=status.HTTP_200_OK
        )