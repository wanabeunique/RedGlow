from apps.authentication.models import User
from apps.matchmaking.models import Game, UserElo
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_related_objects(sender, **kwargs):
    if not kwargs.get('created'):
        return
    games = Game.objects.all()
    userElo_list = []

    for game in games:
        userElo_list.append(
            UserElo(
                user=kwargs.get('instance'),
                game=game
            )
        )

    UserElo.objects.bulk_create(userElo_list)