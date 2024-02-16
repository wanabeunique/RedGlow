from channels.db import database_sync_to_async
from django.db.models import Q, OuterRef, Subquery
from django.db.models.manager import BaseManager
from django.utils import timezone
from apps.matchmaking.models import UserMatch, UserElo, UserQueue, Game, Match
from apps.authentication.models import User
from apps.tools.db_tools import (
    async_filter_first,
    async_filter_count,
    async_filter_select_related
)
from apps.tools.exceptions import ValidationError
from .mm_parent import MatchMakingParent

class MatchMakingDecision(MatchMakingParent):

    def __init__(self, data_json: dict, user: User, to_accept: bool):
        self.to_accept = to_accept
        super().__init__(data_json=data_json, user=user)


    async def make_decision(self):
        if not self._is_valid:
            raise ValidationError(
                'You should call validate_data first'
            )
        
        self.user_match_instance.is_accepted = self.to_accept

        await database_sync_to_async(self.user_match_instance.save)()

        if self.to_accept:
            await self.__accept()
        else:
            await self.__decline()

    async def validate_data(self):
        self.match_instance: Match = await self.__get_match(self.data_json.get('hash'))
        
        if self.match_instance is None:
            raise ValidationError(
                "Invalid data"
            )
        
        if self.match_instance.status != Match.Status.CREATED:
            raise ValidationError(
                "Invalid data"
            )

        if self.match_instance.date_to_confirm < timezone.now():
            raise ValidationError(
                'Time to accept match is over'
            )

        self.user_match_instance: UserMatch | None = await async_filter_first(UserMatch, match=self.match_instance, user=self.user)

        if self.user_match_instance is None:
            raise ValidationError(
                "You can't perfome this action"
            )

        if self.user_match_instance.is_accepted is not None:
            raise ValidationError(
                "You can't perfome this action"
            )
        
        self._is_valid = True

    @database_sync_to_async
    def __get_match(self, hash):
        return Match.objects.filter(hash=hash).select_related('game').first()

    async def __accept(self):
        await self.__check_if_all_accepted()

    @database_sync_to_async
    def __get_user_match_instances_and_elo(self):
        elo_subq = UserElo.objects.filter(user=OuterRef('user'), game=self.match.game).values('elo')[:1]
        return UserMatch.objects.filter(match=self.match).annotate(elo=Subquery(elo_subq)).select_related('user')

    async def __check_if_all_accepted(self):
        user_match_instances: BaseManager[UserMatch] = await self.__get_user_match_instances_and_elo()
        count_not_accepted = await async_filter_count(UserMatch, Q(is_accepted=False) | Q(is_accepted=None), base_manager=user_match_instances)
        
        if count_not_accepted != 0:
            return
        
        self.match_instance.status = Match.Status.PREPARING
        await database_sync_to_async(self.match_instance.save)()
        await self.__send_match_created_messages(user_match_instances)


    async def __send_match_created_messages(self, to_send: BaseManager[UserMatch]):
        players_info = []
        async for user_match in to_send:
            players_info.append(
                {
                    "username": user_match.user.username,
                    "photo": user_match.user.photo_url,
                    "elo": user_match.elo,
                    "date_joined": user_match.user.date_joined.strftime("%Y-%m-%d")
                }
            )

        async for user_match in to_send:
            await self.channel_layer.group_send(
                f'matchQueue_{user_match.user.username}',
                {
                    'type': 'match_created',
                    'hash': self.match_instance.hash,
                    "players": players_info
                }
            )

    async def __decline(self):
        user_match_instances = await self.__cancel_match()
        await self.__send_match_cancel_messages(user_match_instances)

    async def __cancel_match(self):
        user_match_instances: BaseManager[UserMatch] = await async_filter_select_related(UserMatch, ['user'], match=self.match_instance)
        self.match_instance.status = self.match_instance.Status.CANCELED
        await database_sync_to_async(self.match_instance.save)()
        return user_match_instances
        
    async def __send_match_cancel_messages(self, to_send: BaseManager[UserMatch]):
        async for user_match in to_send:
            await self.channel_layer.group_send(
                f'matchQueue_{user_match.user.username}',
                {
                    'type': 'match_canceled_by_user',
                    'hash': self.match_instance.hash
                }
            )