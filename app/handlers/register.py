import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from app.handlers.messages import MESSAGES
from api.api import add_data


class Auth(StatesGroup):
    name = State()
    group = State()
    subgroup = State()


# ----------

async def register_start(message: types.Message):
    logging.info('register init by ' + str(message.from_user.id))
    await message.answer(MESSAGES['register_start'])
    await Auth.next()


# ----------

async def register_name(message: types.Message, state: FSMContext):
    await state.update_data(id=message.from_user.id)
    if len(message.text.split(" ")) == 3:
        await state.update_data(name=message.text)
        await message.answer(MESSAGES['register_group'])
        await Auth.next()
    else:
        await message.answer(MESSAGES['register_wrong_name'])


# ----------

async def register_group(message: types.Message, state: FSMContext):
    await state.update_data(group=message.text)
    await message.answer(MESSAGES['register_subgroup'])
    await Auth.next()


# ----------

async def register_subgroup(message: types.Message, state: FSMContext):
    await state.update_data(subgroup=message.text)
    user_data=await state.get_data()
    user_data_list = list(user_data.values())
    # await add_data(user_data_list, "Студенты")
    await message.answer(str(user_data))
    await message.answer(str(user_data_list))
    await message.answer(MESSAGES['register_end'])
    await state.finish()


# ----------


def register_handlers_register(dp: Dispatcher):
    # Все команды обрабатываются здесь.
    # Тут можно задавать параметры выполнения и ключевые слова по которым они будут вызываться.
    dp.register_message_handler(register_start, commands="register", state="*")
    dp.register_message_handler(register_name, state=Auth.name)
    dp.register_message_handler(register_group, state=Auth.group)
    dp.register_message_handler(register_subgroup, state=Auth.subgroup)
