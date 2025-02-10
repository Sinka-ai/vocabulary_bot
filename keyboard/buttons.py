from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from lexicon.lexicon_ru import LEXICON_RU

button_yes_settings = InlineKeyboardButton(text=LEXICON_RU['yes'], callback_data='yes_pressed_settings')
button_no_settings = InlineKeyboardButton(text=LEXICON_RU['no'], callback_data='no_pressed_settings')

keyboard_yes_no_settings = InlineKeyboardMarkup(inline_keyboard=[[button_yes_settings,button_no_settings]])



button_yes_word = InlineKeyboardButton(text=LEXICON_RU['yes'], callback_data='yes_pressed_word')
button_no_word = InlineKeyboardButton(text=LEXICON_RU['no'], callback_data='no_pressed_word')

keyboard_yes_no_word = InlineKeyboardMarkup(inline_keyboard=[[button_yes_word, button_no_word]])



button_yes_generator = InlineKeyboardButton(text=LEXICON_RU['yes'], callback_data='yes_pressed_generator')
button_no_generator = InlineKeyboardButton(text=LEXICON_RU['no'], callback_data='no_pressed_generator')

keyboard_yes_no_generator = InlineKeyboardMarkup(inline_keyboard=[[button_yes_generator, button_no_generator]])


button_yes_delete = InlineKeyboardButton(text=LEXICON_RU['yes'], callback_data='yes_pressed_delete')
button_no_delete = InlineKeyboardButton(text=LEXICON_RU['no'], callback_data='no_pressed_delete')

keyboard_yes_no_delete = InlineKeyboardMarkup(inline_keyboard=[[button_yes_delete,button_no_delete]])

menu_buttons = []

callbacks = [['to_add', 'to_test'], ['to_generator', 'to_ai'], ['to_prune', 'to_download'], ['to_delete', 'to_settings']]
texts = [['Добавить слово', 'Тест'], ['Генератор','AI'], ['Очистка словаря', 'Скачать таблицу'], ['Удалить слово', 'Настройки']]

for i in range(len(callbacks)):
    menu_buttons.append([InlineKeyboardButton(text=texts[i][0],callback_data=callbacks[i][0]),
                        InlineKeyboardButton(text=texts[i][1], callback_data=callbacks[i][1])])

menu_keyboard = InlineKeyboardMarkup(inline_keyboard=menu_buttons)




