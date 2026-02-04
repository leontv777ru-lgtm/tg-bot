from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db import database

class ClientKeyboard:

    @staticmethod
    async def get_signal_keyboard(lang: str):
        ref = await database.get_ref()
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🚀 Регистрация", url=ref)]
        ])

    @staticmethod
    async def back_keyboard(lang: str):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅ Назад", callback_data="back")]
        ])
