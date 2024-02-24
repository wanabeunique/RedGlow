from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=255,unique=True,error_messages={"unique":"Данное имя пользователя занято"},db_index=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True,error_messages={"unique":"Данный адрес электронной почты уже зарегистрирован"})
    phoneNumber = models.CharField(max_length=25,unique=True,error_messages={"unique":"Данный номер телефона уже используется"},null=True)
    steamId = models.CharField(max_length=255,null=True)
    photo = models.ImageField(upload_to='images/userPhoto/',null=True)
    background = models.ImageField(upload_to='images/userBackground/',null=True)
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

class UserMetaData(models.Model):
    timezone = models.CharField(max_length=100)
    ip_adress = models.CharField(max_length=25)
    country = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE)