import logging
import validators

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from app.handlers.messages import MESSAGES
from api.api import add_data


class OrderWork(StatesGroup):
    waiting_for_link = State()


# ----------

async def lab_start(message: types.Message):
    logging.info('Lab init by ' + str(message.from_user.id))
    await message.answer(MESSAGES['link_start'])
    await OrderWork.waiting_for_link.set()


# ----------

async def lab_link_send(message: types.Message, state: FSMContext):
    link = message.text
    try:
        if validators.url(link):
            if add_data([str(message.from_user.id), message.text], "Работы"):
                await message.answer(MESSAGES['link_update'])
            else:
                await message.answer(MESSAGES['link_update_error'])
            await state.finish()
        else:
            await message.answer(MESSAGES['link_invalid'])
    except:
        await message.answer(MESSAGES['link_update_error'])
        await state.finish()


# ----------

def register_handlers_lab(dp: Dispatcher):
    # Все команды обрабатываются здесь.
    # Тут можно задавать параметры выполнения и ключевые слова по которым они будут вызываться.
    dp.register_message_handler(lab_start, commands="lab", state="*")
    dp.register_message_handler(lab_link_send, state=OrderWork.waiting_for_link)
