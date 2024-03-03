/usr/local/bin/wait-for-it.sh localhost:5672 -t 30 --

celery -A gamingPlatform worker -l info --concurrency=10 &


until timeout 10s celery -A gamingPlatform inspect ping; do
    >&2 echo "Celery workers not available"
done
echo 'Starting flower'
celery -A gamingPlatform flower --port=5555 -P eventlet