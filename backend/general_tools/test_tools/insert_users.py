import django
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.gamingPlatform.settings')
django.setup()

from apps.authentication.models import User
import random
from string import ascii_letters
import os


def create_users(count_of_each_users_part):
    username_to_use = 'test_username'
    email_to_use = 'tmp@gmail.com'
    password_to_use = os.environ.get('PASSWORD_FOR_TEST_USERS','admin1234')

    users_1 = []
    for i in range(count_of_each_users_part):
        user = User(
            username=username_to_use + (ascii_letters[random.randint(0, len(ascii_letters)-1)] * random.randint(1,5)) + str(i),
            email=ascii_letters[random.randint(0, len(ascii_letters)-1)] + str(i) + email_to_use,
        )
        user.set_password(password_to_use)
        user.save()
        users_1.append(user)

    users_2 = []
    username_to_use = 'slave_tester'
    email_to_use = 'slave@gmail.com'
    for i in range(count_of_each_users_part + 1, count_of_each_users_part * 2):
        user = User(
            username=username_to_use + (ascii_letters[random.randint(0, len(ascii_letters)-1)] * random.randint(1,5)) + str(i),
            email=ascii_letters[random.randint(0, len(ascii_letters)-1)] + str(i) + email_to_use,
        )
        user.set_password(password_to_use)
        user.save()
        users_2.append(user)

    users_1.extend(users_2)
    return users_1, users_2