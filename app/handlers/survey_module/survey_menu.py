from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

import keyboards
from config.config_reader import load_config


class SurveyGeneralStates(StatesGroup):
    professor = State()
    student = State()


async def start(message: types.Message, state: FSMContext):
    config = load_config("config/bot.ini")
    if str(message.from_user.id) in config.tg_bot.admin_id:
        await SurveyGeneralStates.professor.set()
        kb = keyboards.get_professor_keyboard()
        await message.answer("Меню", reply_markup=kb)
    else:
        await SurveyGeneralStates.student.set()
        await state.update_data(answers={})
        await message.answer("Вы студент")


def register_handlers_survey_menu(dp: Dispatcher):
    dp.register_message_handler(start, commands=['survey'], state="*")
