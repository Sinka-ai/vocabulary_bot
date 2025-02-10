from create_bot import dp, bot
import handlers
from main_menu import set_main_menu
from data.update_table import update


print('bot is running')


if __name__ == '__main__':
    update()
    dp.startup.register(set_main_menu)
    dp.include_router(handlers.settings_handlers.router)
    dp.include_router(handlers.delete_handlers.router)
    dp.include_router(handlers.add_handlers.router)
    dp.include_router(handlers.test_handlers.router)
    dp.include_router(handlers.general_handlers.router)
    dp.include_router(handlers.generator_handlers.router)
    dp.include_router(handlers.ai_handlers.router)
    dp.run_polling(bot)
