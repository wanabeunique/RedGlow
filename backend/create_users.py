import django
import os
import random
import string

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gamingPlatform.settings')
django.setup()

from apps.authentication.models import User

username = 'kirin'
password = '1234'
email = 'randomemail'
emailDomen = '@mail.ru'
characters = string.ascii_letters

for i in range(250):
    i = str(i)
    a = User.objects.create(username=random.choice(characters) + username+  i,password=password,email=email + i + emailDomen)
    a.set_password(password)
    a.save()

print('rdy')