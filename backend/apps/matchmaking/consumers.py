from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.auth import get_user
from channels.db import database_sync_to_async
from django.db.models import F, Q, OuterRef, Subquery
from django.db.models.manager import BaseManager
from typing import Iterable, List
import json
from .models import *
from apps.authentication.models import User
from apps.tools.db_tools import (
    async_filter_delete,
    async_filter_update,
    async_filter_exists,
    async_filter_values
)
from apps.tools.validators import validate_json


class MatchQueueConsumer(AsyncJsonWebsocketConsumer):
    """
    Получаем сообщения вида:
    1) При заходе в очередь
        {
            'type': enqueued,
            'eloFilter': bool,
            'targetPlayers': int,
            'game': str,
        }
    2) Игрок принял игру:
        {
            'type': 'game_accepted',
            'hash': str
        }
    3) Игрок не принял игру:
        {
            'type': 'game_canceled_by_user',
            'hash': str,
        }
    4) Если таймер принятия истек, и кто-то не принял:
        {
            'type': 'game_canceled_by_user',
            'hash': str
        }
    Отправляем сообщения вида:
    1) Найдена игра:
        {
            'type': 'game_ready'
            'count_of_players': int,
            'hash': str,
        }
    2) Игра отменена:
        {
            'type': 'game_canceled',
            "hash": str
        }
    3) Все приняли игру:
        {
            'type': 'game_created',
            'hash': str
        }
    """
    acceptable_keys = dict(
        enqueued=('eloFilter', 'targetPlayers', 'game'),
        game_accepted=('hash'),
        game_canceled_by_user=('hash'),
    )
    types = ('enqueued', 'game_accepted', 'game_canceled_by_user')

    async def connect(self):

        user = await get_user(self.scope)
        if user and user.is_authenticated:
            self.username = user.username
            self.group_name = f'matchQueue_{self.username}'
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, code):
        if self.group_name:
            user = await get_user(self.scope)
            await async_filter_update(UserQueue, dict(user=user.id), dict(active=False))
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    @database_sync_to_async
    def elo_query(self, match_queues, elo_subquery, elo):
        return match_queues.filter(eloFilter=True).annotate(elo=Subquery(
            elo_subquery)).filter(elo__gt=elo+250, elo__lt=elo-250)

    async def receive(self, text_data):
        user = await get_user(self.scope)
        if not (user and user.is_authenticated):
            await self.close()

        data_json: dict = json.loads(text_data)

        message_type = data_json.get('type')

        if not message_type:
            await self.send_status_info('Invalid data', error=True)
            return

        if message_type not in self.types:
            await self.send_status_info('Invalid data', error=True)
            return

        is_json_valid = await validate_json(data_json, self.acceptable_keys.get(message_type))

        if not is_json_valid:
            await self.send_status_info('Invalid data', error=True)
            return
        data_json.pop('type')
        method = getattr(self, message_type)

        await method(data_json, user)

    async def enqueued(self, data_json: dict, user: User):
        # Проверка, есть ли игра в базе данных
        does_game_exist = await async_filter_exists(name=data_json.get('game', ''))
        if not does_game_exist:
            await self.send_status_info('Game not found', error=True)
            return
        game: Game = await database_sync_to_async(Game.objects.get)(name=data_json.get('game', ''))
        data_json['game'] = game

        # Проверка, есть ли запись юзера в бд
        queuedBeforeUser = database_sync_to_async(
            UserQueue.objects.filter)(user=user)
        # Есть - обновляем
        if queuedBeforeUser:
            data_json['active'] = True
            database_sync_to_async(queuedBeforeUser.update)(
                **data_json)
            queuedUser = await database_sync_to_async(UserQueue.objects.get)(user=user)

        # Если нет, то создаем
        else:
            data_json['user'] = user
            queuedUser: UserQueue = await database_sync_to_async(UserQueue.objects.create)(**data_json)

        # Получение всех игроков в поиске с такой же игрой
        match_queues = await database_sync_to_async(UserQueue.objects.filter)(
            game=game, active=True)
        match_queues = await database_sync_to_async(match_queues.select_related)('user', 'game')
        match_queues = await database_sync_to_async(match_queues.order_by)('-queuedFrom')
        
        # Не нашлось игроков - выходим
        if len(match_queues) < game.minPlayers:
            return

        if queuedUser.eloFilter:
            elo_subquery = await async_filter_values(UserElo, values=('elo'), border=1, user=OuterRef('user'), game=game.id)
            userElo = await database_sync_to_async(UserElo.objects.get)(user=queuedUser.user)
            match_queues = await self.elo_query(match_queues, elo_subquery, userElo.elo)
        else:
            match_queues = await database_sync_to_async(match_queues.filter)(eloFilter=False)

        if len(match_queues) < game.minPlayers:
            return

        # Проверка, на фильтрацию по кол-ву игроков
        if not queuedUser.targetPlayers:
            # циклом пройтись по возможным кол-вам игроков
            numOfPlayersQueued = len(match_queues)

            if not game.strictNumOfPlayers:

                if numOfPlayersQueued >= game.maxPlayers:
                    await self.createGame(match_queues, game, game.maxPlayers)
                else:
                    await self.createGame(match_queues, game, numOfPlayersQueued)

            elif numOfPlayersQueued == game.strictNumOfPlayers:
                await self.createGame(match_queues, game, numOfPlayersQueued)
        else:
            if not game.strictNumOfPlayers:
                match_queues = database_sync_to_async(match_queues.filter)(
                    Q(targetPlayers=queuedUser.targetPlayers) | Q(targetPlayers=None))
                if len(match_queues) >= queuedUser.targetPlayers and len(match_queues) >= game.minPlayers:
                    await self.createGame(match_queues=match_queues, game=game, numOfPlayers=len(match_queues))

    async def createGame(self, match_queues: BaseManager[UserQueue], game, numOfPlayers=None):
        match: Match = await database_sync_to_async(Match.objects.create)(game=game)
        user_match_objects = []
        users_to_send = []
        count_of_added_players = 0
        for match_queue in match_queues:
            if count_of_added_players == numOfPlayers:
                break

            user_match_objects.append(
                UserMatch(user=match_queue.user, match=match)
            )
            users_to_send.append(match_queue.user.username)
            count_of_added_players += 1

        await database_sync_to_async(UserMatch.objects.bulk_create)(user_match_objects)
        await database_sync_to_async(match_queues.update)(active=False)
        await self.send_ready_messages(user_match_objects, match.hash)

    async def send_ready_messages(self, users: List[User], hash):
        for user in users:
            await self.channel_layer.group_send(
                f'matchQueue_{user.username}',
                {
                    'type': 'game_ready',
                    'count_of_players': len(users),
                    'hash': hash,
                }
            )

    async def game_accepted(self, data_json: dict, user: User):
        pass

    async def game_canceled_by_user(self, data_json: dict, user: User):
        pass

    async def game_ready(self, event):
        await self.send_json(event)

    async def game_created(self, event):
        pass

    async def game_canceled(self, event):
        pass

    async def send_status_info(self, message, error=False):
        await self.send_json(
            {
                'status': 'error' if error else 'success',
                'message': message
            }
        )


class MatchConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        pass

    async def disconnect(self, code):
        if self.group_name:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        pass

    async def game_status_changed(self, event):
        pass
