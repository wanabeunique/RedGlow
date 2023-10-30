import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gamingPlatform.settings')
django.setup()

from apps.friends.models import Friendship
from apps.authentication.models import User
import json

a = User.objects.get(username='kirin3243')

photo = a.photo

if not photo:
    photo = None

print(json.dumps({'a':photo}))