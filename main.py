from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import KeyboardButton
from keyboard import admin_kb, user_a_kb, user_kb
from create_bot import dp, bot
from database import db
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from handlers import admin



admin.register_handlers_admin(dp)

async def on_startup(_):
    await db.create_table()
    users = await db.get_users()
    for user in users:
        try:
            await bot.send_message(user, f"Bot is online now, please send /start to start working with bot", reply_markup = ReplyKeyboardMarkup().add(KeyboardButton('/start')))
        except Exception:
            pass


if __name__ == "__main__":
    executor.start_polling(dispatcher = dp, skip_updates = True, on_startup = on_startup)

