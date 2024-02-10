from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.auth import get_user
from channels.db import database_sync_to_async
from django.db.models import F, Q, OuterRef, Subquery, Prefetch
from django.db.models.manager import BaseManager
from typing import Iterable, List
from django.utils import timezone
from .models import *
from apps.authentication.models import User
from apps.tools.db_tools import (
    async_filter_delete,
    async_filter_update,
    async_filter_exists,
    async_filter_values,
    async_filter_first,
    async_filter_count,
    async_filter_select_related
)
from apps.tools.validators import validate_json
import logging
from asgiref.sync import sync_to_async
from django.conf import settings

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
            'type': 'match_accepted',
            'hash': str
        }
    3) Игрок не принял игру:
        {
            'type': 'match_declined',
            'hash': str,
        }
    Отправляем сообщения вида:
    1) Пользователь был внесен в очередь:
        {
            "type": "player_in_queue"
        }
    2) Найдена игра:
        {
            'type': 'match_found'
            'count_of_players": int,
            'hash': str,
            "time_to_accept": int
        }
    2) Игра отменена игроком:
        {
            'type': 'match_canceled_by_user',
            "hash": str
        }
    3) Игра отменена по истечению времени:
        {
            "type": 'match_canceled_by_time',
            "hash": str
        }
    4) Все приняли игру:
        {
            'type': 'match_created',
            'hash': str,
            "players_info": {
                    "username": str,
                    "photo": str,
                    "elo": int,
                    "date_joined": str(date)
                }
        }
    """
    acceptable_keys = dict(
        enqueued={'target_players': int, 'game': str, 'elo_filter': bool},
        match_accepted={'hash': str},
        match_declined={'hash': str},
    )

    async def connect(self):

        user = await get_user(self.scope)
        if not (user and user.is_authenticated):
            await self.close()
            return
        self.username = user.username
        self.group_name = f'matchQueue_{self.username}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        if hasattr(self, 'group_name'):
            user = await get_user(self.scope)
            await async_filter_update(UserQueue, filters=dict(user=user.id), updates=dict(is_active=False))
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, data_json, **kwargs):
        user = await get_user(self.scope)
        if not (user and user.is_authenticated):
            await self.close()
            return
        message_type = data_json.pop('type', None)

        if message_type is None:
            await self.send_status_info('Invalid type', error=True)
            return

        if message_type not in self.acceptable_keys.keys():
            await self.send_status_info('Invalid type', error=True)
            return

        is_json_valid = await validate_json(data_json, self.acceptable_keys.get(message_type))

        if not is_json_valid:
            await self.send_status_info('Invalid data', error=True)
            return

        method = getattr(self, message_type)

        await method(data_json, user)

    @database_sync_to_async
    def filter_users_by_game(self, game, pk):
        return UserQueue.objects.filter(game=game, is_active=True).exclude(pk=pk).order_by('-queued_from')
    
    async def enqueued(self, data_json: dict, user: User):
        # Проверка, есть ли игра в базе данных
        game = await async_filter_first(Game,name=data_json.get('game', ''))
        if game is None:
            await self.send_status_info('Game not found', error=True)
            return

        data_json['game'] = game

        # Проверка, есть ли запись юзера в бд
        queued_user: UserQueue | None = await async_filter_first(UserQueue, user=user.pk)
        # Есть - обновляем
        if queued_user:
            if queued_user.is_active:
                await self.send_status_info("You're already in the queue", error=True)
                return
            
            if queued_user.match_found:
                await self.send_status_info("You're already in the game", error=True)
                return
            
            data_json['is_active'] = True
            for key,value in data_json.items():
                setattr(queued_user, key, value)
            await database_sync_to_async(queued_user.save)()

        # Если нет, то создаем
        else:
            data_json['user'] = user
            queued_user: UserQueue = UserQueue(**data_json)
            await database_sync_to_async(queued_user.save)()
        await self.player_in_queue({
            "type": "player_in_queue"
        })
        # Получение всех игроков в поиске с такой же игрой
        match_queues = await self.filter_users_by_game(game, queued_user.pk)

        await self.filter_elo(queued_user, game, match_queues, user)

    @database_sync_to_async
    def filter_users_by_elo(self, match_queues: BaseManager[UserQueue], elo_subquery, elo, **filters):
        return match_queues.filter(**filters).annotate(elo=Subquery(elo_subquery)).filter(elo__gt=elo-250, elo__lt=elo+250)
    
    @database_sync_to_async
    def tmp_filter(self, match_queues: BaseManager, elo_subquery, elo):
        return match_queues.annotate(elo=Subquery(elo_subquery)).filter(Q(elo__gt=elo-250, elo__lt=elo+250) | Q(elo_filter=False))

    @database_sync_to_async
    def log_info(self, to_log, message):
        logger = logging.getLogger(__name__)
        logger.info(f'{message}:{to_log}')

    async def filter_elo(self, queued_user: UserQueue, game: Game, match_queues: BaseManager[UserQueue], user: User):
        num_of_players_queued = await database_sync_to_async(match_queues.count)()
        await self.log_info(match_queues, 'got in filter_elo with that')
        if num_of_players_queued + 1 < game.min_players:
            return
        
        elo_subquery = UserElo.objects.filter(user=OuterRef('user'), game=game.id).values('elo')
        user_elo = await database_sync_to_async(UserElo.objects.get)(user=user.pk,game=game.pk)

        if queued_user.elo_filter:
            match_queues = await self.filter_users_by_elo(match_queues, elo_subquery, user_elo.elo, elo_filter=True)
            await self.filter_num_of_players(queued_user, game, match_queues)

        else:
            match_queues = await self.tmp_filter(match_queues, elo_subquery, user_elo.elo)
            await self.filter_num_of_players(queued_user, game, match_queues, user)
        
    @database_sync_to_async
    def get_targetPlayers_list(self, match_queues: BaseManager):
        return match_queues.exclude(target_players=None).distinct('target_players').values_list('target_players',flat=True)

    @database_sync_to_async
    def union_users(self, match_queues: BaseManager, item, to_union: BaseManager):
        return match_queues.filter(target_players=item).select_related('user', 'game').union(to_union).order_by('-queued_from')
    
    @database_sync_to_async
    def get_users_by_targetPlayers(self, match_queues: BaseManager, queued_user: UserQueue):
        return match_queues.filter(Q(target_players=queued_user.target_players) | Q(target_players=None)).select_related('user', 'game').order_by('-queued_from')

    async def filter_num_of_players(self, queued_user: UserQueue, game: Game, match_queues: BaseManager[UserQueue], user: User):
        num_of_players_queued = await database_sync_to_async(match_queues.count)()
        
        if num_of_players_queued + 1 < game.min_players:
            return
        await self.log_info(match_queues, 'got in filter_num_of_players with that')
        if not queued_user.target_players:
            # циклом пройтись по возможным кол-вам игроков
            target_players = await self.get_targetPlayers_list(match_queues)
            user_queue_none_target_players = await database_sync_to_async(match_queues.filter)(target_players=None)
            for item in target_players:
                players_found = await self.union_users(match_queues, item, user_queue_none_target_players)
                num_of_players_queued = await database_sync_to_async(match_queues.count)()
                num_of_players_queued += 1
                if not game.strict_num_of_players:

                    if num_of_players_queued >= game.max_players:
                        await self.create_match(players_found, game, queued_user, game.max_players, user)
                        return
                    else:
                        await self.create_match(players_found, game, queued_user, num_of_players_queued, user)
                        return

                elif num_of_players_queued >= game.strict_num_of_players:
                    await self.create_match(players_found, game, queued_user, game.strict_num_of_players, user)
                    return
        else:
            match_queues = await self.get_users_by_targetPlayers(match_queues, queued_user)
            num_of_players_queued = await database_sync_to_async(match_queues.count)()
            num_of_players_queued += 1
            if not game.strict_num_of_players:
                if num_of_players_queued >= queued_user.target_players and num_of_players_queued >= game.min_players:
                    await self.create_match(match_queues, game, queued_user, queued_user.target_players, user)
                    return
                
            elif num_of_players_queued >= game.strict_num_of_players:
                await self.create_match(match_queues, game, queued_user, game.strict_num_of_players, user)
                return
            
    @database_sync_to_async
    def create_userMatch_obj(self, **data):
        return UserMatch(**data)

    async def create_match(self, match_queues: BaseManager[UserQueue], game: Game, queued_user: UserQueue, num_of_players: int, user: User):
        match_instance: Match = await database_sync_to_async(Match.objects.create)(game=game)
        await self.log_info(match_queues, 'got into create_game with that:')
        user_match_objects = [await self.create_userMatch_obj(user=user, match=match_instance)]
        users_to_send = [user.username]
        count_of_added_players = 1
        match_queues_lst: list[UserQueue] = await sync_to_async(list)(match_queues)
        for match_queue in match_queues_lst:
            if count_of_added_players >= num_of_players:
                break

            user_match_objects.append(
                await self.create_userMatch_obj(user=match_queue.user, match=match_instance)
            )
            users_to_send.append(match_queue.user.username)
            count_of_added_players += 1

        await database_sync_to_async(UserMatch.objects.bulk_create)(user_match_objects)
        await self.update_match_queues_when_found(match_queues)

        await self.send_ready_messages(users_to_send, match_instance.hash)

    async def send_ready_messages(self, users: list[str], match_hash):
        time_to_accept = settings.TIME_TO_ACCEPT_A_GAME
        for user in users:
            await self.channel_layer.group_send(
                f'matchQueue_{user}',
                {
                    'type': 'match_found',
                    'count_of_players': len(users),
                    'hash': match_hash,
                    'time_to_accept': time_to_accept
                }
            )

    @database_sync_to_async
    def update_match_queues_when_found(self, match_queues: BaseManager[UserQueue]):
        match_queues.update(is_active=False, match_found=True)

    async def validate_and_change_status(self, match_instance: Match, user: User, make_accepted: bool) -> bool:
        if match_instance is None:
            await self.send_status_info(message='Invalid hash', error=True)
            return False
        
        if match_instance.status != match_instance.Status.CREATED:
            await self.send_status_info(message='Invalid data', error=True)
            return False

        if match_instance.date_to_confirm < timezone.now():
            await self.send_status_info(message='Time to accept match is over', error=True)
            return False

        user_match_instance: UserMatch | None = await async_filter_first(UserMatch, match=match_instance, user=user)

        if user_match_instance is None:
            await self.send_status_info(message="You can't perfome this action", error=True)
            return False

        if user_match_instance.is_accepted is not None:
            await self.send_status_info(message="You can't perfome this action", error=True)
            return False
        
        user_match_instance.is_accepted = make_accepted

        await database_sync_to_async(user_match_instance.save)()
        return True

    @database_sync_to_async
    def get_match(self, hash):
        return Match.objects.filter(hash=hash).select_related('game').first()

    async def match_accepted(self, data_json: dict, user: User):
        match_instance: Match | None = await self.get_match(data_json.get('hash', None))
        is_valid = await self.validate_and_change_status(match_instance, user, True)

        if not is_valid:
            return
        await self.send_status_info('Match was accepted succesfully')
        await self.check_if_all_accepted(match_instance)

    @database_sync_to_async
    def get_user_match_instances_and_elo(self, match: Match):
        elo_subq = UserElo.objects.filter(user=OuterRef('user'), game=match.game).values('elo')[:1]
        return UserMatch.objects.filter(match=match).annotate(elo=Subquery(elo_subq)).select_related('user')

    async def check_if_all_accepted(self, match: Match):
        user_match_instances: BaseManager[UserMatch] = await self.get_user_match_instances_and_elo(match)
        count_not_accepted = await async_filter_count(UserMatch, Q(is_accepted=False) | Q(is_accepted=None), base_manager=user_match_instances)
        if count_not_accepted != 0:
            return
        
        match.status = match.Status.PREPARING
        await database_sync_to_async(match.save)()
        user_match_instances_list = await sync_to_async(list)(user_match_instances)
        await self.send_match_created_messages(user_match_instances_list, match.hash)


    async def send_match_created_messages(self, to_send: list[UserMatch], match_hash: str):
        players_info = []
        for user_match in to_send:
            players_info.append(
                {
                    "username": user_match.user.username,
                    "photo": user_match.user.photo_url,
                    "elo": user_match.elo,
                    "date_joined": user_match.user.date_joined.strftime("%Y-%m-%d")
                }
            )

        for user_match in to_send:
            await self.channel_layer.group_send(
                f'matchQueue_{user_match.user.username}',
                {
                    'type': 'match_created',
                    'hash': match_hash,
                    "players": players_info
                }
            )

    async def match_declined(self, data_json: dict, user: User):
        match_instance: Match | None = await self.get_match(data_json.get('hash', None))
        is_valid = await self.validate_and_change_status(match_instance, user, False)
        if not is_valid:
            return
        await self.send_status_info('Match was declined succesfully')
        user_match_instances_list = await self.cancel_match(match_instance)
        await self.send_match_cancel_messages(user_match_instances_list, match_instance.hash)

    async def cancel_match(self, match_instance: Match):
        user_match_instances: BaseManager[UserMatch] = await async_filter_select_related(UserMatch, ['user'], match=match_instance)
        match_instance.status = match_instance.Status.CANCELED
        await database_sync_to_async(match_instance.save)()
        user_match_instances_list = await sync_to_async(list)(user_match_instances)
        return user_match_instances_list
        
    async def send_match_cancel_messages(self, to_send: list[UserMatch], match_hash: str):
        for user_match in to_send:
            await self.channel_layer.group_send(
                f'matchQueue_{user_match.user.username}',
                {
                    'type': 'match_canceled_by_user',
                    'hash': match_hash
                }
            )

    async def match_found(self, event):
        await self.send_json(event)

    async def match_created(self, event):
        await self.send_json(event)
        await self.close()

    async def match_canceled_by_user(self, event):
        await self.send_json(event)

    async def match_canceled_by_time(self, event):
        await self.send_json(event)

    async def player_in_queue(self, event):
        await self.send_json(event)

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
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        pass

    async def game_status_changed(self, event):
        pass
