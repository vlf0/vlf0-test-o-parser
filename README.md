<div align="center">

# Ozon parser

This project is an [ozon marketplace](https://ozon.ru) parser writing on Python
which allows get data of products that were parsed and save them to DB. Also allows get 
last parsing result via telegram bot by command at any time (when the project is running).

___

#### How it works:

</div>

The core is django app which have a few API endpoints to calling parser and getting results.
First you need call bot _notifications_ command. The bot will add your telegram ID to redis storage and as a result
the bot will be able to send you notifications.
Then sending POST request to [run parser API](http://localhost:8000/api/v1/run_parsing) with a such body 
(number can be any from 0 to 50): 
```JSON
{"count": 25}
```
If not passed value will be set automatically to 10 by default. 
When parser is called the app is executing parsing of marketplace using **playwrite** lib and then saving to DB.
After successful parsing solving send request to telegram bot API based on FastAPI framework and the bot sends 
notification to users ids which were saved via bot before. Now parsed data is available, and we can get them
via GET request. It will return whole list of products in JSON format:
```JSON
"output": [
    {
      "name": "string",
      "price": "number",
      "description": "string",
      "image_url": "string",
      "discount": "string | null"
    }   
  ]
}
```
[get list products API](http://localhost:8000/api/v1/parsed_data) - return all products.
[get single product API](http://localhost:8000/api/v1/parsed_data) - return one product by id.
_API endpoints also have been described via Swagger - [Swagger](http://localhost:8000/swagger/)._
___
## Stack:
#### - MySQL 8.4
#### - Redis 7.4.2
#### - Django 3.2.25
#### - DRF 3.15.1
#### - FastAPI 0.111.0
#### - aiogram 3.6.0 
#### - Celery 5.4.0
___

<div align="center">

## How to run it:

</div>

:exclamation: __You need have installed _Git, Docker and Docker-Compose_ on machine where will run the project.
If you don't have - please install it first. :exclamation: Docker should be running.__

1. Clone the project into needed directory:

    `git clone https://github.com/vlf0/vlf0-test-o-parser.git`
2. Create file named `.env` in each directory where is `example.env` and fill them yourself data.
3. Go to project root and run command:
    `docker-compose up`

___

Screencast from Django admin panel placed in the project root named _"parser_admin_panel"_. 
You can also [see video on YouTube (0:19)](https://youtu.be/qmhtJGehcZw) 
