from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class ClientKeyboard:

    @staticmethod
    async def start_keyboard(lang: str):
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🚀 Start" if lang == "en" else "🚀 Старт",
                        callback_data="check"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🌍 Language" if lang == "en" else "🌍 Язык",
                        callback_data="get_lang"
                    )
                ]
            ]
        )

    @staticmethod
    async def languages_board(prefix: str):
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🇷🇺 Русский",
                        callback_data=f"{prefix}|ru"
                    ),
                    InlineKeyboardButton(
                        text="🇬🇧 English",
                        callback_data=f"{prefix}|en"
                    )
                ]
            ]
        )

    @staticmethod
    async def menu_keyboard(user, lang: str):
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🎯 Get signal" if lang == "en" else "🎯 Получить сигнал",
                        callback_data="signal"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🌍 Language" if lang == "en" else "🌍 Язык",
                        callback_data="get_lang"
                    )
                ]
            ]
        )
