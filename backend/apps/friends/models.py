from django.db import models
from apps.authentication.models import User

class Friendship(models.Model):
    class Status(models.IntegerChoices):
        INVITED = 0, "Заявка отправлена"
        FRIENDS = 1, "Друзья"
    inviter = models.ForeignKey(User,on_delete=models.CASCADE,related_name='inviter',null=True)
    accepter = models.ForeignKey(User,on_delete=models.CASCADE,related_name='accepter',null=True)
    status = models.PositiveSmallIntegerField(choices=Status.choices)