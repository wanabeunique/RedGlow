from django.db import models
from apps.authentication.models import User

class Relation(models.Model):
    class Status(models.IntegerChoices):
        INVITED = 0, "Invited"
        FRIENDS = 1, "Friends"
    inviter = models.ForeignKey(User,on_delete=models.CASCADE,related_name='inviter',null=True)
    accepter = models.ForeignKey(User,on_delete=models.CASCADE,related_name='accepter',null=True)
    status = models.PositiveSmallIntegerField(choices=Status.choices)

# status = False - заявка от user_1, status = True - друзья