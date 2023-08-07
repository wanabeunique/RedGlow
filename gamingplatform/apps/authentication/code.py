import redis
from random import randint
from django.core.mail import EmailMessage
from django.template.loader import render_to_string 

def generateCode():
    return ''.join(str(randint(0, 9)) for i in range(7))

def saveEmailCode(email, code):
    r = redis.StrictRedis(host='localhost', port=6379, db=0, password='SeMeN4565', socket_timeout=None, connection_pool=None, charset='utf-8', errors='strict', unix_socket_path=None)

    r.set(email, code)
    r.expire(email, 900) #900 seconds = 15 min
    r.close()

def sendEmailCode(email,username, forWhat):
    code = generateCode() 
    saveEmailCode(email, code)

    mail_subject = 'Код активации'
    message = render_to_string('emailMessage.html',
        {
            'username': username,
            'code': code,
            'forWhat':forWhat,
        }
    )
    email = EmailMessage(mail_subject,message, from_email='semen.vrazhkin@yandex.ru',to=[email,])
    email.send()