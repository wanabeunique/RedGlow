from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.auth import get_user, logout
from channels.db import database_sync_to_async
from typing import Iterable
import json
from apps.friends.models import Friendship
from apps.authentication.models import User
from django.db.models import Q


class FriendConsumer(AsyncJsonWebsocketConsumer):
    """
    Фронтенд отправляет сообщение вида:
        {
            "type": str,
            "username": str,
        }
    где username - это username пользователя, относительно которого производится действие
    Варианты type:
    - Отправка заявки
        "type": "create_intive"
    - Отмена отправки
        "type": "cancel_intive"
    - Принятие заявки
        "type": "accept_intive"
    - Отклонение заявки
        "type": "decline_intive"
    - Удаление друга
        "type": "delete_friend"
    Фронтенд получает сообщение вида:
        {
            "type": str,
            "username": str,
            "photo": str
        }
    Варианты type:
    - Входящая заявка
        "type": "incoming_intive"
    - Отправленная заявка принята
        "type": "accepted_invite"
    """
    keys = ['type', 'username']

    async def connect(self):
        user = await get_user(self.scope)
        if not (user and user.is_authenticated):
            await self.close()
            return

        self.username = user.username
        self.group_name = f'friends_{self.username}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        if self.group_name:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):

        user = await get_user(self.scope)
        if not (user and user.is_authenticated):
            await self.close()
            return

        data_json: dict = json.loads(text_data)
        if not validate_json(data_json, self.keys):
            await self.send_status_info(message='Invalid data', status='error')
            return

        target_username = data_json.get('username')

        if user.username == target_username:
            await self.send_status_info(message='Invalid data', status='error')
            return

        if not User.objects.filter(username=target_username).exists():
            await self.send_status_info(message='Not found', status='error')
            return

        target_user = await User.objects.aget(username=target_username)
        message_type = data_json.get('type')
        method = getattr(self, message_type)

        method(target_username, target_user, user)

    async def create_invite(self, target_username: str, target_user: User, current_user: User):

        try:
            await Friendship.objects.acreate(inviter=current_user, accepter=target_user)
            await self.send_status_info(message='Заявка успешно создана')
            await self.channel_layer.group_send(
                f'friends_{target_username}',
                {'type': f'incoming_invite', "username": current_user.username,
                    'photo': current_user.photo_url}
            )
        except:
            await self.send_status_info(message='Ошибка при создании заявки', error=True)

    async def cancel_invite(self, target_username: str, target_user: User, current_user: User):
        if not Friendship.objects.filter(inviter=current_user, accepter=target_user, status=Friendship.Status.INVITED).exists():
            await self.send_status_info(message='Заявки не существует', error=True)
            return

        Friendship.objects.filter(
            inviter=current_user, accepter=target_user).delete()

        await self.send_status_info(message='Заявка успешно отменена')

    async def accept_invite(self, target_username: str, target_user: User, current_user: User):
        if not Friendship.objects.filter(inviter=target_user, accepter=current_user, status=Friendship.Status.INVITED).exists():
            await self.send_status_info(message='Заявки не существует', error=True)
            return

        Friendship.objects.filter(inviter=target_user, accepter=current_user).update(
            status=Friendship.Status.FRIENDS)

        await self.send_status_info(message='Заявка успешно принята')

        await self.channel_layer.group_send(
            f'friends_{target_username}',
            {'type': f'accepted_invite', "username": current_user.username,
                "photo": current_user.photo_url}
        )

    async def decline_invite(self, target_username: str, target_user: User, current_user: User):
        if not Friendship.objects.filter(inviter=target_user, accepter=current_user, status=Friendship.Status.INVITED).exists():
            await self.send_status_info(message='Заявки не существует', error=True)
            return

        Friendship.objects.filter(
            inviter=target_user, accepter=current_user).delete()

        await self.send_status_info(message='Заявка успешно отклонена')

    async def delete_friend(self, target_username: str, target_user: User, current_user: User):

        if not Friendship.objects.filter(
            Q(inviter=target_user, accepter=current_user, status=Friendship.Status.FRIENDS) | Q(
                inviter=current_user, accepter=target_user, status=Friendship.Status.FRIENDS)
        ).exists():
            await self.send_status_info(message='Вы не друзья', error=True)
            return

        Friendship.objects.filter(
            Q(inviter=target_user, accepter=current_user, status=Friendship.Status.FRIENDS) | Q(
                inviter=current_user, accepter=target_user, status=Friendship.Status.FRIENDS)
        ).delete()

        await self.send_status_info(message='Пользователь успешно удалён из друзей')

    async def incoming_invite(self, event):
        await self.send_json(event)

    async def accepted_invite(self, event):
        await self.send_json(event)

    async def send_status_info(self, message, error=False):
        await self.send_json(
            {
                'status': 'error' if error else 'success',
                'message': message
            }
        )


def validate_json(json: dict, keys: list) -> bool:
    if not isinstance(json, dict):
        return False
    if not isinstance(keys, Iterable):
        return False

    for item in json.keys():
        if item not in keys:
            return False
        keys.remove(item)

    return True
