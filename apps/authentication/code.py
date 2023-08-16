import redis
from random import randint
from django.core.mail import EmailMessage
from django.template.loader import render_to_string 

def generateCode():
    return ''.join(str(randint(0, 9)) for i in range(7))

def saveSmth(email, smth):
    r = connectToRedis()

    r.set(email, smth)
    r.expire(email, 900) #900 seconds = 15 min
    r.close()

def sendEmailCode(email,username, forWhat):
    code = generateCode() 
    saveSmth(email, code)

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

def sendLink(email, username, forWhat):
    hashEmail = f"fnox+{hash(email)}+{hash(username)}+{email}"
    saveSmth(email,hashEmail)

    mail_subject = 'Ссылка для смены пароля'
    message = render_to_string('emailMessage.html',
        {
            'username': username,
            'code': f'http://localhost:5173/forgot/password?key={hashEmail}',
            'forWhat':forWhat,
        }
    )
    email = EmailMessage(mail_subject,message, from_email='semen.vrazhkin@yandex.ru',to=[email,])
    email.send()

def connectToRedis():
    return redis.StrictRedis(host='redis', port=6379, db=0, socket_timeout=None, connection_pool=None, charset='utf-8', errors='strict', unix_socket_path=None)