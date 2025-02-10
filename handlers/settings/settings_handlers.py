import os

import data.create_tables as tables
import data.user_session as users
from aiogram.filters import Text, Command
import filters.filters as f
from lexicon.lexicon_ru import LEXICON_RU
from aiogram.types import Message, CallbackQuery
from aiogram import Router
from keyboard.buttons import keyboard_yes_no_settings
from data.create_empty import create_empty_user


global MY_ID_TELEGRAM
MY_ID_TELEGRAM = os.environ['MY_TG_ID']
admin_ids = [MY_ID_TELEGRAM]
router = Router()



@router.message(Command(commands=['count']), f.InSettings(users.user_data))
async def proccess_change_incl_tag(message: Message):
    await message.answer(text = 'Какие по длине тесты ты хочешь проходить?')


@router.message(lambda message: message.text.isnumeric(), f.InSettings(users.user_data))
async def isnumeric(message: Message):
    new_count = int(message.text)
    user_id = message.from_user.id
    db = tables.psycopg2.connect(dbname=os.environ['POSTGRES_DB'],
                                 user=os.environ['POSTGRES_USER'],
                                 password=os.environ['POSTGRES_PASSWORD'],
                                 host=os.environ['POSTGRES_CONTAINER_NAME'],  # Это имя контейнера с базой данных
                                 port="5432")
    sql = db.cursor()
    sql.execute(f'UPDATE users SET set_test_words = {new_count} WHERE user_id = {user_id}')
    db.commit()
    sql.close()
    db.close()
    await message.answer(LEXICON_RU['new_count'] + str(new_count)+'\n'+ LEXICON_RU['back_2menu'])


@router.callback_query(Text(text=['yes_pressed_settings']), f.InSettings(users.user_data))
async def proccess_button_yes_press(callback: CallbackQuery):
    user_id = callback.from_user.id
    db = tables.psycopg2.connect(dbname=os.environ['POSTGRES_DB'],
                                 user=os.environ['POSTGRES_USER'],
                                 password=os.environ['POSTGRES_PASSWORD'],
                                 host=os.environ['POSTGRES_CONTAINER_NAME'],  # Это имя контейнера с базой данных
                                 port="5432")
    sql = db.cursor()
    users.user_data[user_id]['include_tag'] = 1
    sql.execute(f'UPDATE users SET include_tag = 1 WHERE user_id = {user_id}')
    db.commit()
    await callback.message.answer(LEXICON_RU['now_tag_included'])
    sql.close()
    db.close()
    users.user_data[user_id]['state'] = 'in_menu'
    await callback.message.answer(LEXICON_RU['back_2menu'])
    await callback.answer()


@router.callback_query(Text(text=['no_pressed_settings']), f.InSettings(users.user_data))
async def proccess_button_yes_press(callback: CallbackQuery):
    user_id = callback.from_user.id
    db = tables.psycopg2.connect(dbname=os.environ['POSTGRES_DB'],
                                 user=os.environ['POSTGRES_USER'],
                                 password=os.environ['POSTGRES_PASSWORD'],
                                 host=os.environ['POSTGRES_CONTAINER_NAME'],  # Это имя контейнера с базой данных
                                 port="5432")
    sql = db.cursor()
    users.user_data[user_id]['include_tag'] = 0
    sql.execute(f'UPDATE users SET include_tag = 0 WHERE user_id = {user_id}')
    db.commit()
    await callback.message.answer(LEXICON_RU['now_tag_disabled'])
    sql.close()
    db.close()
    users.user_data[user_id]['state'] = 'in_menu'
    await callback.message.answer(LEXICON_RU['back_2menu'])
    await callback.answer()


async def start_settings(message: Message, user_id: int):
    await message.answer(LEXICON_RU['settings_start'] + LEXICON_RU['change_count']+ LEXICON_RU['back_2menu'])
    create_empty_user(user_id)
    db = tables.psycopg2.connect(dbname=os.environ['POSTGRES_DB'],
                                 user=os.environ['POSTGRES_USER'],
                                 password=os.environ['POSTGRES_PASSWORD'],
                                 host=os.environ['POSTGRES_CONTAINER_NAME'],  # Это имя контейнера с базой данных
                                 port="5432")
    sql = db.cursor()
    sql.execute(f'SELECT set_test_words AS words FROM users WHERE user_id = {user_id}')
    query = next(sql)
    users.user_data[user_id]['words_in_test'] = int(query[0])
    await message.answer(LEXICON_RU['settings_current_pos'] + str(users.user_data[user_id]["words_in_test"]))

    users.user_data[user_id]['state'] = 'in_settings'
    sql.close()
    db.close()


@router.message(Command(commands=['settings']))
async def proccess_settings(message: Message):
    await start_settings(message, message.from_user.id)

@router.callback_query(Text(text=['to_settings']))
async def proccess_settings_button(callback: CallbackQuery):
    await callback.answer()
    await start_settings(callback.message, callback.from_user.id)