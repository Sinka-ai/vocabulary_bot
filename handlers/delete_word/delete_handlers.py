import os

import data.create_tables as tables
import data.user_session as users
from aiogram.filters import Command, Text
import filters.filters as f
from data.create_empty import create_empty_user
from lexicon.lexicon_ru import LEXICON_RU
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from keyboard.buttons import keyboard_yes_no_delete

router = Router()


async def start_delete(message: Message, user_id: int):
    create_empty_user(user_id)
    users.user_data[user_id]['state'] = 'in_delete'
    await message.answer(LEXICON_RU['enter_en_word'])


@router.message(Command(commands=['delete']))
async def proccess_start_delete(message: Message):
    await start_delete(message, message.from_user.id)


@router.callback_query(Text(text=['to_delete']))
async def start_delete_button(callback: CallbackQuery):
    await callback.answer()
    await start_delete(callback.message, callback.from_user.id)


@router.message(F.text,~Text(startswith='/'), f.InDelete(users.user_data))
async def proccess_put_word_2delete(message: Message):
    db = tables.psycopg2.connect(dbname=os.environ['POSTGRES_DB'],
                                 user=os.environ['POSTGRES_USER'],
                                 password=os.environ['POSTGRES_PASSWORD'],
                                 host=os.environ['POSTGRES_CONTAINER_NAME'],  # Это имя контейнера с базой данных
                                 port="5432")
    sql = db.cursor()
    user_id = message.from_user.id
    sql.execute(f"SELECT * FROM words WHERE en='{message.text.lower()}' AND user_id={user_id}")
    if sql.fetchone() is None:
        await message.answer(LEXICON_RU['havent_found'])
    else:
        await message.answer(LEXICON_RU['you_sure'],
                        reply_markup = keyboard_yes_no_delete)
        users.user_data[user_id]['en'] = message.text.lower()
    sql.close()
    db.close()


@router.callback_query(Text(text=['yes_pressed_delete']))
async def proccess_delete_word(callback: CallbackQuery):
    user_id = callback.from_user.id
    db = tables.psycopg2.connect(dbname=os.environ['POSTGRES_DB'],
                                 user=os.environ['POSTGRES_USER'],
                                 password=os.environ['POSTGRES_PASSWORD'],
                                 host=os.environ['POSTGRES_CONTAINER_NAME'],  # Это имя контейнера с базой данных
                                 port="5432")
    sql = db.cursor()
    en = users.user_data[user_id]['en']
    sql.execute(f"DELETE FROM words WHERE en = '{en}' AND user_id = {user_id}")
    db.commit()
    sql.close()
    db.close()
    await callback.message.answer(str(LEXICON_RU['word'] + en + LEXICON_RU['deleted']+LEXICON_RU['back_2menu']))
    users.user_data[user_id]['state'] = 'in_menu'
    await callback.answer()


@router.callback_query(Text(text=['no_pressed_delete']))
async def proccess_exit(callback: CallbackQuery):
    user_id = callback.from_user.id
    await callback.message.answer(LEXICON_RU['stoped'])
    users.user_data[user_id]['state'] = 'in_menu'
    await callback.answer()