import redis
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from cryptography.fernet import Fernet
from django.conf import settings
import urllib.parse
import json


domen = 'http://localhost:5173'

def generateKey(email):
    f = Fernet(settings.CR_KEY)
    return f.encrypt(bytes(email,encoding='utf-8')).decode('utf-8')

def saveSmth(owner, smth):
    r = connectToRedis()

    r.set(owner, json.dumps(smth))
    r.expire(owner, 900) #900 seconds = 15 min
    r.close()


def sendLink(email, username, forWhat, subject,toSave, urlStructure):

    key = generateKey(email)
    saveSmth(owner=email,smth=toSave)

    url = f"{domen}{urlStructure}?key={key}"
    forWhat = url + "\n" + forWhat 
    message = render_to_string('emailMessage.html',
        {
            'username': username,
            'forWhat':forWhat,
        }
    )
    email = EmailMessage(subject,message, from_email='semen.vrazhkin@yandex.ru',to=[email,])
    email.send()

def sendSmth(email, username, smth, subject):
    pass

def connectToRedis():
    return redis.StrictRedis(host='redis', port=6379, db=1, socket_timeout=None, connection_pool=None, charset='utf-8', errors='strict', unix_socket_path=None)

# CR_KEY = Fernet.generate_key()
# while True:
#     f = Fernet(CR_KEY)
#     token = f.encrypt(b"kirin3243@gmail.com") 
#     print(token.decode('utf-8'))
#     print(f.decrypt(token).decode('utf-8'))