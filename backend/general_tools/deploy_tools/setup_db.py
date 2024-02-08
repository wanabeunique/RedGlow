import django
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.gamingPlatform.settings')
django.setup()

from apps.matchmaking.models import Game, UserQueue
from django.db import IntegrityError
import logging

civ_5_game = Game(
    name="Sid Meier's Civilization V",
    strict_num_of_players=False,
    min_players=4,
    max_players=12
)

logger = logging.getLogger(__name__)

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


UserQueue.objects.all().update(is_active=False)