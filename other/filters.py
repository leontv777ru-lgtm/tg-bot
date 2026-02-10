from aiogram.filters import BaseFilter
from aiogram import types, Bot

from config import CHANNEL_ID
from database.db import DataBase


class ChatJoinFilter(BaseFilter):
    async def __call__(self, message: types.Message, bot: Bot):
        member = await bot.get_chat_member(
            chat_id=int(CHANNEL_ID),
            user_id=message.from_user.id
        )
        return member.status.value in ("member", "administrator", "creator")


class RegisteredFilter(BaseFilter):
    async def __call__(self, callback: types.CallbackQuery):
        return await DataBase.get_user_info(callback.from_user.id) is not None
