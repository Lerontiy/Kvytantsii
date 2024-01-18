from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import KeyboardButton
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from aiogram.filters.callback_data import CallbackData

from messages import messages
from database import db

from icecream import ic

from enum import Enum


class MyCitizenCallback(CallbackData, prefix="citizen"):
    db_id: int

class MyDirection(str, Enum):
    forward = "forward"
    back = "back"

class MyChangePageCallback(CallbackData, prefix="change_page"):
    direction: MyDirection
    last_id: int


class MyKeyboardMarcup:
    def choose_citizen_marcup(self, last_id:int):
        builder = InlineKeyboardBuilder()
        all_citizens_id_and_names = db.get_all_citizens_id_and_names()
        
        start_cou = last_id
        
        for i in range(last_id, len(all_citizens_id_and_names)):
            el = all_citizens_id_and_names[i]
            builder.button(text=el[1], callback_data=MyCitizenCallback(db_id=el[0]))
            last_id += 1
            if(last_id-start_cou == 20):
                break

        buider2 = InlineKeyboardBuilder()
        if(start_cou>0):
            buider2.button(text=messages["back"], callback_data=MyChangePageCallback(direction=MyDirection.back, last_id=last_id))
        del start_cou
        if(last_id < len(all_citizens_id_and_names)):
            buider2.button(text=messages["forward"], callback_data=MyChangePageCallback(direction=MyDirection.forward, last_id=last_id))
        del all_citizens_id_and_names, last_id
        buider2.adjust(2)

        builder.adjust(2)
        builder.attach(buider2)
        del buider2


        return builder.as_markup()
    
    def send_message_button_marcup(self):
        return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=messages["send_message"])]], resize_keyboard=True)
    
    def remove_reply_marcup(self):
        return ReplyKeyboardRemove()
    
kb_marcup = MyKeyboardMarcup()




        
            











