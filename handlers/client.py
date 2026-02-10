from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from database.db import DataBase
from keyboards.client import ClientKeyboard
from other.languages import languages
from other.filters import ChatJoinFilter

router = Router()

@router.message(CommandStart())
async def start_command(message: Message, user_id: int = 0):
    try:
        await message.delete()
    except:
        pass

    user = await DataBase.get_user_info(
        message.from_user.id if user_id == 0 else user_id
    )

    if user is None:
        await get_language(message, True)
        return

    await message.answer(
        languages[user[2]]["welcome"].format(
            first_name=message.from_user.first_name
        ),
        reply_markup=await ClientKeyboard.start_keyboard(user[2]),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("sel_lang"))
async def select_language(callback: CallbackQuery):
    data = callback.data.split("|")
    await DataBase.register(callback.from_user.id, data[2])
    await start_command(callback.message, user_id=int(data[1]))

@router.callback_query(F.data.startswith("resel_lang"))
async def reselect_language(callback: CallbackQuery):
    data = callback.data.split("|")
    await DataBase.update_lang(int(data[1]), data[2])
    await start_command(callback.message, user_id=int(data[1]))

@router.callback_query(F.data == "get_lang")
async def get_language(query: Message | CallbackQuery, first: bool = False):
    msg = query.message if isinstance(query, CallbackQuery) else query

    try:
        await msg.delete()
    except:
        pass

    prefix = (
        f"sel_lang|{msg.from_user.id}"
        if first
        else f"resel_lang|{msg.from_user.id}"
    )

    await msg.answer(
        "Select language",
        reply_markup=await ClientKeyboard.languages_board(prefix)
    )

@router.callback_query(F.data.in_(["back", "check"]), ChatJoinFilter())
async def menu_output(callback: CallbackQuery):
    try:
        await callback.message.delete()
    except:
        pass

    user_info = await DataBase.get_user_info(callback.from_user.id)
    lang = await DataBase.get_lang(callback.from_user.id)

    await callback.message.answer(
        languages[lang]["welcome_message"],
        reply_markup=await ClientKeyboard.menu_keyboard(user_info, lang),
        parse_mode="HTML"
    )

    await callback.answer()
