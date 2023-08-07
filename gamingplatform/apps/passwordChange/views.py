from rest_framework import generics
from .serializers import ChangePasswordSerializer, ForgotPasswordCodeSerializer, ForgotPasswordChangeSerializer
from apps.authentication.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import NotAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from apps.authentication.code import sendEmailCode
from apps.authentication.serializers import CodeSerializer
from rest_framework.viewsets import ViewSet
from django.contrib.auth import authenticate, login
import redis

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

        serializer.is_valid()
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

class ForgotPasswordAPI(ViewSet):
    permission_classes = (AllowAny,)
    serializer_class = ForgotPasswordCodeSerializer

    def create(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        sendEmailCode(email,User.objects.get(email=email).username,"Код для смены пароля на нашей платформе")
        return Response(
            {"detail":"Код был выслан на почту"},status=status.HTTP_202_ACCEPTED
        )

        
    def update(self, request):
        request.data.update({"doDelete":False})

        data = request.data

        serializer = CodeSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        return Response(
            {"detail":"Код принят"}, status=status.HTTP_202_ACCEPTED
        )

    
class ChangeForgotPasswordAPI(APIView):
    serializer_class = ForgotPasswordChangeSerializer
    permission_classes = (AllowAny,)
    
    def put(self, request, *args, **kwargs):
       
        data = request.data
        serializer = self.serializer_class(data=request.data)
        email = data.get('email')
        r = redis.StrictRedis(host='localhost', port=6379, db=0, password='SeMeN4565', socket_timeout=None, connection_pool=None, charset='utf-8', errors='strict', unix_socket_path=None)
        if r.exists(email):
            r.delete(email)
        else:
            return Response(
                {"detail":"Время выделенное на смену пароля истекло"},status=status.HTTP_403_FORBIDDEN
            )
        r.close()
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=data['email'])
        user.set_password(serializer.data.get("password"))
        user.save()

        return Response(
            {"detail":"Пароль был успешно изменён"},status=status.HTTP_200_OK
        )
