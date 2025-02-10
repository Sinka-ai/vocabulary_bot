from aiogram import Bot
from lexicon.lexicon_ru import LEXICON_RU
from aiogram.types import BotCommand


async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/menu',
                   description=LEXICON_RU['menu_descr']),
        BotCommand(command='/help',
                   description=LEXICON_RU['help_descr']),
        BotCommand(command='/test',
                   description=LEXICON_RU['test_descr']),
        BotCommand(command='/add',
                   description=LEXICON_RU['add_descr']),
        BotCommand(command='/delete',
                   description=LEXICON_RU['delete_descr']),
        BotCommand(command='/settings',
                   description=LEXICON_RU['settings_descr']),
        BotCommand(command='/tag',
                   description=LEXICON_RU['tag_descr']),
        BotCommand(command='/count',
                   description=LEXICON_RU['count_descr']), ]

    await bot.set_my_commands(main_menu_commands)
