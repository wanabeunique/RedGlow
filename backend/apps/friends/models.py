from django.db import models
from apps.authentication.models import User


class Friendship(models.Model):
    class Status(models.IntegerChoices):
        INVITED = 1, "Заявка отправлена"
        FRIENDS = 2, "Друзья"
    inviter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='inviter')
    accepter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='accepter')
    status = models.PositiveSmallIntegerField(choices=Status.choices)
    created_at = models.DateField(auto_now=True)

    class Meta:
        unique_together = ('inviter', 'accepter')

    def __str__(self):
        return f"{self.inviter.username} - {self.accepter.username}"
