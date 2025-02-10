import os
from aiogram import Bot
from aiogram import Dispatcher

bot: Bot = Bot(token=os.environ['TOKEN_VOCAB'], parse_mode='HTML')
dp: Dispatcher = Dispatcher()
