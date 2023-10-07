import redis

def connectToRedis():
    return redis.StrictRedis(host='redis', port=6379, db=1, socket_timeout=None, connection_pool=None, charset='utf-8', errors='strict', unix_socket_path=None)
