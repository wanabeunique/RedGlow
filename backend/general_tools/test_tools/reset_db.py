import django
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.gamingPlatform.settings')
django.setup()

from apps.authentication.models import User
from apps.friends.models import Friendship
import logging

User.objects.all().exclude(username='admin').delete()
Friendship.objects.all().delete()
logger = logging.getLogger(__name__)
logger.info("DB has been cleaned")