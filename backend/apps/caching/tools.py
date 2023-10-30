import hashlib
from django.core.cache import cache
from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework import status

def get_cache_key(start_name, path, username=None, for_all=False):
    if for_all:
        cache_key = f"{start_name}_cache_{path}"
    else:
        cache_key = f"{start_name}_cache_{path}_{hashlib.sha256(username.encode('utf-8')).hexdigest()}"

    return cache_key

def delete_cache(start_name, path, username=None, for_all=False):
    cache.delete(get_cache_key(start_name, path, username, for_all))

def updateElementFromCache(request, start_name, path, newValue, key, oldValue=None, for_all=False, timeout=300):
    cache_key = get_cache_key(start_name, path, request,for_all)
    value: list | dict = cache.get(cache_key)
    if type(value) is list:
        for item in range(len(value)):
            if value[item][key] == oldValue:
                value[item][key] = newValue
                break
    value[key] = newValue
    cache.set(cache_key, value, timeout)

def addElementToCache(request, start_name, path, value, key, for_all=False, timeout=300):
    cache_key = get_cache_key(start_name, path, request,for_all)
    value: list = cache.get(cache_key)
    if type(value) is not list:
        return
    value.append({key:value})
    cache.set(cache_key, value, timeout)

def deleteElementFromCache(request, start_name, path, key, value, for_all=False, timeout=300):
    cache_key = get_cache_key(start_name, path, request,for_all)
    value: list = cache.get(cache_key)
    if type(value) is not list:
        return
    for item in range(len(value)):
        if value[item][key] == value:
            del value[item]
            break
    cache.set(cache_key, value, timeout)



def checkForCache(cache_key: str):
    cachedData = cache.get(cache_key)

    if cachedData:
        return Response(cachedData,status=status.HTTP_200_OK)

def setCache(
    cache_key: str,
    value,
    timeout: int | None = 300
):
    cache.set(cache_key, value, timeout)


class CachedResponse:
    def __init__(self, data, code=None):
        if not code:
            code = status.HTTP_200_OK
        self.data = data
        self.code = code