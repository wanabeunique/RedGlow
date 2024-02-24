from channels.db import database_sync_to_async
from django.db.models import OuterRef, Subquery
from django.db.models.manager import BaseManager
from apps.matchmaking.models import Game, Match, UserMatch, UserQueue, UserElo
from apps.tools.db_tools import async_filter_select_related_first, async_filter_first
from django.conf import settings
from .mm_parent import MatchMakingParent
from apps.tools.exceptions import ValidationError

class MatchMakingQueue(MatchMakingParent):
    target_players_match_queues: dict[int | None, dict[str, list[UserQueue | int]]] = None
    match_queues: BaseManager[UserQueue] | None = None
    queued_user: UserQueue | None = None
    game: Game | None = None

    async def validate_data(self):
        game: Game = await async_filter_first(Game,name=self.data_json.get('game', ''))

        if game is None:
            raise ValidationError(
                'Game not found'
            )
        if self.data_json.get('target_players') is not None:
            if self.data_json.get('target_players') < game.min_players or self.data_json.get('target_players') > game.max_players:
                raise ValidationError(
                    'Invalid target_players'
                )

        self.data_json['game'] = game

        # Проверка, есть ли запись юзера в бд
        queued_user: UserQueue | None = await async_filter_select_related_first(UserQueue, select_related=['user'], user=self.user.pk)
        # Есть - обновляем
        if queued_user:
            if queued_user.is_active:
                raise ValidationError(
                    "You're already in the queue"
                )
            
            if queued_user.match_found:
                raise ValidationError(
                    "You're already in the game"
                )
            
            self.data_json['is_active'] = True
            for key,value in self.data_json.items():
                setattr(queued_user, key, value)

            await database_sync_to_async(queued_user.save)()

        # Если нет, то создаем
        else:
            self.data_json['user'] = self.user
            queued_user: UserQueue = UserQueue(**self.data_json)
            await database_sync_to_async(queued_user.save)()

        self.match_queues = await self.__filter_users_by_game(game, queued_user.pk)
        self.queued_user = queued_user
        self.game = game
        self._is_valid = True

    async def enqueue(self):
        if not self._is_valid:
            raise ValidationError(
                'You should call validate_data first'
            )
        
        await self.__check_elo_filter()

    @database_sync_to_async
    def __filter_users_by_game(self, game, pk):
        return UserQueue.objects.filter(game=game, is_active=True).exclude(pk=pk).order_by('-queued_from')
    
    @database_sync_to_async
    def __filter_users_by_elo(self, elo_subquery, elo, **filters):
        self.match_queues = self.match_queues.filter(**filters).annotate(
            elo=Subquery(elo_subquery)
        ).filter(elo__gt=elo-250, elo__lt=elo+250)
    
    @database_sync_to_async
    def __get_none_elo_filter_players(self, elo_subquery,**filters):
        self.match_queues = self.match_queues.filter(**filters).annotate(
            elo=Subquery(elo_subquery)
        ).filter(elo_filter=False)

    async def __check_elo_filter(self):
        num_of_players_queued = await database_sync_to_async(self.match_queues.count)()

        if num_of_players_queued + 1 < self.game.min_players:
            return
        
        elo_subquery = UserElo.objects.filter(user=OuterRef('user'), game=self.game.pk).values('elo')
        user_elo: UserElo = await database_sync_to_async(UserElo.objects.get)(user=self.user.pk,game=self.game.pk)

        if self.queued_user.elo_filter:
            await self.__filter_users_by_elo(elo_subquery, user_elo.elo)
        else:
            await self.__get_none_elo_filter_players(elo_subquery)
        await self._log_info(self.match_queues, 'after_elo_got_filtered')
        await self.__filter_num_of_players()
    
    async def __get_users_by_target_players(self, target_players_needed: int | None = None):
        self.target_players_match_queues = {}

        def update_key(obj: UserQueue):
            if self.target_players_match_queues.get(obj.target_players, None) is None:
                self.target_players_match_queues[obj.target_players] = dict(instances=list(),ids=list())
                    
            self.target_players_match_queues[obj.target_players]['instances'].append(obj)
            self.target_players_match_queues[obj.target_players]['ids'].append(obj.pk)

        async for obj in self.match_queues:
            if target_players_needed is not None and (target_players_needed == obj.target_players or obj.target_players is None):
                update_key(obj)
            elif target_players_needed is None:
                update_key(obj)
                

    async def __search_for_none_target_players(self):
        for target_players, objects in self.target_players_match_queues.items():
            
            players_found = objects.get('instances')
            all_ids = objects.get('ids')

            if self.target_players_match_queues.get(None, None) is not None and target_players is not None:
                players_found.extend(self.target_players_match_queues.get(None).get('instances'))
                all_ids.extend(self.target_players_match_queues.get(None).get('ids'))

            await self._log_info(players_found,'players found')
            num_of_players_queued = len(players_found) + 1
            if not self.game.strict_num_of_players:
                if target_players is not None:
                    if num_of_players_queued >= target_players:
                        return (players_found, target_players, all_ids)

                elif num_of_players_queued >= self.game.min_players and num_of_players_queued <= self.game.max_players:
                    return (players_found, num_of_players_queued, all_ids)

            elif num_of_players_queued >= self.game.strict_num_of_players:
                return (players_found, self.game.strict_num_of_players, all_ids)
            
        return None, None, None
            
    async def __search_for_exact_target_players(self):
        players_found = list()
        all_ids = list()
        if self.target_players_match_queues.get(self.queued_user.target_players, None) is not None:
            players_found.extend(self.target_players_match_queues.get(self.queued_user.target_players).get('instances'))
            all_ids.extend(self.target_players_match_queues.get(self.queued_user.target_players).get('ids'))

        if self.target_players_match_queues.get(None, None) is not None:
            players_found.extend(self.target_players_match_queues.get(None).get('instances'))
            all_ids.extend(self.target_players_match_queues.get(None).get('ids'))
        
        num_of_players_queued = len(players_found) + 1
         
        if not self.game.strict_num_of_players:
            if num_of_players_queued >= self.queued_user.target_players and num_of_players_queued >= self.game.min_players:
                return (players_found, self.queued_user.target_players, all_ids)
            
        elif num_of_players_queued >= self.game.strict_num_of_players:
            return (players_found, self.game.strict_num_of_players, all_ids)
        
        return None, None, None
            

    async def __filter_num_of_players(self):
        num_of_players_queued = await database_sync_to_async(self.match_queues.count)()
        
        if num_of_players_queued + 1 < self.game.min_players:
            return
        
        await self.__get_users_by_target_players(self.queued_user.target_players)
        if not self.queued_user.target_players:
            players_found, num_of_players, ids = await self.__search_for_none_target_players()
        else:
            players_found, num_of_players, ids = await self.__search_for_exact_target_players()

        if players_found is None:
            return
        
        ids.append(self.queued_user.pk)
        await self.__create_match(players_found, num_of_players, ids)

    async def __create_match(self, match_queues: list[UserQueue], num_of_players: int, all_ids: list[int]):
        match_instance: Match = await database_sync_to_async(Match.objects.create)(game=self.game)
        user_match_objects = [UserMatch(user=self.user, match=match_instance)]
        users_to_send = [self.user.username]
        count_of_added_players = 1
        for match_queue in match_queues:
            if count_of_added_players >= num_of_players:
                break

            user_match_objects.append(
                UserMatch(user=match_queue.user, match=match_instance)
            )
            users_to_send.append(match_queue.user.username)
            count_of_added_players += 1

        await database_sync_to_async(UserMatch.objects.bulk_create)(user_match_objects)
        await self.update_match_queues_when_found(all_ids)

        await self.__send_ready_messages(users_to_send, match_instance.hash)

    @database_sync_to_async
    def update_match_queues_when_found(self, all_ids: list[int]):
        UserQueue.objects.filter(id__in=all_ids).update(is_active=False,match_found=True)

    async def __send_ready_messages(self, users: list[str], match_hash):
        time_to_accept = settings.TIME_TO_ACCEPT_A_GAME
        await self._send_messages_to_ws(
            users,
            {
                'type': 'match_found',
                'count_of_players': len(users),
                'hash': match_hash,
                'time_to_accept': time_to_accept
            } 
        )