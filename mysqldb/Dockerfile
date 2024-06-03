FROM mysql:8.4

COPY ./config/my.cnf /etc/mysql/my.cnf

RUN chmod 644 /etc/mysql/my.cnf

COPY ./initdb.d/. /docker-entrypoint-initdb.d/.

WORKDIR /var/vib/mysqldb