from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.auth import get_user, logout
from channels.db import database_sync_to_async
from django.db.models import Q, Case, When
from typing import Iterable
import json
from apps.friends.models import Friendship
from apps.authentication.models import User
from apps.tools.db_tools import async_filter_exists, async_filter_update, async_filter_delete, async_filter_first
from apps.tools.caching import delete_cache
from apps.tools.extended_consumer import ExtendedAsyncConsumer

class FriendConsumer(ExtendedAsyncConsumer):
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
    acceptable_keys = dict(
        create_invite={'username': str},
        accept_invite={'username': str},
        cancel_invite={'username': str},
        decline_invite={'username': str},
        delete_friend={'username': str}
    )
    group_name_prefix = 'friends'
    target_user: User | None = None

    async def connect(self):
        method_to_call = await self.general_connect()

        await method_to_call()

    async def disconnect(self, close_code):
        await self.discard_group()

    @database_sync_to_async
    def delete_friend_query(self, model: User | Friendship, filter, **updates):
        return model.objects.filter(filter).update(**updates)

    async def receive_json(self, data_json: dict, **kwargs):

        method_to_call = await super().receive_json(data_json, **kwargs)
        if method_to_call is None:
            return
        target_username = data_json.get('username')
        
        if target_username == self.user.username:
            await self.send_status_info(message='Invalid data', error=True)
            return
        
        self.target_user: User | None = await async_filter_first(User, username=target_username)

        if self.target_user is None:
            await self.send_status_info(message='Not found', error=True)
            return

        await method_to_call()

    async def create_invite(self):
        flag = await async_filter_exists(Friendship, Q(inviter=self.user, accepter=self.target_user) | Q(inviter=self.target_user, accepter=self.user))
        if flag:
            await self.send_status_info(message=f'Невозможно создать заявку', error=True)
            return

        await database_sync_to_async(Friendship.objects.create)(
            inviter=self.user, accepter=self.target_user, status=Friendship.Status.INVITED)
        await self.send_status_info(message='Заявка успешно создана')
        await self.channel_layer.group_send(
            f'friends_{self.target_user.username}',
            {'type': f'incoming_invite', "username": self.user.username,
                'photo': self.user.photo_url}
        )
        await self.invalidate_cache(self.target_user.username, self.user.username)
        await self.invalidate_cache(self.user.username, self.target_user.username)

    async def cancel_invite(self):
        flag = await async_filter_exists(Friendship, inviter=self.user, accepter=self.target_user, status=Friendship.Status.INVITED)
        if not flag:
            await self.send_status_info(message='Заявки не существует', error=True)
            return

        await async_filter_delete(Friendship, inviter=self.user, accepter=self.target_user)

        await self.send_status_info(message='Заявка успешно отменена')
        await self.invalidate_cache(self.target_user.username, self.user.username)
        await self.invalidate_cache(self.user.username, self.target_user.username)

    async def accept_invite(self):
        flag = await async_filter_exists(Friendship, inviter=self.target_user, accepter=self.user, status=Friendship.Status.INVITED)
        if not flag:
            await self.send_status_info(message='Заявки не существует', error=True)
            return

        await async_filter_update(
            Friendship,
            filters=dict(inviter=self.target_user, accepter=self.user),
            updates=dict(status=Friendship.Status.FRIENDS)
        )

        await self.send_status_info(message='Заявка успешно принята')

        await self.channel_layer.group_send(
            f'friends_{self.target_user.username}',
            {'type': f'accepted_invite', "username": self.user.username,
                "photo": self.user.photo_url}
        )

        await self.invalidate_cache(self.target_user.username, self.user.username)
        await self.invalidate_cache(self.user.username, self.target_user.username)

    async def decline_invite(self):
        flag = await async_filter_exists(Friendship, inviter=self.target_user, accepter=self.user, status=Friendship.Status.INVITED)
        if not flag:
            await self.send_status_info(message='Заявки не существует', error=True)
            return

        await async_filter_delete(Friendship, inviter=self.target_user, accepter=self.user)

        await self.send_status_info(message='Заявка успешно отклонена')

        await self.invalidate_cache(self.target_user.username, self.user.username)
        await self.invalidate_cache(self.user.username, self.target_user.username)

    async def delete_friend(self):
        flag = await async_filter_exists(
            Friendship,
            Q(inviter=self.target_user, accepter=self.user, status=Friendship.Status.FRIENDS) | Q(
                inviter=self.user, accepter=self.target_user, status=Friendship.Status.FRIENDS)
        )
        if not flag:
            await self.send_status_info(message='Вы не друзья', error=True)
            return

        await self.delete_friend_query(
            Friendship,
            Q(inviter=self.target_user, accepter=self.user, status=Friendship.Status.FRIENDS) |
            Q(inviter=self.user, accepter=self.target_user,
              status=Friendship.Status.FRIENDS),
            inviter=self.target_user, accepter=self.user, status=Friendship.Status.INVITED
        )
        await self.send_status_info(message='Пользователь успешно удалён из друзей')

        await self.invalidate_cache(self.target_user.username, self.user.username)
        await self.invalidate_cache(self.user.username, self.target_user.username)

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
