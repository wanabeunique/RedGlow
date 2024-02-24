from apps.authentication.models import User
from apps.matchmaking.models import Game, UserElo, UserBehavior
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

@receiver(post_save, sender=User)
def create_related_objects(sender, **kwargs):
    created_flag = kwargs.get('created')
    user_instance: User = kwargs.get('instance')
    steam_flag = bool(user_instance.steamId)
    

    userElo_list = []
    
    if steam_flag:
        content_type = ContentType.objects.get_for_model(User)
        q_for_filter = Q(
            codename='play_mm',
            content_type=content_type
        )
    if created_flag or steam_flag:
        games = Game.objects.all()
        for game in games:
            if created_flag:
                userElo_list.append(
                    UserElo(
                        user=user_instance,
                        game=game
                    )
                )
            if steam_flag:
                q_for_filter |= Q(
                    codename=f'play_mm_{game.name}',
                    content_type=content_type
                )
                
    if created_flag:
        UserElo.objects.bulk_create(userElo_list)
        UserBehavior.objects.create(user=user_instance)
    if steam_flag:
        user_instance.user_permissions.add(*Permission.objects.filter(q_for_filter))