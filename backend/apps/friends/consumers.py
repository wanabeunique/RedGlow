from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.auth import get_user, logout
from channels.db import database_sync_to_async
from django.db.models import Q, Case, When
from typing import Iterable
import json
from apps.friends.models import Friendship
from apps.authentication.models import User
from apps.tools.db_tools import async_filter_exists, async_filter_update, async_filter_delete
from apps.tools.caching import delete_cache
import logging

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
        "type": "create_invite"
    - Отмена отправки
        "type": "cancel_invite"
    - Принятие заявки
        "type": "accept_invite"
    - Отклонение заявки
        "type": "decline_invite"
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
        "type": "incoming_invite"
    - Отправленная заявка принята
        "type": "accepted_invite"
    """
    types = ['create_invite', 'accept_invite',
             "cancel_invite", "decline_invite", "delete_friend"]

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
        if hasattr(self,"group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    @database_sync_to_async
    def delete_friend_query(self, model: User | Friendship, filter, **updates):
        return model.objects.filter(filter).update(**updates)

    async def receive(self, text_data):

        user = await get_user(self.scope)
        if not (user and user.is_authenticated):
            await self.close()
            return

        data_json: dict = json.loads(text_data)
        if data_json.get('type', None) is None or data_json.get('username', None) is None:
            await self.send_status_info(message='Invalid data', error=True)
            return

        target_username = data_json.get('username')

        if user.username == target_username:
            await self.send_status_info(message='Invalid data', error=True)
            return

        user_flag = await async_filter_exists(User, username=target_username)

        if not user_flag:
            await self.send_status_info(message='Not found', error=True)
            return

        target_user = await database_sync_to_async(
            User.objects.get)(username=target_username)
        message_type = data_json.get('type')

        if not message_type:
            await self.send_status_info(message='Invalid data', error=True)
            return

        if message_type not in self.types:
            await self.send_status_info(message='Invalid data', error=True)
            return

        method = getattr(self, message_type)

        await method(target_username, target_user, user)

    async def create_invite(self, target_username: str, target_user: User, current_user: User):
        flag = await async_filter_exists(Friendship, Q(inviter=current_user, accepter=target_user) | Q(inviter=target_user, accepter=current_user))
        if flag:
            await self.send_status_info(message=f'Невозможно создать заявку', error=True)
            return

        await database_sync_to_async(Friendship.objects.create)(
            inviter=current_user, accepter=target_user, status=Friendship.Status.INVITED)
        await self.send_status_info(message='Заявка успешно создана')
        await self.channel_layer.group_send(
            f'friends_{target_username}',
            {'type': f'incoming_invite', "username": current_user.username,
                'photo': current_user.photo_url}
        )
        await self.invalidate_cache(target_username, current_user.username)
        await self.invalidate_cache(current_user.username, target_username)

    async def cancel_invite(self, target_username: str, target_user: User, current_user: User):
        flag = await async_filter_exists(Friendship, inviter=current_user, accepter=target_user, status=Friendship.Status.INVITED)
        if not flag:
            await self.send_status_info(message='Заявки не существует', error=True)
            return

        await async_filter_delete(Friendship, inviter=current_user, accepter=target_user)

        await self.send_status_info(message='Заявка успешно отменена')
        await self.invalidate_cache(target_username, current_user.username)
        await self.invalidate_cache(current_user.username, target_username)

    async def accept_invite(self, target_username: str, target_user: User, current_user: User):
        flag = await async_filter_exists(Friendship, inviter=target_user, accepter=current_user, status=Friendship.Status.INVITED)
        if not flag:
            await self.send_status_info(message='Заявки не существует', error=True)
            return

        await async_filter_update(
            Friendship,
            filters=dict(inviter=target_user, accepter=current_user),
            updates=dict(status=Friendship.Status.FRIENDS)
        )

        await self.send_status_info(message='Заявка успешно принята')

        await self.channel_layer.group_send(
            f'friends_{target_username}',
            {'type': f'accepted_invite', "username": current_user.username,
                "photo": current_user.photo_url}
        )

        await self.invalidate_cache(target_username, current_user.username)
        await self.invalidate_cache(current_user.username, target_username)

    async def decline_invite(self, target_username: str, target_user: User, current_user: User):
        flag = await async_filter_exists(Friendship, inviter=target_user, accepter=current_user, status=Friendship.Status.INVITED)
        if not flag:
            await self.send_status_info(message='Заявки не существует', error=True)
            return

        await async_filter_delete(Friendship, inviter=target_user, accepter=current_user)

        await self.send_status_info(message='Заявка успешно отклонена')

        await self.invalidate_cache(target_username, current_user.username)
        await self.invalidate_cache(current_user.username, target_username)

    async def delete_friend(self, target_username: str, target_user: User, current_user: User):
        flag = await async_filter_exists(
            Friendship,
            Q(inviter=target_user, accepter=current_user, status=Friendship.Status.FRIENDS) | Q(
                inviter=current_user, accepter=target_user, status=Friendship.Status.FRIENDS)
        )
        if not flag:
            await self.send_status_info(message='Вы не друзья', error=True)
            return

        await self.delete_friend_query(
            Friendship,
            Q(inviter=target_user, accepter=current_user, status=Friendship.Status.FRIENDS) |
            Q(inviter=current_user, accepter=target_user,
              status=Friendship.Status.FRIENDS),
            inviter=target_user, accepter=current_user, status=Friendship.Status.INVITED
        )
        await self.send_status_info(message='Пользователь успешно удалён из друзей')

        await self.invalidate_cache(target_username, current_user.username)
        await self.invalidate_cache(current_user.username, target_username)

    async def invalidate_cache(self, username1, username2):
        delete_cache('friendship_status', f'/user/friendship/{username1}/',username2)
        delete_cache('friendship_status', f'/user/friendship/{username2}/',username1)

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
