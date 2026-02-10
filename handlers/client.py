from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

from config import CHANNEL_URL, SUPP
from other.languages import languages

class ClientKeyboard:

    @staticmethod
    async def start_keyboard(lang: str) -> InlineKeyboardMarkup:
        ikb = InlineKeyboardBuilder()

        ikb.button(
            text=languages[lang]["subscribe"],
            url=CHANNEL_URL
        )
        ikb.button(
            text=languages[lang]["check"],
            callback_data="check"
        )

        ikb.adjust(1)
        return ikb.as_markup()

    @staticmethod
    async def menu_keyboard(user_info: list, lang: str) -> InlineKeyboardMarkup:
        ikb = InlineKeyboardBuilder()

        ikb.button(
            text=languages[lang]["register"],
            callback_data="register"
        )
        ikb.button(
            text=languages[lang]["instruction"],
            callback_data="instruction"
        )
        ikb.button(
            text=languages[lang]["choose_lang"],
            callback_data="get_lang"
        )
        ikb.button(
            text="Help 🆘",
            url=SUPP
        )

        ikb.adjust(1)
        return ikb.as_markup()

    @staticmethod
    async def languages_board(prefix: str) -> InlineKeyboardMarkup:
        ikb = InlineKeyboardBuilder()

        for lang in languages:
            ikb.button(
                text=languages[lang]["lang_name"],
                callback_data=f"{prefix}|{lang}"
            )

        ikb.adjust(2)
        return ikb.as_markup()

    @staticmethod
    async def back_keyboard(lang: str) -> InlineKeyboardMarkup:
        ikb = InlineKeyboardBuilder()

        ikb.button(
            text=languages[lang]["back"],
            callback_data="back"
        )

        return ikb.as_markup()

    @staticmethod
    async def register_keyboard(callback, lang: str) -> InlineKeyboardMarkup:
        ikb = InlineKeyboardBuilder()

        ikb.button(
            text=languages[lang]["back"],
            callback_data="back"
        )

        return ikb.as_markup()

    @staticmethod
    async def get_signal_keyboard(lang: str) -> InlineKeyboardMarkup:
        ikb = InlineKeyboardBuilder()

        ikb.button(
            text=languages[lang]["get_signal"],
            callback_data="get_signal"
        )

        return ikb.as_markup()
