import hashlib
from django.core.cache import cache
from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework import status
from functools import wraps
from django.conf import settings


class CachedResponse:
    def __init__(self, data, code=None):
        if not code:
            code = status.HTTP_200_OK
        self.data: dict = data
        self.code = code


def cache_response(timeout: int | None = None, start_name: str | None = None, for_all: bool = False):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request: HttpRequest, *args, **kwargs):

            if not for_all:
                cache_key = f"{start_name}_cache_{request.path}_{hashlib.sha256(request.user.username.encode('utf-8')).hexdigest()}"
            else:
                cache_key = f"{start_name}_cache_{request.path}"
            cachedData: CachedResponse | None = cache.get(cache_key)

            if cachedData is not None:
                return Response(cachedData.data, status=cachedData.code)

            response: CachedResponse = view_func(request, *args, **kwargs)

            if status.is_success(response.code):
                cache.set(cache_key, response, timeout if timeout else settings.CACHE_TIMEOUT_CUSTOM)
            return Response(response.data, status=response.code)
        return _wrapped_view
    return decorator


def get_cache_key(start_name, path, username=None, for_all=False):
    if for_all:
        cache_key = f"{start_name}_cache_{path}"
    else:
        cache_key = f"{start_name}_cache_{path}_{hashlib.sha256(username.encode('utf-8')).hexdigest()}"

    return cache_key


def delete_cache(start_name, path, username=None, for_all=False):
    cache.delete(get_cache_key(start_name, path, username, for_all))


def change_cached_data(key_to_change, value_to_change, start_name, path, username=None, for_all=False):
    key = get_cache_key(start_name, path, username, for_all)
    cached_resp: CachedResponse = cache.get(key)

    if cached_resp is None:
        return

    cached_resp.data[key_to_change] = value_to_change
    cache.set(key, cached_resp, timeout=settings.CACHE_TIMEOUT_CUSTOM)
