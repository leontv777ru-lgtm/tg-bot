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

        if user_info[1] != "verifed":
            ikb.button(text=languages[lang]["get_signal"], callback_data="register")
        else:
            ikb.button(
                text=languages[lang]["get_signal"],
                web_app=types.WebAppInfo(
                    url="https://entypublic.github.io/dogmain/"
                )
            )

        ikb.adjust(2, 1, 1)
        return ikb.as_markup()

    @staticmethod
    async def register_keyboard(user_id: int, lang: str):
        ikb = InlineKeyboardBuilder()
        ref = await DataBase.get_ref()
        ikb.button(
            text=languages[lang]["register_action"],
            url=f"{ref}&sub1={user_id}"
        )
        ikb.button(text=languages[lang]["back"], callback_data="back")
        ikb.adjust(1)
        return ikb.as_markup()

    @staticmethod
    async def back_keyboard(lang: str):
        ikb = InlineKeyboardBuilder()
        ikb.button(text=languages[lang]["back"], callback_data="back")
        return ikb.as_markup()

    @staticmethod
    async def get_signal_keyboard(lang: str):
        ikb = InlineKeyboardBuilder()
        ikb.button(
            text=languages[lang]["get_signal"],
            web_app=types.WebAppInfo(
                url="https://entypublic.github.io/dogmain/"
            )
        )
        ikb.button(text=languages[lang]["back"], callback_data="back")
        ikb.adjust(1)
        return ikb.as_markup()