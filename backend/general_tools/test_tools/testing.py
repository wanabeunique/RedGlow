import django
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.gamingPlatform.settings')
django.setup()

from apps.matchmaking.models import UserMatch, Match, UserQueue

match_instance = Match.objects.last()

print(UserMatch.objects.filter(match=match_instance).select_related('user').values('user'))
print(UserQueue.objects.filter(user__in=UserMatch.objects.filter(match=match_instance).select_related('user').values('user')).update(match_found=False, is_active=True))
