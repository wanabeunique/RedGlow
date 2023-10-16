from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.views import APIView
from .serializers import UserProfileSerializer, UserPhotoSerializer, UserSteamSerializer, UserBackgroundSerializer, UserForeignSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from apps.authentication.models import User
from steam.webapi import WebAPI
from decouple import config

class RetrieveUserProfileView(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)
    def get_object(self, queryset=None):
        return self.request.user


class RetirieveForeignUserProfileView(RetrieveAPIView):
    serializer_class = UserForeignSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'username'
class RetrieveUserPhotoView(RetrieveAPIView):
    serializer_class = UserPhotoSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'username'
    queryset = User.objects.all()

class UpdateUserPhotoView(UpdateAPIView):
    serializer_class = UserPhotoSerializer
    permission_classes = (IsAuthenticated,)
    def get_object(self,queryset=None):
        return self.request.user

class UpdateUserBackgroundView(UpdateAPIView):
    serializer_class = UserBackgroundSerializer
    permission_classes = (IsAuthenticated,)
    def get_object(self,queryset=None):
        return self.request.user

class RetrieveUserBackgroundView(RetrieveAPIView):
    serializer_class = UserBackgroundSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'username'
    queryset = User.objects.all()

class UpdateSteamIdView(UpdateAPIView):
    serializer_class = UserSteamSerializer
    permission_classes = (IsAuthenticated, )
    def get_object(self, queryset=None):  
        return self.request.user

class RetrieveUserOwnsGameView(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self,request,username=None,game=None):
        try:
            steamId = User.objects.get(username=username).steamId
            steamApi = WebAPI(key=config('STEAM_KEY'),https=True)
            for game in steamApi.IPlayerService.GetOwnedGames(steamid=steamId,include_appinfo=False,include_played_free_games=False,
                include_free_sub=True,include_extended_appinfo=True,appids_filter=0,language='ru',skip_unvetted_apps=True).get('response').get('games'):
                if game.get('name') == game:
                    return Response(data={'doesOwn':True},status=status.HTTP_200_OK)
            return Response(data={'doesOwn':False},status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(data={'detail':'Not found'},status=status.HTTP_404_NOT_FOUND)
        
class RetrieveUserSteamNameView(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self,request,username=None):
        try:
            steamId = User.objects.get(username=username).steamId
            steamApi = WebAPI(key=config('STEAM_KEY'),https=True)
            steamName = steamApi.ISteamUser.GetPlayerSummaries(steamids=steamId).get('response').get('players')[0].get('personaname')
            return Response(data={'steamName':steamName},status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(data={'detail':'Not found'},status=status.HTTP_404_NOT_FOUND)