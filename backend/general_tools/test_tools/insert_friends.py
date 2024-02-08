import django
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.gamingPlatform.settings')
django.setup()

from apps.authentication.models import User
from apps.friends.models import Friendship
import random
import os

def create_friends():
    users = User.objects.all().order_by('id')
    main_users = users[:len(users) // 2]
    help_users = users[len(users) // 2:]

    friendship_list = []
    friendships = {
        'friends': [[] for _ in range(len(main_users))],
        'invites_out': [[] for _ in range(len(main_users))],
        'invites_in': [[] for _ in range(len(main_users))]
    }
    for item in range(len(main_users)):
        user = main_users[item]
        for key in friendships.keys():
            while len(friendships[key][item]) < 150:
                random_user = help_users[random.randint(0,len(help_users)-1)]
                if random_user in friendships['friends'][item] or random_user in friendships['invites_out'][item] or random_user in friendships['invites_in'][item]:
                    continue
                friendships[key][item].append(random_user)

            friendships_tmp = friendships[key][item]

            if key == 'friends':
                for user_friendship in friendships_tmp:
                    friendship_list.append(
                        Friendship(
                            inviter=user,
                            accepter=user_friendship,
                            status=Friendship.Status.FRIENDS
                        )
                    )
            elif key == 'invites_out':
                for user_friendship in friendships_tmp:
                    friendship_list.append(
                        Friendship(
                            inviter=user,
                            accepter=user_friendship,
                            status=Friendship.Status.INVITED
                        )
                    )
            else:
                for user_friendship in friendships_tmp:
                    friendship_list.append(
                        Friendship(
                            inviter=user_friendship,
                            accepter=user,
                            status=Friendship.Status.FRIENDS
                        )
                    )
    return Friendship.objects.bulk_create(friendship_list)