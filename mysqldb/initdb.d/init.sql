CREATE DATABASE IF NOT EXISTS parsing;

ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'root';

FLUSH PRIVILEGES;

USE parsing;

CREATE USER 'obs'@'%' IDENTIFIED BY 'obs';

ALTER USER 'obs'@'%' IDENTIFIED WITH mysql_native_password BY 'obs';

GRANT ALL PRIVILEGES ON parsing.* TO 'obs'@'%';

FLUSH PRIVILEGES;