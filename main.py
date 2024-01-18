import asyncio
import logging
import sys
import os

from aiogram import types, Bot, Dispatcher, Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.types.callback_query import CallbackQuery
from aiogram.utils.markdown import hbold
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.base import BaseStorage
from aiogram.client.bot import Bot

from icecream import ic

from settings import get_bot_token
from state_machine import Form
from database import db
from messages import messages
from reply_marcups import kb_marcup, MyCitizenCallback, MyChangePageCallback

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1MJThUytl3meSMUC-aTC9k6Kv-wxegei80BjvHLIxWGo"


form_router = Router()
message_router = Router()
callback_router = Router()

bot = Bot(get_bot_token(), parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())
dp.include_routers(form_router, callback_router, message_router)


@callback_router.callback_query(MyChangePageCallback.filter())
async def change_page(query:CallbackQuery, callback_data:MyChangePageCallback, bot:Bot):
    if(callback_data.direction == "forward"):
        reply_markup=kb_marcup.choose_citizen_marcup(callback_data.last_id)
    else:
        reply_markup=kb_marcup.choose_citizen_marcup(callback_data.last_id-40)

    await bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id, reply_markup=reply_markup)
    del reply_markup

    return


@callback_router.callback_query(MyCitizenCallback.filter())
async def citizen_choose(query:CallbackQuery, callback_data:MyCitizenCallback, state:FSMContext):
    await query.message.answer(messages["send_kvytanciiu"]%db.get_userId_and_name_by_dbId(callback_data.db_id)[1], reply_markup=kb_marcup.remove_reply_marcup())
    await state.set_state(Form.get_message)
    await state.set_data({"db_id": callback_data.db_id})

    return


@form_router.message(Form.get_message)
async def send_message_to_citizen(message:Message, state:FSMContext):
    db_id = await state.get_data()
    try:
        await message.send_copy(db.get_userId_and_name_by_dbId(db_id["db_id"])[0])
        await message.answer(messages["message_sent"], reply_markup=kb_marcup.send_message_button_marcup())
    except:
        await message.answer(messages["message_didnt_sent"], reply_markup=kb_marcup.send_message_button_marcup())

    await state.clear()
    return


@message_router.message(F.text == messages["send_message"])
async def send_message(message: Message, state:FSMContext):
    db.check_user_in_db(message.from_user.id)
    if db.is_admin(message.from_user.id):
        await message.answer(messages['choose_citizen'], reply_markup=kb_marcup.choose_citizen_marcup(0))
    return


@message_router.message(CommandStart())
async def start_command(message:Message):
    await message.answer(messages["start_message"], reply_markup=kb_marcup.send_message_button_marcup())
    return


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass