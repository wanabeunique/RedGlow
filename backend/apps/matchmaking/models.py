from django.db import models, IntegrityError
from apps.authentication.models import User
import hashlib
import string
import random


class Game(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    strictNumOfPlayers = models.BooleanField(default=True)
    maxPlayers = models.IntegerField()

    def __str__(self):
        return self.name


class HeroToPlay(models.Model):
    name = models.CharField(max_length=255)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)


class UserMatchQueue(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    eloFilter = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    queuedFrom = models.DateTimeField(auto_now_add=True)
    targetPlayers = models.SmallIntegerField(null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.game}. {self.user}. {self.active}"


class Match(models.Model):
    class Status(models.IntegerChoices):
        CREATED = 0, "Создана"
        PREPARING = 1, "Подготовка"
        PICKING = 2, "Пики, баны"
        PLAYING = 3, "В процессе"
        ENDED = 4, "Игра окончена"
        CANCELED = -1, "Отменена"

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    status = models.SmallIntegerField(choices=Status.choices, default=0)
    date = models.DateTimeField(auto_now=True)
    duration = models.TimeField(null=True)
    hash = models.CharField(db_index=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.hash:
            self.hash = makeHash(23)
        try:
            super(Match, self).save(*args, **kwargs)
        except IntegrityError:
            self.save(*args, **kwargs)


def makeHash(lenOfTheHash):
    return ''.join(random.sample(string.ascii_letters + string.digits, lenOfTheHash))


class UserMatch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    eloChange = models.SmallIntegerField(null=True)
    place = models.SmallIntegerField(null=True)
    heroToPlay = models.ForeignKey(
        HeroToPlay, on_delete=models.CASCADE, null=True)
    accepted = models.BooleanField(default=False)


class UserElo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    elo = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user}. {self.game}; {self.elo}"
