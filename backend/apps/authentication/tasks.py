from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from cryptography.fernet import Fernet
from django.conf import settings
import json
import redis
from celery import shared_task
import random
import string
from .sending import connectToRedis

domen = 'https://localhost'

@shared_task
def saveSmth(owner, smth):
    r = redis.StrictRedis(host='redis', port=6379, db=1, socket_timeout=None, connection_pool=None, charset='utf-8', errors='strict', unix_socket_path=None)

    r.set(owner, json.dumps(smth))
    r.expire(owner, 900) #900 seconds = 15 min
    r.close()

@shared_task
def generate_code(num) -> str:
    r = connectToRedis()
    code = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(num))
    if r.exists(code):
        generate_code(num)
    return code

@shared_task
def sendLink(username, forWhat, subject, toSave, urlStructure):
    f = Fernet(settings.CR_KEY)
    email = toSave.get('email')
    key = f.encrypt(bytes(email,encoding='utf-8')).decode('utf-8')
    code = generate_code(13)
    
    saveSmth(owner=code,smth=toSave)

    url = f"{domen}{urlStructure}?code={code}&key={key}"
    forWhat = url + "\n" + forWhat 
    message = render_to_string('emailMessageLink.html',
        {
            'username': username,
            'forWhat':forWhat,
        }
    )
    email = EmailMessage(subject,message, from_email='semen.vrazhkin@yandex.ru',to=[email,])
    email.send()

@shared_task
def sendInfo(email, username, info, subject):
    message = render_to_string('emailMessageInfo.html',
        {
            'username': username,
            'info': info
        }
    )
    email = EmailMessage(subject,message, from_email='semen.vrazhkin@yandex.ru',to=[email,])
    email.send()