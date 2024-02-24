from .models import UserQueue
from apps.tools.db_tools import (
    async_filter_update,
    async_filter_first
)
from .matchmaking_helpers.mm_queue import MatchMakingQueue
from .matchmaking_helpers.mm_decision import MatchMakingDecision
from .models import UserBan, Game
from apps.tools.exceptions import ValidationError
from apps.tools.extended_consumer import ExtendedAsyncConsumer
from channels.auth import get_user
from apps.authentication.models import User
from django.db.models import Q
from django.forms import model_to_dict
from channels.db import database_sync_to_async
import logging
class MatchQueueConsumer(ExtendedAsyncConsumer):
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
            'type': 'accept_match',
            'hash': str
        }
    3) Игрок не принял игру:
        {
            'type': 'decline_match',
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
    5) Успешное принятие игры:
        {
            "type": "match_accepted"
        }
    6) Успешное отклонение игры:
        {
            "type": "match_declined"
        }
    7) Кол-во принятых игру:
        {
            'type': 'count_of_accepted',
            'hash': str,
            'count': int
        }
    8) Игрок забанился(ban_ends_at: None означает, что бан перманентный):
        {
            'type': 'player_got_banned',
            'ban_ends_at': str(datetime)
        }
    9) Игрок не может играть в мм по каким то другим причинам(например, не привязан стим):
        {
            'type': 'unable_to_play_mm',
            'reason': str
        }
    10) Настройки выбранной игры
        {
            'type': 'game_settings',
            'name': str,
            'strict_num_of_players': int,
            'min_players': int,
            'max_players': int
        }
    """
    acceptable_keys = dict(
        enqueued={'target_players': int | None, 'game': str, 'elo_filter': bool},
        accept_match={'hash': str},
        decline_match={'hash': str},
    )
    group_name_prefix = 'matchQueue'
    mm_decision: MatchMakingDecision | None = None
    mm_queue: MatchMakingQueue | None = None

    async def connect(self):
        method_to_call = await self.general_connect()
        if method_to_call == self.close:
            return await self.close()
        
        self.game: Game = await async_filter_first(Game, id=int(self.scope['url_route']['kwargs']['game_id']))

        if self.game is None:
            return await self.close()
        
        await method_to_call()
        can_play = await self.check_if_banned()
        await self.game_settings(
            {'type': 'game_settings'} | model_to_dict(self.game, fields=['strict_num_of_players', 'min_players', 'max_players', 'name'])
        )

    async def receive_json(self, data_json: dict, **kwargs):
        method_to_call = await super().receive_json(data_json, **kwargs)
        if method_to_call is None:
            return
        
        await method_to_call(data_json)

    async def check_if_banned(self):
        can_user_play = await self.check_permissions(self.user)

        if can_user_play:
            return True
        
        ban: UserBan | None = await self.get_last_ban(self.user)
        if ban is not None:
            await self.player_got_banned(
                {
                    'type': 'player_got_banned',
                    'ban_ends_at': ban.ban_ends_at.strftime('%Y-%m-%d %H:%M:%S') if ban.ban_ends_at else None
                }
            )
        else:
            await self.unable_to_play_mm(
                {
                    'type': 'unable_to_play_mm',
                    'reason': "You don't have steam linked to your profile"
                }
            )

        return False

    @database_sync_to_async
    def check_permissions(self, user: User):
        return user.has_perm('authentication.play_mm') and user.has_perm(f'authentication.play_mm_{self.game.name}')

    @database_sync_to_async
    def get_last_ban(self, user):
        return UserBan.objects.filter(Q(game=self.game) | Q(game=None),user=user,is_active=True).last()

    async def disconnect(self, code):
        await super().discard_group()
        await self.make_user_inactive()

    async def make_user_inactive(self):
        if self.user is not None:
            await async_filter_update(UserQueue, filters=dict(user=self.user.pk), updates=dict(is_active=False))
    
    async def enqueued(self, data_json: dict):
        can_play = await self.check_if_banned()

        if not can_play:
            return
        
        self.mm_queue = MatchMakingQueue(
            data_json=data_json,
            user=self.user
        )
        try:
            await self.mm_queue.validate_data()
        except ValidationError as error:
            await self.send_status_info(
                message=error.message,error=True
            )
            return
        
        await self.mm_queue.enqueue()

        await self.player_in_queue({
            "type": "player_in_queue"
        })

    async def accept_match(self, data_json: dict):
        self.mm_decision = MatchMakingDecision(data_json, self.user, True)
        await self.make_decision(self.mm_decision)

    async def make_decision(self, mm_decision_instance: MatchMakingDecision):
        try:
            await mm_decision_instance.validate_data()
        except ValidationError as error:
            await self.send_status_info(error.message, error=True)
            return
        
        try:
            await mm_decision_instance.make_decision()
        except ValidationError as error:
            await self.send_status_info(error.message, error=True)
            return
        
        if mm_decision_instance.to_accept:
            await self.match_accepted({
                "type": "match_accepted"
            })
        else:
            await self.match_declined({
                "type": "match_declined"
            })

    async def decline_match(self, data_json: dict):
        self.mm_decision = MatchMakingDecision(data_json, self.user, False)
        await self.make_decision(self.mm_decision)

    async def match_found(self, event):
        await self.send_json(event)

    async def match_created(self, event):
        await self.send_json(event)
        await self.close()

    async def player_got_banned(self, event):
        await self.send_json(event)

    async def match_canceled_by_user(self, event):
        await self.send_json(event)

    async def match_canceled_by_time(self, event):
        await self.send_json(event)

    async def match_accepted(self,event):
        await self.send_json(event)

    async def count_of_accepted(self, event):
        await self.send_json(event)

    async def match_declined(self,event):
        await self.send_json(event)

    async def player_in_queue(self, event):
        await self.send_json(event)

    async def unable_to_play_mm(self, event):
        await self.send_json(event)

    async def game_settings(self, event):
        await self.send_json(event)

class MatchConsumer(ExtendedAsyncConsumer):
    async def connect(self):
        pass

    async def disconnect(self, code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        pass

    async def game_status_changed(self, event):
        pass
