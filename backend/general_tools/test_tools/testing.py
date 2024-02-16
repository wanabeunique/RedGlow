import django
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.gamingPlatform.settings')
django.setup()

from apps.matchmaking.models import UserQueue
from django.db.models.manager import BaseManager

query = UserQueue.objects.filter(is_active=True,match_found=False)

a = list(query)
b = BaseManager()

print(UserQueue.objects.filter(id__in=a))