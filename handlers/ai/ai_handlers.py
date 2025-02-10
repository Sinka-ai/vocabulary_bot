from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Text
from data.create_empty import create_empty_user
from data.user_session import user_data
from lexicon.lexicon_ru import LEXICON_RU
import psycopg2
import os

router = Router()

@router.callback_query(Text(text=['start_ai']))
async def start_ai_dialog(callback: CallbackQuery):
    await callback.message.answer("Функция AI-чата удалена из текущей версии проекта.")
    await callback.answer()

@router.message(F.text, ~Text(startswith='/'))
async def process_message(message: Message):
    await message.answer("На данный момент диалоговый режим с AI недоступен.")