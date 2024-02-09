from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from apps.authentication.models import User
from .models import UserElo, Game, Match, cancel_match_by_time
from django.utils import timezone
from datetime import timedelta
from django.conf import settings


@receiver(post_save, sender=Game)
def create_related_objects(sender, **kwargs):
    if not kwargs.get('created', None):
        return
    users = User.objects.all()
    user_elo_list = []
    for user in users:
        user_elo_list.append(
            UserElo(user=user,game=kwargs.get('instance'))
        )
    UserElo.objects.bulk_create(user_elo_list)

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