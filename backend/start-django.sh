/usr/local/bin/wait-for-it.sh db:5432 -t 20 --
/usr/local/bin/wait-for-it.sh redis:6379 -t 5 --
/usr/local/bin/wait-for-it.sh rabbitmq:5672 -t 20 --
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py createsuperuser --noinput
python general_tools/deploy_tools/setup_db.py
python general_tools/test_tools/setup_test_db.py
gunicorn gamingPlatform.asgi -k gamingPlatform.uvicorn_worker.CustomUvicornWorker -c gunicorn_config.py --reload --access-logfile -