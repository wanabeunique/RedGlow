import django
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.gamingPlatform.settings')
django.setup()

from apps.matchmaking.models import Game, UserQueue, UserBehavior
from apps.authentication.models import User
from django.db import IntegrityError
import logging
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

logger = logging.getLogger(__name__)

def insert_games():
    civ_5_game = Game(
        name="Sid Meier's Civilization V",
        strict_num_of_players=False,
        min_players=4,
        max_players=12
    )

    try:
        civ_5_game.save()
        logger.info("Civilization V game has been inserted in the db")
    except IntegrityError:
        logger.info("Can't insert Cviilization V in the db. It's already there")

    civ_6_game = Game(
        name="Sid Meier's Civilization VI",
        strict_num_of_players=False,
        min_players=4,
        max_players=12
    )

    try:
        civ_6_game.save()
        logger.info("Civilization VI game has been inserted in the db")
    except IntegrityError:
        logger.info("Can't insert Cviilization VI in the db. It's already there")


def update_queues():
    UserQueue.objects.all().update(is_active=False, match_found=False)

def create_permissions():
    content_type = ContentType.objects.get_for_model(User)
    try:
        Permission.objects.create(
            codename='play_mm',
            name='Can play at matchmaking',
            content_type=content_type
        )
    except IntegrityError:
        pass
    for game in Game.objects.all():
        try:
            Permission.objects.create(
                codename=f'play_mm_{game.name}',
                name=f'Can play at matchmaking. Game {game.name}',
                content_type=content_type
            )
        except IntegrityError:
            pass
    logger.info('All custom permissions have been created')

def create_user_behaviors():
    
    instances = []
    for user in User.objects.filter(userbehavior__isnull=True):
        try:
            instances.append(
                UserBehavior(
                    user=user
                )
            )
        except IntegrityError:
            pass
    UserBehavior.objects.bulk_create(instances,ignore_conflicts=True)
    logger.info('All necessary userBehabiors have been created')


insert_games()
update_queues()
create_permissions()
create_user_behaviors()