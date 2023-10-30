from django.core.cache import cache
import hashlib
from functools import wraps
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from .tools import CachedResponse

def cache_response(timeout: int | None = 3600, start_name: str | None = None, for_all: bool = False):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request: HttpResponse, *args, **kwargs):
            if not for_all:
                cache_key = f"{start_name}_cache_{request.path}_{hashlib.sha256(request.user.username.encode('utf-8')).hexdigest()}"
            else:
                cache_key = f"{start_name}_cache_{request.path}"
            cachedData: CachedResponse = cache.get(cache_key)

            if cachedData:
                return Response(cachedData.data,status=cachedData.code)

            response: CachedResponse = view_func(request, *args, **kwargs)
            if status.is_success(response.code):
                cache.set(cache_key, response, timeout)
            return Response(response.data,status=response.code)
        return _wrapped_view
    return decorator