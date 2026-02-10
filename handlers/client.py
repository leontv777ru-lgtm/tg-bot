from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

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

    uid = message.from_user.id if user_id == 0 else user_id
    user = await DataBase.get_user_info(uid)

    if not user:
        await send_language_choice(message, first=True)
        return

    lang = user[2]

    await message.answer(
        languages[lang]["welcome"].format(
            first_name=message.from_user.first_name
        ),
        reply_markup=await ClientKeyboard.start_keyboard(lang),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("sel_lang|"))
async def select_language(callback: CallbackQuery):
    _, user_id, lang = callback.data.split("|")
    await DataBase.register(int(user_id), lang)
    await start_command(callback.message, user_id=int(user_id))

@router.callback_query(F.data.startswith("resel_lang|"))
async def reselect_language(callback: CallbackQuery):
    _, user_id, lang = callback.data.split("|")
    await DataBase.update_lang(int(user_id), lang)
    await start_command(callback.message, user_id=int(user_id))

async def send_language_choice(message: Message, first: bool):
    try:
        await message.delete()
    except:
        pass

    prefix = (
        f"sel_lang|{message.from_user.id}"
        if first
        else f"resel_lang|{message.from_user.id}"
    )

    await message.answer(
        "Select language",
        reply_markup=await ClientKeyboard.languages_board(prefix)
    )

@router.callback_query(F.data == "get_lang")
async def get_language(callback: CallbackQuery):
    await send_language_choice(callback.message, first=False)

@router.callback_query(F.data.in_(["back", "check"]), ChatJoinFilter())
async def menu_output(callback: CallbackQuery):
    try:
        await callback.message.delete()
    except:
        pass

    user = await DataBase.get_user_info(callback.from_user.id)
    if not user:
        await send_language_choice(callback.message, first=True)
        return

    lang = user[2]

    await callback.message.answer(
        languages[lang]["welcome_message"],
        reply_markup=await ClientKeyboard.menu_keyboard(user, lang),
        parse_mode="HTML"
    )

    await callback.answer()
