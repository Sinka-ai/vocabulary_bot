import os
import data.create_tables as tables
import data.user_session as users
from aiogram.filters import Command, Text
import filters.filters as f
from lexicon.lexicon_ru import LEXICON_RU
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram import Router, F
from data.create_empty import create_empty_user
from keyboard.buttons import menu_keyboard
import csv


global MY_ID_TELEGRAM
MY_ID_TELEGRAM = os.environ['MY_TG_ID']
admin_ids = [MY_ID_TELEGRAM]
router = Router()


@router.message(Command(commands=['start']))
async def proccess_start(message: Message):
    db = tables.psycopg2.connect(dbname=os.environ['POSTGRES_DB'],
                                 user=os.environ['POSTGRES_USER'],
                                 password=os.environ['POSTGRES_PASSWORD'],
                                 host=os.environ['POSTGRES_CONTAINER_NAME'],  # Это имя контейнера с базой данных
                                 port="5432")
    sql = db.cursor()
    create_empty_user(message.from_user.id)
    user_id = message.from_user.id
    sql.execute(f'SELECT COUNT(*) FROM users WHERE user_id={user_id}')
    if sql.fetchone()[0]==0:
        sql.execute(f"INSERT INTO users VALUES ({user_id}, 0, 0, 0, 1000, 5, 0, 0)")
        db.commit()
    await message.answer(LEXICON_RU['welcome'])
    sql.close()
    db.close()




@router.message(Command(commands = ['stop']))
async def proccess_stop(message: Message):
    user_id = message.from_user.id
    create_empty_user(user_id)
    await message.answer('Операция остановлена. Чтобы выйти в меню нажмите /menu')
    users.user_data[user_id]['state'] = 'in_menu'


@router.message(Command(commands = ['menu']))
async def proccess_menu(message: Message):
    user_id = message.from_user.id
    create_empty_user(user_id)
    users.user_data[user_id]['state'] = 'in_menu'
    db = tables.psycopg2.connect(dbname=os.environ['POSTGRES_DB'],
                                 user=os.environ['POSTGRES_USER'],
                                 password=os.environ['POSTGRES_PASSWORD'],
                                 host=os.environ['POSTGRES_CONTAINER_NAME'],  # Это имя контейнера с базой данных
                                 port="5432")
    sql = db.cursor()
    sql.execute(f'SELECT rating FROM users WHERE user_id={user_id}')
    user_rating = int(sql.fetchone()[0])
    await message.answer(f'Рейтинг: <b>{user_rating}</b>', reply_markup=menu_keyboard)
    sql.close()
    db.close()


@router.message( F.text.startswith('/admin'), f.IsAdmin(admin_ids))
async def proccess_admin(message: Message, text: str):
    db = tables.psycopg2.connect(dbname=os.environ['POSTGRES_DB'],
                                 user=os.environ['POSTGRES_USER'],
                                 password=os.environ['POSTGRES_PASSWORD'],
                                 host=os.environ['POSTGRES_CONTAINER_NAME'],  # Это имя контейнера с базой данных
                                 port="5432")
    sql = db.cursor()
    sql.execute(f'SELECT * FROM users')
    user_to_delete: int
    try:
        user_to_delete = int(text)
    except ValueError as e:
        await message.answer("введи число")
        return
    await message.answer(str(sql.fetchmany(5)))
    sql.execute(f'SELECT COUNT() FROM users WHERE (user_id = {user_to_delete})')
    if next(sql)[0] != 0:
        with db:
            sql.execute(f'DELETE FROM users WHERE (user_id = {user_to_delete})')
            sql.commit()
            await message.answer(f'пользователь {user_to_delete} удалён')
    else:
        await message.answer('такого пользователя нет')
    sql.close()
    db.close()


@router.callback_query(Text(text=['to_prune']))
async def proccess_prune(callback: CallbackQuery):
    await callback.message.answer('Происходит очистка вашего словаря ...')
    db = tables.psycopg2.connect(dbname=os.environ['POSTGRES_DB'],
                                 user=os.environ['POSTGRES_USER'],
                                 password=os.environ['POSTGRES_PASSWORD'],
                                 host=os.environ['POSTGRES_CONTAINER_NAME'],  # Это имя контейнера с базой данных
                                 port="5432")
    sql = db.cursor()
    sql.execute(f'DELETE FROM words WHERE user_id={callback.from_user.id}')
    db.commit()
    sql.close()
    db.close()
    await callback.message.answer('Ваш словарь успешно удален! \nВыйти в /menu')
    await callback.answer()


@router.callback_query(Text(text=['to_download']))
async def proccess_csv(callback: CallbackQuery):
    db = tables.psycopg2.connect(dbname=os.environ['POSTGRES_DB'],
                                 user=os.environ['POSTGRES_USER'],
                                 password=os.environ['POSTGRES_PASSWORD'],
                                 host=os.environ['POSTGRES_CONTAINER_NAME'],  # Это имя контейнера с базой данных
                                 port="5432")
    sql = db.cursor()
    sql.execute(f'SELECT en, ru, definition, complexity FROM words WHERE user_id={callback.from_user.id}')
    rows = sql.fetchall()

    print(rows)

    # Определяем путь к файлу CSV
    csv_file = f'words_data_{callback.from_user.id}.csv'



    # Записываем данные в файл CSV
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['english', 'russian', 'definition', 'complexity'])  # Заголовки колонок

        for row in rows:
            writer.writerow([str(val) for val in row])

    sql.close()
    db.close()
    await callback.message.answer('Ваш файл собран:')
    await callback.message.answer_document(FSInputFile(csv_file))
    await callback.message.answer('Выйти в /menu')
    os.remove(csv_file)
    await callback.answer()
