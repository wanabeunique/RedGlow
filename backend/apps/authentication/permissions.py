from rest_framework.permissions import BasePermission
from steam.webapi import WebAPI
from decouple import config
from .models import User

class NotAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return bool(not request.user.is_authenticated)
    
class HasSteam(BasePermission):
    def has_permission(self, request, view):
        return bool(User.objects.get(username=request.user.username).steamId)
    
class HasCivilizationV(BasePermission):
    def has_permission(self, request, view):
        steamId = User.objects.get(username=request.user.username).steamId
        steamApi = WebAPI(key=config('STEAM_KEY'),https=True)
        for game in steamApi.IPlayerService.GetOwnedGames(steamid=steamId,include_appinfo=False,include_played_free_games=False,
            include_free_sub=True,include_extended_appinfo=True,appids_filter=0,language='ru',skip_unvetted_apps=True).get('response').get('games'):
            if game.get('name') == "Sid Meier’s Civilization V":
                return True
        return False
        
    
class HasCivilizationVI(BasePermission):
    def has_permission(self, request, view):
        steamId = request.user.steamId
        steamApi = WebAPI(key=config('STEAM_KEY'),https=True)
        for game in steamApi.IPlayerService.GetOwnedGames(steamid=steamId,include_appinfo=False,include_played_free_games=False,
            include_free_sub=True,include_extended_appinfo=True,appids_filter=0,language='ru',skip_unvetted_apps=True).get('response').get('games'):
            if game.get('name') == "Sid Meier’s Civilization VI":
                return True
        return False
    
class HasSub(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.subExpiresIn)