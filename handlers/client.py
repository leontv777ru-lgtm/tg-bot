from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from database.db import DataBase
from keyboards.client import ClientKeyboard
from states.change_ref import ChangeReferral
from config import VERIF_CHANNEL_ID
from languages import languages

router = Router()

# =======================
# /start
# =======================
@router.message(CommandStart())
async def start_handler(message: types.Message):
    lang = await DataBase.get_lang(message.from_user.id)

    if lang is None:
        lang = "ru"
        await DataBase.register(
            user_id=message.from_user.id,
            language=lang
        )

    await message.answer(
        languages[lang]["start"],
        reply_markup=await ClientKeyboard.get_signal_keyboard(lang),
        parse_mode="HTML"
    )

# =======================
# Верификация из канала
# =======================
@router.message(F.chat.func(lambda chat: chat.id == int(VERIF_CHANNEL_ID)))
async def channel_verification_handler(message: types.Message):
    user_id = int(message.text)

    if await DataBase.get_user(user_id) is None:
        lang = await DataBase.get_lang(user_id)
        await DataBase.update_verified(user_id)

        await message.bot.send_message(
            chat_id=user_id,
            text=languages[lang]["success_registration"],
            reply_markup=await ClientKeyboard.get_signal_keyboard(lang),
            parse_mode="HTML"
        )

# =======================
# Смена рефералки
# =======================
@router.callback_query(F.data == "change_ref")
async def change_referral_callback_handler(
    callback: types.CallbackQuery,
    state: FSMContext
):
    lang = await DataBase.get_lang(callback.from_user.id)

    await callback.message.delete()
    await callback.message.answer(
        languages[lang]["enter_new_ref"]
    )

    await state.set_state(ChangeReferral.input_ref)

@router.message(ChangeReferral.input_ref)
async def change_referral_message_state(
    message: types.Message,
    state: FSMContext
):
    lang = await DataBase.get_lang(message.from_user.id)

    await DataBase.edit_ref(message.text)
    await message.answer(
        languages[lang]["ref_changed"]
    )

    await state.clear()
