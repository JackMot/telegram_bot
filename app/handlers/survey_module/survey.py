import json
import logging

from aiogram import Dispatcher, types
from aiogram.bot.bot import Bot as bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import config
import keyboards
from handlers.survey_module.survey_menu import SurveyGeneralStates
from handlers.survey_module.professor import ProfessorStates
from handlers.survey_module.student import StudentStates
from spreadsheets import add_result_to_worksheet
logger = logging.getLogger(__name__)


async def callback_answering_test(callback_query: types.CallbackQuery, state: FSMContext):
    # state = dp.current_state(user=callback_query.message.chat.id)
    separated_data = callback_query.data.split(";")
    survey_sheet_name = separated_data[1]
    with open(f'Surveys/{survey_sheet_name}.json', encoding='utf-8') as json_file:
        survey = json.load(json_file)

        question_number = int(separated_data[2])
        # Проверка ответов на правильность
        if separated_data[0] == "question":
            current_question = survey[question_number - 1]
            answers = list((await state.get_data())['answers'])
            is_correct = False
            if current_question['правильный'] == separated_data[3]:
                is_correct = True
            answer = {
                "Вопрос": str(survey[question_number - 1]['Вопрос']),
                "is_correct": is_correct
            }
            answers.append(answer)
            await state.update_data(answers=answers)
        # Формируем сообщение с вопросом и ответами
        if question_number < len(survey):
            current_question = survey[question_number]
            answers_kb = keyboards.get_answers_keyboard(current_question, question_number, separated_data[1])
            await callback_query.message.edit_text(text=f"{current_question['Вопрос']}", reply_markup=answers_kb)
            await callback_query.answer()
        # Тест закончен
        else:
            answers = (await state.get_data())['answers']

            correct_answers = 0

            for answer in answers:
                if answer['is_correct']:
                    correct_answers += 1

            logger.info(answers)

            # ВПИСАТЬ в test_name имя выбранного теста(Вместо 'Test')!
            survey_results_name = survey_sheet_name + ' result'

            # В user_data положить фул имя и группу студента из модуля регистрации
            user_data = callback_query.message.chat.id

            add_result_to_worksheet(survey_results_name, user_data, answers)

            await state.reset_state()
            await SurveyGeneralStates.student.set()
            await callback_query.message.edit_text(text=f"Вы прошли тест на {correct_answers}/{len(answers)}")
            await callback_query.answer()


def register_handlers_survey(dp: Dispatcher):
    dp.register_callback_query_handler(callback_answering_test, lambda c: c.data, state=SurveyGeneralStates.student)
