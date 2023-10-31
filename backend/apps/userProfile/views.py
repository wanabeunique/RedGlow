from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.views import APIView
from .serializers import UserProfileSerializer, UserPhotoSerializer, UserSteamSerializer, UserBackgroundSerializer, UserForeignSerializer, UserBehaviorSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from apps.authentication.models import User
from steam.webapi import WebAPI
from decouple import config
from apps.authentication.permissions import HasSteam, DoesntHaveSteam
from apps.caching.decorator import cache_response
from apps.caching.tools import delete_cache, CachedResponse
from django.utils.decorators import method_decorator


#@method_decorator(cache_response(start_name='currentUserProfile'), name='get')
class RetrieveUserProfileView(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)
    def get_object(self, queryset=None):
        return self.request.user
    def get(self,request,*args,**kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

#@method_decorator(cache_response(start_name='foreignUserProfile',for_all=True), name='get')
class RetirieveForeignUserProfileView(RetrieveAPIView):
    serializer_class = UserForeignSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'username'
    queryset = User.objects.all()
    def get(self,request,*args,**kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class RetrieveUserBehaviorView(RetrieveAPIView):
    serializer_class = UserBehaviorSerializer
    permission_classes = (IsAuthenticated, )
    def get_object(self, queryset=None):
        return self.request.user


#@method_decorator(cache_response(start_name='userPhoto',for_all=True), name='get')
class RetrieveUserPhotoView(RetrieveAPIView):
    serializer_class = UserPhotoSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'username'
    queryset = User.objects.all()
    def get(self,request,*args,**kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class UpdateUserPhotoView(UpdateAPIView):
    serializer_class = UserPhotoSerializer
    permission_classes = (IsAuthenticated,)
    def get_object(self,queryset=None):
        return self.request.user
    def put(self, request, *args, **kwargs):
        # delete_cache(
        #     'userPhoto',
        #     f'user/{request.user.username}/photo',
        #     request.user.username,
        #     for_all=True
        # )
        return self.update(request, *args, **kwargs)
    
class UpdateUserBackgroundView(UpdateAPIView):
    serializer_class = UserBackgroundSerializer
    permission_classes = (IsAuthenticated,)
    def get_object(self,queryset=None):
        return self.request.user
    def put(self, request, *args, **kwargs):
        # delete_cache(
        #     'userBackground',
        #     f'user/{request.user.username}/background',
        #     request.user.username,
        #     for_all=True
        # )
        return self.update(request, *args, **kwargs)

#@method_decorator(cache_response(start_name='userBackground',for_all=True), name='get')
class RetrieveUserBackgroundView(RetrieveAPIView):
    serializer_class = UserBackgroundSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'username'
    queryset = User.objects.all()
    def get(self,request,*args,**kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class UpdateSteamIdView(UpdateAPIView):
    serializer_class = UserSteamSerializer
    permission_classes = (IsAuthenticated, DoesntHaveSteam)
    def get_object(self, queryset=None):  
        return self.request.user
    def put(self, request, *args, **kwargs):
        # delete_cache(
        #     'currentUserProfile',
        #     'user/info',
        #     request.user.username
        # )
        return self.update(request, *args, **kwargs)

class RetrieveUserSteamNameView(APIView):
    permission_classes = (IsAuthenticated, HasSteam)
    def get(self,request,username=None):
        try:
            steamId = User.objects.get(username=username).steamId
            steamApi = WebAPI(key=config('STEAM_KEY'),https=True)
            steamName = steamApi.ISteamUser.GetPlayerSummaries(steamids=steamId).get('response').get('players')[0].get('personaname')
            return Response(data={'steamName':steamName},status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(data={'detail':'Not found'},status=status.HTTP_404_NOT_FOUND)