from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router

form_router = Router()

class Form(StatesGroup):
    get_message = State()
    