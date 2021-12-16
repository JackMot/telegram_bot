import json

import gspread
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

import keyboards
import spreadsheets
from handlers.survey_module.survey_menu import SurveyGeneralStates
STUDENTS_ID = [""]  # needs to be get from spreadsheets


class ProfessorStates(StatesGroup):
    check_survey = State()
    start_survey = State()


async def menu(message: types.Message, state: FSMContext):
    kb = keyboards.get_professor_keyboard()
    await message.answer("Меню", reply_markup=kb)


async def choose_survey(callback_query: types.CallbackQuery, state: FSMContext):
    kb = keyboards.get_tests_keyboard()
    await callback_query.message.edit_text(text="Выберите тест", reply_markup=kb)
    if callback_query.data.startswith("check"):
        await ProfessorStates.check_survey.set()
    elif callback_query.data.startswith("start"):
        await ProfessorStates.start_survey.set()
    await callback_query.answer()


async def check_survey(callback_query: types.CallbackQuery, state: FSMContext):
    kb = keyboards.get_professor_keyboard()
    separated_data = callback_query.data.split(";")
    survey_sheet_name = separated_data[1]
    try:
        survey = spreadsheets.get_test(survey_sheet_name)
        question_number = 0
        for question in survey:
            answers_kb = keyboards.get_answers_keyboard(question, question_number, survey_sheet_name)
            question_number += 1
            await callback_query.message.bot.send_message(chat_id=callback_query.message.chat.id,
                                                          text=f"{question['Вопрос']}",
                                                          reply_markup=answers_kb)
        await callback_query.message.answer(f"Выведено {question_number} вопросов", reply_markup=kb)
        await callback_query.answer()
        await SurveyGeneralStates.professor.set()
    except gspread.exceptions.WorksheetNotFound:
        await callback_query.message.answer(f"Лист с названием {survey_sheet_name} не найден :(")
        await callback_query.message.answer("Меню", reply_markup=kb)
        await SurveyGeneralStates.professor.set()


async def start_survey(callback_query: types.CallbackQuery, state: FSMContext):
    kb = keyboards.get_professor_keyboard()
    separated_data = callback_query.data.split(";")
    survey_sheet_name = separated_data[1]
    start_survey_kb = keyboards.start_survey_keyboard(survey_sheet_name)
    try:
        survey = spreadsheets.get_test(survey_sheet_name)
        with open(f'Surveys/{survey_sheet_name}.json', 'w', encoding='utf-8') as f:
            json.dump(survey, f, ensure_ascii=False, indent=4)
        student_count = 0
        for student in STUDENTS_ID:
            await callback_query.message.bot.send_message(text="Доступен новый тест.\n"
                                                               "Чтобы приступить, нажмите кнопку ниже",
                                                          reply_markup=start_survey_kb,
                                                          chat_id=student)
            student_count += 1
        await callback_query.message.answer(f"Сообщение выведено {student_count} студентам")
        await callback_query.message.answer("Меню", reply_markup=kb)
        await callback_query.answer()
        await SurveyGeneralStates.professor.set()
    except gspread.exceptions.WorksheetNotFound:
        await callback_query.message.answer(f"Лист с названием {survey_sheet_name} не найден :(")
        await callback_query.message.answer("Меню", reply_markup=kb)
        await SurveyGeneralStates.professor.set()


def register_handlers_professor(dp: Dispatcher):
    dp.register_message_handler(menu, commands=['menu'], state=SurveyGeneralStates.professor)
    dp.register_callback_query_handler(choose_survey, state=SurveyGeneralStates.professor)
    dp.register_callback_query_handler(check_survey, lambda c: c.data.startswith("test"),
                                       state=ProfessorStates.check_survey)
    dp.register_callback_query_handler(start_survey, lambda c: c.data.startswith("test"),
                                       state=ProfessorStates.start_survey)
