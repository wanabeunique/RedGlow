import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gamingPlatform.settings')
django.setup()
from apps.authentication.models import User  # noqa
from apps.friends.models import Friendship  # noqa
# 3-252, 250 всего
i = 3
j = i+99
me = [53, 54]

while i < j:
    try:
        Friendship.objects.create(status=Friendship.Status.FRIENDS, inviter=User.objects.get(
            id=i), accepter=User.objects.get(id=me[i % 2]))
        if i % 2:
            Friendship.objects.create(status=Friendship.Status.FRIENDS, inviter=User.objects.get(
                id=me[(i + 1) % 2]), accepter=User.objects.get(id=i))
    except:
        pass
    try:
        Friendship.objects.create(status=Friendship.Status.INVITED, inviter=User.objects.get(
            id=me[(i + 1) % 2]), accepter=User.objects.get(id=i))
    except:
        pass
    i += 1

i = i + 100
j = i + 199

while i < j:
    try:
        Friendship.objects.create(status=Friendship.Status.INVITED, inviter=User.objects.get(
            id=i), accepter=User.objects.get(me[i % 2]))
    except:
        pass
    i += 1

print('rdy')
