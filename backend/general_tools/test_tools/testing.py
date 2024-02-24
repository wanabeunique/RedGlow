import django
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.gamingPlatform.settings')
django.setup()

from apps.matchmaking.models import UserMatch, Match, UserQueue, UserBan, Game, UserBehavior
from apps.authentication.models import User
from django.conf import settings
from gamingPlatform.celery import app as celery_app
from celery.result import AsyncResult
import logging
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.core.cache import cache

game = Game.objects.get(id=1)
game.min_players = 4
game.save()