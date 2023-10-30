from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.core.cache import cache
from django.contrib.auth.hashers import make_password
import hashlib
from celery import shared_task
import random
import string

domen = 'https://localhost'

@shared_task
def saveSmth(owner, smth):
    cache.set(owner, smth,900)

@shared_task
def generate_code(num) -> str:

    code = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(num))
    return code

@shared_task
def sendLink(username, forWhat, subject, toSave, urlStructure):
    email: str = toSave.get('email')
    password = toSave.get('password')
    if password:
        toSave['password'] = make_password(password)
    key = hashlib.sha256(email.encode('utf-8')).hexdigest()
    code = generate_code(13)
    saveSmth(owner=key,smth=code)
    saveSmth(owner=code+key,smth=toSave)

    url = f"{domen}{urlStructure}?code={code}&email={email}"
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