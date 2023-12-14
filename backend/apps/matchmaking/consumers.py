from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.auth import get_user
from channels.db import database_sync_to_async
from django.db.models import F, Q, OuterRef, Subquery
from .models import *
import json
import typing


class MatchQueueConsumer(AsyncJsonWebsocketConsumer):
    """
    Получаем сообщение вида:
    {
        'type': queued,
        'elo_filter': bool,
        'target_players': int,
        'game': str,
    }
    Отправляем, когда найдена игра:
    {
        'type': 'game_ready'
        'count_of_players': int,
        'hash': str,
    }
    После этого все игроки должны принять игру. При принятии, получаем сообщение вида:
    {
        'type': 'game_accepted'
    }
    Если хотя бы один игрок не принял игру, то принимаем:
    {
        'type': 'game_canceled_by_user',
        'hash': str,
    }
    Если таймер принятия истек, и кто-то не принял, принимаем:
    {
        'type': 'game_canceled_by_user',
        'hash': str
    }
    А потом отправляем:
    {
        'type': 'game_canceled'
    }
    Все приняли игру, отправляем:
    {
        'type': 'game_created',
        'hash': str
    }
    """
    queued_keys = ('type', 'elo_filter', 'target_players', 'game')

    async def connect(self):

        user = await get_user(self.scope)
        if user and user.is_authenticated:
            self.username = user.username
            self.group_name = f'matchQueues_{self.username}'
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, code):
        user = await get_user(self.scope)
        MatchQueue.objects.filter(user=user.id).update(active=False)
        if self.group_name:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        user = await get_user(self.scope)
        if not (user and user.is_authenticated):
            await self.close()

        dataJson: dict = json.loads(text_data)

        if dataJson.get('type') == 'queued':
            await self.validate_queued(dataJson, user)

        elif dataJson.get('type') == 'game_accepted':
            pass

        elif dataJson.get('type') == 'game_canceled_by_user':
            pass

    async def validate_queued(self, dataJson: dict, user):
        matchQueueInstance = validatedJson(dataJson, self.queued_keys)
        if not matchQueueInstance:
            return

        # Проверка, есть ли игра в базе данных
        try:
            matchQueueInstance['game'] = await Game.objects.aget(name=dataJson.get('game', ''))
        except Game.DoesNotExist:
            return

        # Проверка, есть ли запись юзера в бд

        # Есть - обновляем
        queuedBeforeUser = database_sync_to_async(
            UserMatchQueue.objects.filter)(user=user)

        if queuedBeforeUser:

            database_sync_to_async(queuedBeforeUser.update)(
                **matchQueueInstance)
            queuedUser = await UserMatchQueue.objects.aget(user=user)

        # Если нет, то создаем
        else:
            matchQueueInstance['user'] = user
            queuedUser = await UserMatchQueue.objects.acreate(**matchQueueInstance)

        # Получение всех игроков в поиске с такой же игрой
        match_queues = UserMatchQueue.objects.filter(
            game=queuedUser.game, active=True).prefetch_related('user', 'game').order_by('queuedFrom')

        if not match_queues:
            return

        await self.filterQueue(queuedUser, match_queues, queuedUser.game)

    async def filterQueue(self, queuedUser: UserMatchQueue, match_queues, game: Game):
        # Проверка, на фильтрацию по рейтингу
        if queuedUser.eloFilter:
            elo_subquery = UserElo.objects.filter(
                user=OuterRef('user')).values('elo')[:1]
            userElo = await UserElo.objects.aget(user=queuedUser.user)
            match_queues = match_queues.filter(eloFilter=True).annotate(elo=Subquery(
                elo_subquery)).filter(elo__gt=userElo.elo+250, elo__lt=userElo.elo-250)

        else:
            match_queues = match_queues.filter(eloFilter=False)

        # Проверка, на фильтрацию по кол-ву игроков
        if not queuedUser.targetPlayers:

            numOfPlayersQueued = len(match_queues)
            if not game.strictNumOfPlayers:
                if numOfPlayersQueued >= 4:
                    if numOfPlayersQueued >= game.maxPlayers:
                        await self.createGame(match_queues, game, game.maxPlayers)
                    else:
                        numOfPlayersQueued
            elif numOfPlayersQueued == game.strictNumOfPlayers:
                await self.createGame(match_queues, game, numOfPlayersQueued)

        else:
            if not game.strictNumOfPlayers:
                match_queues = match_queues.filter(
                    Q(targetPlayers=queuedUser.targetPlayers) | Q(targetPlayers=None))
                if len(match_queues) >= queuedUser.targetPlayers:
                    # Отправить собщение о найденной игре
                    await self.createGame(match_queues=match_queues, game=game, numOfPlayers=queuedUser.targetPlayers)
                return

    async def createGame(self, match_queues, game, numOfPlayers=None):
        match = await Match.objects.acreate(game=game)
        userMatchObjects = []
        for matchQueue in match_queues:
            userMatchObjects.append(
                UserMatch(user=matchQueue.user, match=match)
            )
        await UserMatch.objects.abulk_create(userMatchObjects)
        match_queues.update(active=False)
        await self.sendRdyMessages(match_queues)

    async def sendRdyMessages(self, matchQueues, type, hash):
        for instance in matchQueues:
            await self.channel_layer.group_send(
                f'matchQueues_{instance.user.username}',
                {
                    'type': f'game.ready',
                    "count_of_players": len(matchQueues),
                    'gameHash': hash
                }
            )

    async def game_ready(self, event):
        await self.send(text_data=json.dumps(
            {
                "type": 'game_ready',
                'count_of_players': event.get('count_of_players'),
                'hash': event.get('hash')
            }
        ))

        pass

    async def game_accepted(self, event):
        await self.send(text_data=json.dumps({"type": 'game_accepted'}))

    async def game_created(self, event):
        await self.send(text_data=json.dumps({"type": 'game_created', 'game_hash': event.get('game_hash')}))

    async def game_canceled(self, event):
        pass


def validatedJson(self, json: dict, keys: typing.Iterable) -> dict | None:
    if not isinstance(json, dict):
        return None
    if not isinstance(keys, typing.Iterable):
        return None
    tmp = {}
    for key in keys:
        if key in json.keys():
            value = json.get(key, '')
            if value == '':
                return None
            else:
                if key != 'type':
                    tmp[key] = value
        else:
            return None
    tmp['active'] = True
    return tmp


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
