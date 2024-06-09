#!/bin/bash

# Start MySQL in the background
echo "Starting MySQL server..."
/usr/local/bin/docker-entrypoint.sh mysqld &

wait_for_mysql() {
    until mysql -h database -P 3306 -u root -p$MYSQL_ROOT_PASSWORD -e "SELECT 1;" > /dev/null 2>&1; do
        echo "Waiting for MySQL server to become available..."
        sleep 5
    done
    echo "MySQL server is now available."
}

wait_for_mysql

echo "Running custom initialization script..."
/var/lib/mysqldb/init.sh

wait

echo "MySQL custom initialization complete. Server is ready."