from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from handlers.survey_module.survey_menu import SurveyGeneralStates


class StudentStates(StatesGroup):
    passes_survey = State()


async def menu(message: types.Message, state: FSMContext):
    await message.answer("Студент")


def register_handlers_student(dp: Dispatcher):
    dp.register_message_handler(menu, commands=['menu'], state=SurveyGeneralStates.student)
