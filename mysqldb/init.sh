#!/bin/bash

echo "Start Parsing DB initialization..."

DB_HOST=$(grep "^DB_HOST=" .env | cut -d'=' -f2- | tr -d '\r')
DB_PORT=$(grep "^DB_PORT=" .env | cut -d'=' -f2- | tr -d '\r')
DB_NAME=$(grep "^DB_NAME=" .env | cut -d'=' -f2- | tr -d '\r')
DB_USER=$(grep "^DB_USER=" .env | cut -d'=' -f2- | tr -d '\r')
DB_USER_PASSWORD=$(grep "^DB_USER_PASSWORD=" .env | cut -d'=' -f2- | tr -d '\r')

cat <<EOF > /var/lib/mysqldb/init.sql

CREATE DATABASE IF NOT EXISTS ${DB_NAME};

ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY '${MYSQL_ROOT_PASSWORD}';

FLUSH PRIVILEGES;

USE ${DB_NAME};

CREATE USER '${DB_USER}'@'%' IDENTIFIED BY '${DB_USER_PASSWORD}';

ALTER USER '${DB_USER}'@'%' IDENTIFIED WITH mysql_native_password BY '${DB_USER_PASSWORD}';

GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'%';

FLUSH PRIVILEGES;
EOF

mysql -h $DB_HOST -P $DB_PORT -u root -p$MYSQL_ROOT_PASSWORD < init.sql

echo "Parsing DB initialize success"

rm /var/lib/mysqldb/init.sql