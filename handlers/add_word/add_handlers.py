import data.create_tables as tables
import data.user_session as users
from aiogram.filters import Command, Text
import filters.filters as f
from lexicon.lexicon_ru import LEXICON_RU
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from data.create_empty import create_empty_user
import os
import requests
from bs4 import BeautifulSoup
from googletrans import Translator
from keyboard.buttons import keyboard_yes_no_word





router = Router()



# Функция для поиска определения слова и примеров использования
# Используется парсер html страницы cambridge dictionary
def get_word_definition(word, lang='english'):
    # URL для запроса на Cambridge Dictionary
    url = f'https://dictionary.cambridge.org/dictionary/{lang}/{word}'

    # Заголовки для запроса
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    try:
        # Отправляем запрос на сайт
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Проверяем, был ли запрос успешным

    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")
        return None

    # Используем BeautifulSoup для парсинга страницы
    soup = BeautifulSoup(response.text, 'html.parser')

    # Ищем определение
    definition_tag = soup.find('div', class_='def ddef_d db')
    if definition_tag:
        definition = definition_tag.text.strip()
    else:
        definition = "No definition found."

    example_tag = soup.find('span', class_='eg deg')
    if example_tag:
        example = example_tag.text.strip()
    else:
        example = "No example found."

    complexity_tag = soup.find('span', class_='epp-xref')
    if complexity_tag:
        complexity = complexity_tag.text.strip()
    else:
        complexity = "No complexity found."

    return {
        'word': word,
        'definition': definition[:-1],
        'example': example,
        'complexity': complexity
    }


#ищем в словаре кэмбриджа слово, похожее на данное
def cambridge_find_similar(word, lang='english'):
    url = f'https://dictionary.cambridge.org/spellcheck/{lang}/?q={word}'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    try:
        # Отправляем запрос на сайт
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Проверяем, был ли запрос успешным

    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")
        return None

    # Используем BeautifulSoup для парсинга страницы
    soup = BeautifulSoup(response.text, 'html.parser')

    similar_word_tag = soup.find('li', class_='lp-5')
    return similar_word_tag.text.strip()


# Функция для перевода английского слова на русский язык
def translate_to_russian(word):
    translator = Translator()
    translation = translator.translate(word, src='en', dest='ru')
    return translation.text


def find_word(word, lang='english'):
    w = get_word_definition(word, lang)
    answer = ''
    if w['definition'] == 'No definition found':
        another_word = cambridge_find_similar(word)
        answer += f'Возможно вы имели ввиду слово <b>{another_word}</b>. \n'
        w = get_word_definition(another_word, lang)
    w['translate'] = translate_to_russian(w["word"])
    answer += f'<b>Слово</b>: {w["word"]}. \n<b>Перевод</b>: {w["translate"]}. \n<b>Определение</b>: {w["definition"]}. '
    answer += f'\n<b>Пример использования</b>: {w["example"]}. \n<b>Сложность</b>: {w["complexity"]}'

    return answer, w


async def proccess_add(message: Message, user_id: int):
    create_empty_user(user_id)
    users.user_data[user_id]['state'] = 'in_add_en'
    await message.answer('Введите слово на английском')


@router.message(Command(commands=['add']))
async def proccess_add_command(message: Message):
    await proccess_add(message, message.from_user.id)


@router.callback_query(Text(text=['to_add']))
async def proccess_add_button(callback: CallbackQuery):
    await callback.answer()
    await proccess_add(callback.message, callback.from_user.id)


@router.message(F.text, ~Text(startswith='/'), f.InAddEn(users.user_data))
async def proccess_add_en(message: Message):
    user_id = message.from_user.id
    en = message.text.lower()


    text, word = find_word(en)

    users.user_data[user_id]['en'] = word['word']
    users.user_data[user_id]['ru'] = word['translate']
    users.user_data[user_id]['definition'] = word['definition']
    users.user_data[user_id]['complexity'] = word['complexity']

    await message.answer(text + '\nДобавляем?', reply_markup=keyboard_yes_no_word)


@router.callback_query(Text(text=['yes_pressed_word']))
async def proccess_add_word(callback: CallbackQuery):
    user_id = callback.from_user.id
    db = tables.psycopg2.connect(dbname=os.environ['POSTGRES_DB'],
                                     user=os.environ['POSTGRES_USER'],
                                     password=os.environ['POSTGRES_PASSWORD'],
                                     host=os.environ['POSTGRES_CONTAINER_NAME'],  # Это имя контейнера с базой данных
                                     port="5432")
    sql = db.cursor()
    sql.execute(f"INSERT INTO words VALUES ({user_id}, '{users.user_data[user_id]['en']}', "
                f" '{users.user_data[user_id]['ru']}',  '{users.user_data[user_id]['definition']}', "
                f" '{users.user_data[user_id]['complexity']}',  CURRENT_DATE, 0, 0, 0, 0) ")

    db.commit()
    sql.close()
    db.close()
    await callback.message.answer(f'Слово <b>{users.user_data[user_id]["en"]}, {users.user_data[user_id]["ru"]}</b>,'
                         ' успешно добавлено!\n'
                                  'Вы можете либо добавить следующее слово, либо выйти в /menu')
    await callback.answer()
    users.user_data[user_id]['state'] = 'in_add_en'


@router.callback_query(Text(text=['no_pressed_word']))
async def proccess_next_word(callback: CallbackQuery):
    await callback.message.answer('Введите другое слово:')
    await callback.answer()

