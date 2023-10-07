/usr/local/bin/wait-for-it.sh localhost:8000 -t 10 --

# Запускаем Celery worker
celery -A gamingPlatform worker -l info &

# Ждем некоторое время (или выполните другие команды, если необходимо)

# Запускаем Flower
until timeout 10s celery -A gamingPlatform inspect ping; do
    >&2 echo "Celery workers not available"
done
echo 'Starting flower'
celery -A gamingPlatform flower --port=5555 -P eventlet