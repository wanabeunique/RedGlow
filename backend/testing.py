import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gamingPlatform.settings')
django.setup()

from django.db.models import F, OuterRef, Subquery, Q
from apps.friends.models import Friendship
from apps.authentication.models import User
from apps.matchmaking.models import *

# user1 = User.objects.get(id=55)
# user2 = User.objects.get(id=53)
# user3 = User.objects.get(id=54)

# game = Game.objects.create(name="Sid Meire's Civilization VI")

# UserElo.objects.create(user=user1,game=game,elo=25)
# MatchQueue.objects.create(user=user1,game=game,eloFilter=True,targetPlayers=4)

# UserElo.objects.create(user=user2,game=game,elo=967)
# MatchQueue.objects.create(user=user2,game=game,eloFilter=True,targetPlayers=6)

# UserElo.objects.create(user=user2,game=game,elo=534)
# MatchQueue.objects.create(user=user2,game=game,eloFilter=True,targetPlayers=5)


elo_subquery = UserElo.objects.filter(user=OuterRef('user')).values('elo')[:1]
elo = 1300
# Затем используйте Subquery для аннотации elo в модели MatchQueue
match_queues = MatchQueue.objects.prefetch_related('user','game').filter(
                    game=1,active=True,eloFilter=True,targetPlayers=4
).annotate(elo=Subquery(elo_subquery)).filter(elo__gt=elo-600, elo__lt=elo+600)

print(
    match_queues
)