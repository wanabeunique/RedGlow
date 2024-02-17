from .models import UserElo, UserQueue, UserMatch, Game, Match
from apps.tools.db_tools import (
    async_filter_delete,
    async_filter_update,
    async_filter_exists,
    async_filter_values,
    async_filter_first,
    async_filter_count,
    async_filter_select_related
)
from .matchmaking_helpers.mm_queue import MatchMakingQueue
from .matchmaking_helpers.mm_decision import MatchMakingDecision
from apps.tools.exceptions import ValidationError
from apps.tools.extended_consumer import ExtendedAsyncConsumer

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
    """
    acceptable_keys = dict(
        enqueued={'target_players': int | None, 'game': str, 'elo_filter': bool},
        accept_match={'hash': str},
        decline_match={'hash': str},
    )
    group_name_prefix = 'matchQueue'

    async def disconnect(self, code):
        if hasattr(self, 'group_name'):
            if self.user is not None:
                await async_filter_update(UserQueue, filters=dict(user=self.user.pk), updates=dict(is_active=False))
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
    
    async def enqueued(self, data_json: dict):
    
        matchmaking_queue = MatchMakingQueue(
            data_json=data_json,
            user=self.user
        )
        try:
            await matchmaking_queue.validate_data()
        except ValidationError as error:
            await self.send_status_info(
                message=error.message,error=True
            )
            return
        
        await matchmaking_queue.enqueue()

        await self.player_in_queue({
            "type": "player_in_queue"
        })

    async def accept_match(self, data_json: dict):
        mm_decision = MatchMakingDecision(data_json, self.user, True)
        await self.make_decision(mm_decision)

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
        mm_decision = MatchMakingDecision(data_json, self.user, False)
        await self.make_decision(mm_decision)

    async def match_found(self, event):
        await self.send_json(event)

    async def match_created(self, event):
        await self.send_json(event)
        await self.close()

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
