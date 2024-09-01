import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from config_reader import config
from filtres.role_filter import RoleFilter
from handlers.admin import admin_router
from handlers.client import client_router
from handlers.common import common_router


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    bot = Bot(config.bot_token.get_secret_value())
    dp = Dispatcher(storage=MemoryStorage())

    dp.startup.register(set_main_menu)

    dp.include_router(common_router)
    dp.include_router(client_router)
    dp.include_router(admin_router)

    client_router.message.filter(RoleFilter(role='Client'))
    admin_router.message.filter(RoleFilter(role='Administrator'))

    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot, skip_updates=False)


async def set_main_menu(bot: Bot):
    # Создаем список с командами и их описанием для кнопки menu
    main_menu_commands = [
        BotCommand(command='/start',
                   description='Перезапуск бота'),
        BotCommand(command='/support',
                   description='Поддержка')
    ]

    await bot.set_my_commands(main_menu_commands)


if __name__ == '__main__':
    asyncio.run(main())
