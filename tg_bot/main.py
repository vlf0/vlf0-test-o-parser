import sys
import asyncio
import logging
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


@dp.message(filters.CommandStart())
async def update_ids(message: types.Message) -> None:
    b_data = await redis.get('ids')
    if b_data is not None:
        ids_list = b_data.decode('UTF-8').split(' ')
        if str(message.from_user.id) not in ids_list:
            await redis.append('ids', f' {message.from_user.id}')
            await message.answer('your id added.', parse_mode='')
            return
        await message.answer('your id already exist.', parse_mode='')
        return
    await redis.set('ids', message.from_user.id)
    await message.answer('your id added.', parse_mode='')


@dp.message(filters.Command('get'))
async def get_last_parsing_data(message: types.Message) -> None:
    await message.answer('GET command')


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

