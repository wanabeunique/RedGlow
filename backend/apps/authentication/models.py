from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser


class User(AbstractUser):
    username = models.CharField(max_length=255,unique=True,error_messages={"unique":"Данное имя пользователя занято"})
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True,error_messages={"unique":"Данный адрес электронной почты уже зарегистрирован"})
    phoneNumber = models.CharField(max_length=25,unique=True,error_messages={"unique":"Данный номер телефона уже используется"},null=True)
    steamId = models.CharField(max_length=255,null=True)
    photo = models.ImageField(default="", upload_to='images/userPhoto/',null=True)
    decency = models.IntegerField(default=10000)
    reports = models.IntegerField(default=8)
    isAdmin = models.BooleanField(default=False)
    subExpiresIn = models.TimeField(default='00:00:00')
    inGame = models.BooleanField(default=False)
    country = models.CharField(null=True)
    banExpiresIn = models.TimeField(default='00:00:00')
    voteExpiresIn = models.TimeField(default='00:00:00')
    is_staff = None
    first_name = None
    last_name = None

    def __str__(self):
        return self.username