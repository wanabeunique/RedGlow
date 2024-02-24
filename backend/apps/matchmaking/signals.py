from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from apps.authentication.models import User
from .models import UserElo, Game, Match, cancel_match_by_time, unban_player, UserBan, end_streak
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from apps.tools.caching import delete_cache


@receiver(post_save, sender=Game)
def create_related_objects(sender, **kwargs):
    delete_cache('mm_games','/mm/games',for_all=True)
    if not kwargs.get('created', None):
        return

    game_instance: Game = kwargs.get('instance')
    users = User.objects.all()
    user_elo_list = []
    for user in users:
        user_elo_list.append(
            UserElo(user=user,game=game_instance)
        )
    content_type = ContentType.objects.get_for_model(User)
    UserElo.objects.bulk_create(user_elo_list)
    Permission.objects.create(
        codename=f'play_mm_{game_instance.name}',
        name=f'Can play at matchmaking. Game: {game_instance.name}',
        content_type=content_type
    )

@receiver(pre_save, sender=Match)
def setup_dates(sender, **kwargs):
    match_instance: Match = kwargs.get('instance')
    if match_instance.status == match_instance.Status.PLAYING:
        match_instance.date_started = timezone.now()

    if match_instance.status == match_instance.Status.ENDED:
        match_instance.date_ended = timezone.now()

    if match_instance.status == match_instance.Status.PREPARING:
        match_instance.revoke_task()

@receiver(post_save, sender=Match)
def make_match_hash(sender, **kwargs):
    if not kwargs.get('created', None):
        return

    match_instance: Match = kwargs.get('instance')
    
    if match_instance.status == match_instance.Status.CREATED:
        if not match_instance.celery_task_id:
            match_instance.date_to_confirm = match_instance.date_created + timedelta(seconds=settings.TIME_TO_ACCEPT_A_GAME)
            task = cancel_match_by_time.apply_async(
                args=[match_instance.pk],
                eta=match_instance.date_to_confirm
            )
            match_instance.celery_task_id = task.task_id

    match_instance.make_hash()
    match_instance.save()

@receiver(pre_save, sender=UserBan)
def update_ban_dates(sender, **kwargs):
    user_ban_instance: UserBan = kwargs.get('instance', None)

    if user_ban_instance is None:
        return
    
    if user_ban_instance.ban_type == UserBan.BanType.ADVANTAGE:
        user_ban_instance.game = None
    
    if not user_ban_instance.pk:
        user_ban_instance.ban_started_since = timezone.now()
    
    if user_ban_instance.ban_ends_at is None and user_ban_instance.streak_ends_at is None:
        num_of_ban = UserBan.objects.filter(
            is_active=True,
            user=user_ban_instance.user,
            game=user_ban_instance.game,
            ban_type=user_ban_instance.ban_type
        ).count() + 1

        bans: dict = settings.BAN_TYPE_AND_TIMEOUT.get(UserBan.BanType(user_ban_instance.ban_type).name)

        if num_of_ban in bans.keys():
            ban_time: timedelta = bans.get(num_of_ban)
        else:
            ban_time: timedelta = bans.get(max(bans.keys()))

        if ban_time == 'infinity':
            ban_time = None
            streak_time = None
        else:
            if ban_time <= timedelta(days=1):
                streak_time = timedelta(days=1)
            else:
                streak_time = ban_time

        if ban_time:
            user_ban_instance.ban_ends_at = user_ban_instance.ban_started_since + ban_time
            user_ban_instance.streak_ends_at = user_ban_instance.ban_ends_at + streak_time
        else:
            user_ban_instance.ban_ends_at = None
            user_ban_instance.streak_ends_at = None

@receiver(post_save, sender=UserBan)
def ban_user(sender, **kwargs):
    if not kwargs.get('created', None):
        return
    
    user_ban_instance: UserBan = kwargs.get('instance', None)

    if user_ban_instance is None:
        return
    
    previous_ban = UserBan.objects.filter(user=user_ban_instance.user,game=user_ban_instance.game,ban_type=user_ban_instance.ban_type,is_active=True).last()
    
    if previous_ban is not None:
        previous_ban.revoke_end_streak_task()
        previous_ban.revoke_unban_player_task()

    content_type = ContentType.objects.get_for_model(User)
    if user_ban_instance.ban_type == user_ban_instance.BanType.ADVANTAGE:
        can_play_permission = Permission.objects.get(
            codename='play_mm',
            content_type=content_type
        )
    else:
        can_play_permission = Permission.objects.get(
            codename=f'play_mm_{user_ban_instance.game.name}',
            content_type=content_type
        )

    user_ban_instance.user.user_permissions.remove(can_play_permission)

    if user_ban_instance.ban_ends_at is None:
        return

    unban_task = unban_player.apply_async(
        args=[user_ban_instance.pk],
        eta=user_ban_instance.ban_ends_at
    )
    end_streak_task = end_streak.apply_async(
        args=[user_ban_instance.user.pk, user_ban_instance.ban_type, user_ban_instance.game],
        eta=user_ban_instance.streak_ends_at
    )
    user_ban_instance.unban_player_task_id = unban_task.task_id
    user_ban_instance.end_streak_task_id = end_streak_task.task_id
    user_ban_instance.save()