from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import CHANNEL_URL, SUPP
from database.db import DataBase
from other.languages import languages


class ClientKeyboard:

    @staticmethod
    async def start_keyboard(lang: str):
        ikb = InlineKeyboardBuilder()
        ikb.button(text=languages[lang]["subscribe"], url=CHANNEL_URL)
        ikb.button(text=languages[lang]["check"], callback_data="check")
        ikb.adjust(1)
        return ikb.as_markup()

    @staticmethod
    async def menu_keyboard(user_info: list, lang: str):
        ikb = InlineKeyboardBuilder()

        ikb.button(text=languages[lang]["register"], callback_data="register")
        ikb.button(text=languages[lang]["instruction"], callback_data="instruction")
        ikb.button(text=languages[lang]["choose_lang"], callback_data="get_lang")
        ikb.button(text="Help🆘", url=SUPP)

