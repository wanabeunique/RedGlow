import django
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.gamingPlatform.settings')
django.setup()

from apps.authentication.models import User
from apps.friends.models import Friendship
from insert_users import create_users
from insert_friends import create_friends
import logging

count_of_each_users_part = 1000

logger = logging.getLogger(__name__)

if User.objects.all().count() <= 1:
    users = create_users(count_of_each_users_part)
    logger.info('users have been inserted')
else:
    logger.info("There's already users in db. Run reset_db.py first")


if Friendship.objects.all().count() == 0:
    friends = create_friends()
    logger.info('friendships have been inserted')
else:
    logger.info("There's already friendships in db. Run reset_db.py first")