from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.views import APIView
from .serializers import UserProfileSerializer, UserPhotoSerializer, UserSteamSerializer, UserBackgroundSerializer, UserForeignSerializer, UserBehaviorSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from apps.authentication.models import User
from steam.webapi import WebAPI
from decouple import config
from apps.tools.permissions import HasSteam, DoesntHaveSteam
from apps.tools.caching import delete_cache, cache_response, CachedResponse, change_cached_data
from django.utils.decorators import method_decorator


def invalidate_cache(name, response, username):
    change_cached_data(
        name,
        response.data.get(name),
        f'user_{name}',
        f'user/{username}/{name}',
        for_all=True
    )
    change_cached_data(
        name,
        response.data.get(name),
        'foreign_user_profile',
        f'user/{username}/info',
        for_all=True
    )
    change_cached_data(
        name,
        response.data.get(name),
        'current_user_profile',
        'user/info',
        username
    )


@method_decorator(cache_response(start_name='current_user_profile'), name='get')
class RetrieveUserProfileView(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CachedResponse(serializer.data)


@method_decorator(cache_response(start_name='foreign_user_profile', for_all=True), name='get')
class RetirieveForeignUserProfileView(RetrieveAPIView):
    serializer_class = UserForeignSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'username'
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CachedResponse(serializer.data)


class RetrieveUserBehaviorView(RetrieveAPIView):
    serializer_class = UserBehaviorSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self, queryset=None):
        return self.request.user


@method_decorator(cache_response(start_name='user_photo', for_all=True), name='get')
class RetrieveUserPhotoView(RetrieveAPIView):
    serializer_class = UserPhotoSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'username'
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CachedResponse(serializer.data)


class UpdateUserPhotoView(UpdateAPIView):
    serializer_class = UserPhotoSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        self.instance = self.request.user
        return self.instance

    def put(self, request, *args, **kwargs):
        response: Response = self.update(request, *args, **kwargs)
        if status.is_success(response.status_code):
            invalidate_cache('photo', response, self.instance.username)
        return response


class UpdateUserBackgroundView(UpdateAPIView):
    serializer_class = UserBackgroundSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        self.instance = self.request.user
        return self.instance

    def put(self, request, *args, **kwargs):
        response: Response = self.update(request, *args, **kwargs)
        if status.is_success(response.status_code):
            self.invalidate_cache(response, self.instance.username)
        return response


@method_decorator(cache_response(start_name='user_background', for_all=True), name='get')
class RetrieveUserBackgroundView(RetrieveAPIView):
    serializer_class = UserBackgroundSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'username'
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CachedResponse(serializer.data)


class UpdateSteamIdView(UpdateAPIView):
    serializer_class = UserSteamSerializer
    permission_classes = (IsAuthenticated, DoesntHaveSteam)

    def get_object(self, queryset=None):
        self.instance = self.request.user
        return self.instance

    def put(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)
        if status.is_success(response.status_code):
            change_cached_data(
                'steamIdExists', True, 'current_user_profile', 'user/info', self.instance.username)
        return response


class RetrieveUserSteamNameView(APIView):
    permission_classes = (IsAuthenticated, HasSteam)

    def get(self, request, username=None):
        try:
            steamId = User.objects.get(username=username).steamId
            steamApi = WebAPI(key=config('STEAM_KEY'), https=True)
            steamName = steamApi.ISteamUser.GetPlayerSummaries(steamids=steamId).get(
                'response').get('players')[0].get('personaname')
            return Response(data={'steamName': steamName}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(data={'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
