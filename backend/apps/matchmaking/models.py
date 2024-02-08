from django.db import models, IntegrityError
from apps.authentication.models import User
import hashlib
from django.core.exceptions import ValidationError
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from celery.result import AsyncResult
from gamingPlatform.celery import app as celery_app

class Game(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    strict_num_of_players = models.BooleanField(default=True)
    max_players = models.IntegerField()
    min_players = models.IntegerField()

    def __str__(self):
        return self.name
    
    def clean(self) -> None:
        if self.strict_num_of_players and self.max_players != self.min_players:
            raise ValidationError(
                "If strictNumOfPlayers is True, minPlayers and maxPlayers must be equal"
            )
        
        if self.max_players < self.min_players:
            raise ValidationError(
                "maxPlayers must be bigger than minPlayers"
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)



class HeroToPlay(models.Model):
    name = models.CharField(max_length=255)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)


class UserQueue(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    elo_filter = models.BooleanField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    queued_from = models.DateTimeField(auto_now=True)
    target_players = models.SmallIntegerField(null=True)
    is_active = models.BooleanField(default=True)
    match_found = models.BooleanField(default=False)

    def __str__(self):
        return f"Game: {self.game}. User: {self.user}. TP: {self.target_players}"


class Match(models.Model):
    class Status(models.IntegerChoices):
        CREATED = 0, "Создана"
        PREPARING = 1, "Подготовка"
        PICKING = 2, "Пики, баны"
        PLAYING = 3, "В процессе"
        ENDED = 4, "Игра окончена"
        CANCELED = -1, "Отменена"

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    status = models.SmallIntegerField(choices=Status.choices, default=Status.CREATED)
    date_created = models.DateTimeField(auto_now_add=True)
    date_to_confirm = models.DateTimeField()
    date_started = models.DateTimeField(null=True)
    date_ended = models.TimeField(null=True)
    hash = models.CharField(db_index=True, unique=True, null=True)
    celery_task_id = models.CharField(max_length=255)

    def make_hash(self):
        self.hash = hashlib.sha256(f"{self.status}-{self.pk}-{self.date_created}-MATCH".encode()).hexdigest()

    @shared_task
    def cancel_match_by_time(self):
        self.status = self.Status.CANCELED
        players = UserMatch.objects.filter(match=self).select_related('user')
        self.save()
        channel_layer = get_channel_layer()
        for player in players:
            async_to_sync(channel_layer.group_send)(
                f'matchQueue_{player.user.username}',
                {
                    'type': 'match_canceled_by_time',
                    'hash': self.hash
                }
            )

    def revoke_task(self):
        task = AsyncResult(self.celery_task_id)
        if not task.ready():
            celery_app.control.revoke(self.celery_task_id, terminate=True)

    def cancel_match(self):
        UserQueue.objects.filter(user__in=UserMatch.objects.filter(match=self).values('user')).update(game_found=False)
        


class UserMatch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    elo_change = models.SmallIntegerField(null=True)
    place = models.SmallIntegerField(null=True)
    hero_to_play = models.ForeignKey(
        HeroToPlay, on_delete=models.CASCADE, null=True)
    is_accepted = models.BooleanField(null=True)


class UserElo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    elo = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ['user','game']

    def __str__(self):
        return f"{self.user}. {self.game}; {self.elo}"