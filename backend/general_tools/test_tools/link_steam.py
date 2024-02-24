import sys
import django
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.gamingPlatform.settings')
django.setup()

from apps.authentication.models import User
import logging

args = sys.argv
logger = logging.getLogger(__name__)

for i in args[1:]:
    tmp_lst = i.split(':')

    user = User.objects.get(username=tmp_lst[0])
    user.steamId = tmp_lst[1]
    user.save()


logger.info('Steamids have been updated')