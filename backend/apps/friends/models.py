from django.db import models
from apps.authentication.models import User

class Friendship(models.Model):
    class Status(models.IntegerChoices):
        INVITED = 0, "Заявка отправлена"
        FRIENDS = 1, "Друзья"
    inviter = models.ForeignKey(User,on_delete=models.CASCADE,related_name='inviter',null=True)
    accepter = models.ForeignKey(User,on_delete=models.CASCADE,related_name='accepter',null=True)
    status = models.PositiveSmallIntegerField(choices=Status.choices)
    created_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.inviter.username} - {self.accepter.username}"
    class Meta:
        unique_together = ('inviter', 'accepter')


# class Friendship(models.Model):
#     user_1 = models.ForeignKey(User, related_name='friend_1', on_delete=models.CASCADE)
#     user_2 = models.ForeignKey(User, related_name='friend_2', on_delete=models.CASCADE)
#     created_at = models.DateField(auto_now_add=True)

#     class Meta:
#         unique_together = ['user_a', 'user_b']

#     def __str__(self):
#         return f'{self.user_a.username} - {self.user_b.username}'


# class FriendRequest(models.Model):
#     sent_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='sent_by')
#     received_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='received_by')
#     is_accepted = models.BooleanField(default=False)
#     created_at = models.DateField(auto_now_add=True)

#     class Meta:
#         unique_together = ['from_user','to_user']

#     def __str__(self):
#         return f'{self.from_user.username} to {self.to_user.username}'