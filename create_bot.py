from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database import db

ADMIN_ID = 1030563973
bot = Bot(token = '5895569438:AAF-DE-HH5ePR8ens-kzBVAP4bziPA-DM2g')
dp = Dispatcher(bot, storage=MemoryStorage())

