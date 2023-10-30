from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser


class User(AbstractUser):
    username = models.CharField(max_length=255,unique=True,error_messages={"unique":"Данное имя пользователя занято"})
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True,error_messages={"unique":"Данный адрес электронной почты уже зарегистрирован"})
    phoneNumber = models.CharField(max_length=25,unique=True,error_messages={"unique":"Данный номер телефона уже используется"},null=True)
    steamId = models.CharField(max_length=255,null=True)
    photo = models.ImageField(upload_to='images/userPhoto/',null=True)
    background = models.ImageField(upload_to='images/userBackground/',null=True)
    decency = models.IntegerField(default=10000)
    reportsOwned = models.IntegerField(default=8)
    reportsGot = models.IntegerField(default=0)
    isAdmin = models.BooleanField(default=False)
    subExpiresIn = models.TimeField(default='00:00:00')
    inGame = models.BooleanField(default=False)
    country = models.CharField(null=True)
    banExpiresIn = models.TimeField(default='00:00:00')
    muteExpiresIn = models.TimeField(default='00:00:00')
    voteExpiresIn = models.TimeField(default='00:00:00')
    first_name = None
    last_name = None

    def __str__(self):
        return self.username
    @property
    def photo_url(self):
        if self.photo: 
            return self.photo.storage.url(self.photo.name)
        return None
    @property
    def background_url(self):
        if self.background: 
            return self.background.storage.url(self.background.name)
        return None