CREATE_TABLES_FILE='deployments/db/create_tables.sql'
AUTH_STUFF_FILE='deployments/db/auth_stuff.sql'
TRIGGERS_FILE='deployments/db/triggers.sql'

psql -h localhost -p 5432 -d redglow -U postgres -W -f $CREATE_TABLES_FILE
psql -h localhost -p 5432 -d redglow -U postgres -W -f $AUTH_STUFF_FILE
echo "База данных успешно заполнена."