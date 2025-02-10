from data.user_session import user_data
from data.create_empty import create_empty_user
from aiogram.filters import Command, Text
import filters.filters as f
from lexicon.lexicon_ru import LEXICON_RU
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from classes.classes import Dictionary
from data.update_table import update
import psycopg2
import os




router = Router()


def make_wr(tot, cor):
    if tot==0:
        return 0
    else:
        return cor/tot

async def test_start(message: Message, user_id: int):
    update()
    db = psycopg2.connect(dbname=os.environ['POSTGRES_DB'],
                          user=os.environ['POSTGRES_USER'],
                          password=os.environ['POSTGRES_PASSWORD'],
                          host=os.environ['POSTGRES_CONTAINER_NAME'],  # Это имя контейнера с базой данных
                          port="5432")
    sql = db.cursor()
    sql.execute(f'SELECT set_test_words FROM users WHERE user_id={user_id}')
    count = next(sql)[0]
    create_empty_user(user_id)
    user_data[user_id]['test_dictionary'] = Dictionary(count, user_id)
    user_data[user_id]['test_gen'] = user_data[user_id]['test_dictionary']()
    if len(user_data[user_id]['test_dictionary'].words) == 0:
        await message.answer(LEXICON_RU['no_words']+LEXICON_RU['back_2menu'])
        sql.close()
        db.close()
    else:
        user_data[user_id]['current_word'] = next(user_data[user_id]['test_gen'])
        user_data[user_id]['state'] = 'in_test'
        user_data[user_id]['total'] = 0
        user_data[user_id]['correct'] = 0
        user_data[user_id]['rating_diff'] = 0
        sql.close()
        db.close()
        await message.answer(LEXICON_RU['test_start'] + str(len(user_data[user_id]['test_dictionary'].words)))
        await message.answer(LEXICON_RU['word_in_en']+f"<b>{user_data[user_id]['current_word'].en}</b>")


@router.message(Command(commands=['test']))
async def start_test(message:Message):
    await test_start(message, message.from_user.id)


@router.callback_query(Text(text=['to_test']))
async def start_test_button(callback: CallbackQuery):
    await callback.answer()
    await test_start(callback.message, callback.from_user.id)



@router.message(f.InTest(user_data), Command(commands=['stop']))
async def stop_in_test(message: Message):
    user_id = message.from_user.id
    await message.answer(LEXICON_RU['test_ended']+
    str(make_wr(user_data[user_id]['total'],user_data[user_id]['correct'])))
    await message.answer(LEXICON_RU['back_2menu'])
    user_data[user_id]['test_dictionary'].update(user_id, user_data[user_id]['rating_diff'])


@router.message(F.text,~Text(startswith='/'), f.InTest(user_data))
async def check_word(message: Message):
    user_id = message.from_user.id
    user_translate = message.text.lower()
    real_translate = user_data[user_id]['current_word'].ru
    user_data[user_id]['total']+=1
    user_data[user_id]['current_word'].total += 1
    if user_translate == real_translate:
        user_data[user_id]['rating_diff']+= 5
        user_data[user_id]['correct']+=1
        user_data[user_id]['current_word'].success += 1
        await message.answer(LEXICON_RU['correct_answer'])
        user_data[user_id]['test_dictionary'].delete_word(real_translate)
        try:
            user_data[user_id]['current_word'] = next(user_data[user_id]['test_gen'])
            await message.answer(LEXICON_RU['next_word']+f"<b>{user_data[user_id]['current_word'].en}</b>")
        except StopIteration:
            await message.answer(LEXICON_RU['test_ended']+
            str(make_wr(user_data[user_id]['total'],user_data[user_id]['correct'])*100.0)+'%')
            await message.answer(LEXICON_RU['back_2menu'])
            user_data[user_id]['test_dictionary'].update(user_id, user_data[user_id]['rating_diff'])
    else:
        user_data[user_id]['rating_diff']-=5
        await message.answer(LEXICON_RU['wrong_answer']+real_translate+LEXICON_RU['rating_minus'])
        user_data[user_id]['current_word'] = next(user_data[user_id]['test_gen'])
        await message.answer(LEXICON_RU['next_word']+user_data[user_id]['current_word'].en)
