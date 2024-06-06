import sys
import asyncio
import logging
import aiohttp
from dotenv import dotenv_values
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher, types, filters
import aioredis


config = dotenv_values()
redis_instance = config.get('REDIS_URL')
redis = aioredis.from_url(redis_instance)


TOKEN = config.get('TOKEN')
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2))
dp = Dispatcher()


@dp.message(filters.Command('notifications'))
async def update_ids(message: types.Message) -> None:
    b_data = await redis.get('ids')
    if b_data is not None:
        ids_list = b_data.decode('UTF-8').split(' ')
        if str(message.from_user.id) not in ids_list:
            await redis.append('ids', f' {message.from_user.id}')
            await message.answer('Your ID added. You will get notifications when task will executed.',
                                 parse_mode='')
            return
        await message.answer('Your ID already exist. You will get notifications when task will executed.',
                             parse_mode='')
        return
    await redis.set('ids', message.from_user.id)
    await message.answer('Your ID added. You will get notifications when task will executed.', parse_mode='')


@dp.message(filters.CommandStart())
async def get_last_parsing_data(message: types.Message) -> None:
    api_url = "http://parser:8000/api/v1/parsed_data/"
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            if response.status == 200:
                data = await response.json()
                products_list = data['output']
                counter = 0
                product_number = 1
                text_answer = ''
                for product in products_list:
                    processed_product = (f'№{product_number}\n\nНазвание: {product["name"]}\n\n'
                                         f'ссылка: {product["link"]}\n')
                    text_answer += processed_product
                    counter += 1
                    product_number += 1
                    if counter == 5:
                        await message.answer(f'Данные парсера:\n{text_answer}', parse_mode='')
                        counter = 0
                        text_answer = ''
                if text_answer:
                    await message.answer(f'\n{text_answer}', parse_mode='')
            else:
                await message.answer(f'Failed to get data from API. Status: {response.status}', parse_mode='')


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

