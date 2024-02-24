from django.db import models
from apps.authentication.models import User
import hashlib
from django.core.exceptions import ValidationError
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from celery.result import AsyncResult
from gamingPlatform.celery import app as celery_app
from django.conf import settings
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

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
    date_to_confirm = models.DateTimeField(null=True)
    date_started = models.DateTimeField(null=True)
    date_ended = models.TimeField(null=True)
    hash = models.CharField(db_index=True, unique=True, null=True)
    celery_task_id = models.CharField(max_length=255, null=True)

    def make_hash(self):
        self.hash = hashlib.sha256(f"{self.status}-{self.pk}-{self.date_created}-MATCH".encode()).hexdigest()

    def revoke_task(self):
        task = AsyncResult(self.celery_task_id)
        if task is not None:
            task.revoke()

    def cancel_match(self, cancel_type: str):
        if self.status == Match.Status.CANCELED:
            return

        UserQueue.objects.filter(user__in=UserMatch.objects.filter(match=self).select_related('user').values('user')).update(match_found=False, is_active=False)
        players = UserMatch.objects.filter(match=self).select_related('user')
        self.status = self.Status.CANCELED
        self.save()

        channel_layer = get_channel_layer()
        players_to_ban = list()
        for player in players:
            if not player.is_accepted:
                players_to_ban.append(player.user)

            async_to_sync(channel_layer.group_send)(
                f'matchQueue_{player.user.username}',
                {
                    'type': cancel_type,
                    'hash': self.hash
                }
            )

        ban_players(players_to_ban, channel_layer, self.game, UserBan.BanType.SABOTAGING)
        


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
    

class UserBan(models.Model):
    class BanType(models.IntegerChoices):
        ADVANTAGE = 0, "Получение преимущества незаконным путём"
        SABOTAGING = 1, "Саботирование(Непринятие игры, выход из неё до конца)" 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)
    ban_type = models.PositiveSmallIntegerField(choices=BanType.choices)
    ban_started_since = models.DateTimeField()
    ban_ends_at = models.DateTimeField(null=True)
    streak_ends_at = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)
    end_streak_task_id = models.CharField(max_length=255, null=True)
    unban_player_task_id = models.CharField(max_length=255, null=True)

    def revoke_end_streak_task(self):
        task = AsyncResult(self.end_streak_task_id)
        if task is not None:
            task.revoke()

    def revoke_unban_player_task(self):
        task = AsyncResult(self.unban_player_task_id)
        if task is not None:
            task.revoke()

    def unban_player(self):
        content_type = ContentType.objects.get_for_model(User)
        if self.ban_type == self.BanType.ADVANTAGE:
            can_play_permission = Permission.objects.get(
                codename='play_mm',
                content_type=content_type
            )
        else:
            can_play_permission = Permission.objects.get(
                codename=f'play_mm_{self.game.name}',
                content_type=content_type
            )
        self.user.user_permissions.add(can_play_permission)


class UserBehavior(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    decency = models.IntegerField(default=10000)
    reportsOwned = models.IntegerField(default=8)
    reportsGot = models.IntegerField(default=0)


@shared_task
def cancel_match_by_time(match_instance_pk: int):
    match_instance = Match.objects.filter(pk=match_instance_pk).first()
    
    if match_instance is None:
        return
    
    match_instance.cancel_match('match_canceled_by_time')

@shared_task
def unban_player(user_ban_pk: int):
    user_ban_instance = UserBan.objects.filter(pk=user_ban_pk).select_related('user').first()
    if user_ban_instance is None:
        return
    
    user_ban_instance.unban_player()

@shared_task
def end_streak(user_pk: int, ban_type: int, game: Game):
    UserBan.objects.filter(user=user_pk, ban_type=ban_type, game=game).update(is_active=False)

def ban_players(players_to_ban: list[User], channel_layer, game: Game, ban_type: int):
    for player in players_to_ban:
        user_ban_instance = UserBan(
            user=player,
            game=game,
            ban_type=ban_type
        )
        user_ban_instance.save()

        async_to_sync(channel_layer.group_send)(
            f'matchQueue_{player.username}',
            {
                'type': 'player_got_banned',
                'ban_ends_at': user_ban_instance.ban_ends_at.strftime('%Y-%m-%d %H:%M:%S') if user_ban_instance.ban_ends_at else None
            }
        )
