FROM mysql:8.4

WORKDIR /var/lib/mysqldb

COPY ./config/my.cnf /etc/mysql/my.cnf

RUN chmod 644 /etc/mysql/my.cnf

COPY init.sh .

COPY entrypoint.sh .

RUN chmod 777 /var/lib/mysqldb/

ENTRYPOINT ["sh", "/var/lib/mysqldb/entrypoint.sh"]