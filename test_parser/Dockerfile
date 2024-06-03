FROM python:3.9-slim

# Making container logs displayable
ENV PYTHONUNBUFFERED 1

# Do not attempt to create .pyc files
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR usr/src/parser

COPY . .

RUN apt-get update \
    && apt install pkg-config -y \
    && apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config xvfb x11-utils -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install -r ./requirements.txt pyvirtualdisplay

RUN playwright install chromium

RUN playwright install-deps chromium

# Running the app
ENTRYPOINT ["sh", "/usr/src/parser/entrypoint.sh"]