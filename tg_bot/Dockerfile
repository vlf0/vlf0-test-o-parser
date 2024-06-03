FROM python:3.9-alpine

# Making container logs displayable
ENV PYTHONUNBUFFERED 1

# Do not attempt to create .pyc files
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR usr/src/tg_bot

COPY . .

RUN pip3 install supervisor aiogram hiredis aioredis fastapi

COPY supervisord.conf /etc/supervisord.conf

ENTRYPOINT ["supervisord", "-c", "/etc/supervisord.conf"]