from rest_framework import generics
from .serializers import ChangePasswordSerializer, ForgotPasswordEmailSerializer, ForgotPasswordChangeSerializer
from apps.authentication.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login

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

        serializer.is_valid(raise_exeption=True)
        if not self.object.check_password(serializer.data.get("currentPassword")):
            return Response(
                {"currentPassword": "Неправильный текущий пароль"}, status=status.HTTP_400_BAD_REQUEST
            )
        
        self.object.set_password(serializer.data.get("newPassword"))
        self.object.save()
        userAuth = authenticate(username=self.object.username,password=request.data.get("newPassword"))
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

