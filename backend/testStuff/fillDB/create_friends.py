import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gamingPlatform.settings')
django.setup()

#156-405, 250 всего
#53,54,55
from apps.friends.models import Friendship
from apps.authentication.models import User

i = 156
j = 156+99
me = [53,54]

while i < j:
    try:
        Friendship.objects.create(status=Friendship.Status.FRIENDS,inviter=User.objects.get(id=i),accepter=User.objects.get(id=me[i % 2]))
        if i % 2:
            Friendship.objects.create(status=Friendship.Status.FRIENDS,inviter=User.objects.get(id=me[(i + 1) % 2]),accepter=User.objects.get(id=i))
    except:
        pass
    try:
        Friendship.objects.create(status=Friendship.Status.INVITED,inviter=User.objects.get(id=me[(i + 1) % 2]),accepter=User.objects.get(id=i))
    except:
        pass
    i += 1

i = 156 + 100
j = 156 + 199

while i < j:
    try:
        Friendship.objects.create(status=Friendship.Status.INVITED,inviter=User.objects.get(id=i),accepter=User.objects.get(me[i % 2]))
    except:
        pass
    i += 1

print('rdy')