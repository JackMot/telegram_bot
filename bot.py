import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config.config_reader import load_config
from app.handlers.common import register_handlers_common
from app.handlers.work import register_handlers_work
from app.handlers.lab import register_handlers_lab
from handlers.survey_module.professor import register_handlers_professor
from handlers.survey_module.student import register_handlers_student
from handlers.survey_module.survey import register_handlers_survey
from handlers.survey_module.survey_menu import register_handlers_survey_menu
from app.handlers.register import register_handlers_register

logger = logging.getLogger(__name__)


# ----------

async def set_commands(bot: Bot):
    # Обьявление списка всплывающих подсказок
    commands = [
        BotCommand(command="/help", description="Получить информацию о боте"),
        BotCommand(command="/cancel", description="Отменить текущее действие"),
        BotCommand(command="/register", description="Зарегестрироваться в системе"),
        BotCommand(command="/lab", description="Загрузить ссылку на работу"),
        BotCommand(command="/work", description="Доступ к работам(для преподавателей)"),
        BotCommand(command="/start", description="Начать работу с ботом"),

    ]
    await bot.set_my_commands(commands)


# ----------

async def main():
    # Настройка логирования в stdout
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.info("Starting bot")

    # Парсинг файла конфигурации
    config = load_config("config/bot.ini")

    # Объявление и инициализация объектов бота и диспетчера
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(bot, storage=MemoryStorage())

    # Регистрация хэндлеров
    register_handlers_common(dp)
    register_handlers_register(dp)
    register_handlers_lab(dp)
    register_handlers_work(dp, admin_id=config.tg_bot.admin_id)
    register_handlers_survey_menu(dp)
    register_handlers_professor(dp)
    register_handlers_student(dp)
    register_handlers_survey(dp)

    # Установка команд бота
    await set_commands(bot)

    # Запуск поллинга
    await dp.start_polling()


# ----------

if __name__ == '__main__':
    asyncio.run(main())
