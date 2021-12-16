from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import spreadsheets


def get_answers_keyboard(question: dict, question_number: int, survey_sheet_name: str) -> InlineKeyboardMarkup:
    answers_kb = InlineKeyboardMarkup(row_width=2)
    answers = []
    keys = list(question.keys())
    next_question_number = question_number + 1
    for answer in keys:
        if answer.startswith("ответ"):
            answers.append(InlineKeyboardButton(f"{question[answer]}", callback_data=f"question;"
                                                                                     f"{survey_sheet_name};"
                                                                                     f"{next_question_number};"
                                                                                     f"{answer}"))
    answers_kb.add(*answers)
    return answers_kb


def get_professor_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=2)
    buttons = [InlineKeyboardButton(f"Запустить опрос", callback_data=f"start"),
               InlineKeyboardButton(f"Проверить вопросы", callback_data=f"check")]
    return kb.add(*buttons)


def get_tests_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    buttons = []
    tests = spreadsheets.get_all_tests()
    for test in tests:
        if "result" not in test.title:
            buttons.append(InlineKeyboardButton(f"{test.title}", callback_data=f"test;{test.title}"))
    return kb.add(*buttons)


def start_survey_keyboard(survey_sheet_name: str) -> InlineKeyboardMarkup:
    answers_kb = InlineKeyboardMarkup(row_width=2)
    start_btn = InlineKeyboardButton(f"Начать тест", callback_data=f"start;{survey_sheet_name};0")
    return answers_kb.add(start_btn)
