import sys
import asyncio
import logging
from dotenv import dotenv_values
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher, types, filters

config = dotenv_values()

TOKEN = config.get('TOKEN')

dp = Dispatcher()


class UsersManager:

    def __init__(self):
        self.ids: list = []

    def add_new_id(self, new_id: int):
        if new_id not in self.ids:
            self.ids.append(new_id)


user_manager = UsersManager()


@dp.message(filters.CommandStart())
async def update_ids(message: types.Message) -> None:
    user_manager.add_new_id(message.chat.id)
    await message.answer(f'{user_manager.ids}', parse_mode='')


async def send_notification(bot: Bot, product_amount):
    for user_id in user_manager.ids:
        await bot.send_message(user_id, f'Задача на парсинг товаров с сайта Ozon завершена.'
                                        f' Сохранено: {product_amount} товаров.')


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
