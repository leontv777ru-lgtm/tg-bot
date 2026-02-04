from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from config import VERIF_CHANNEL_ID
from database.db import database
from keyboards.client import ClientKeyboard
from other.languages import languages
from aiogram.fsm.state import StatesGroup, State

router = Router()

class ChangeReferral(StatesGroup):
    input_ref = State()

@router.message(F.chat.func(lambda chat: chat.id == int(VERIF_CHANNEL_ID)))
async def channel_verification_handler(message: types.Message):
    if await database.get_user(message.text) is None:
        lang = await database.get_lang(int(message.text))
        await database.update_verifed(message.text)

        await message.bot.send_message(
            chat_id=int(message.text),
            text=languages[lang]["success_registration"],
            reply_markup=await ClientKeyboard.get_signal_keyboard(lang),
            parse_mode="HTML"
        )

@router.callback_query(F.data == "change_ref")
async def change_referral_callback_handler(
    callback: types.CallbackQuery,
    state: FSMContext
):
    lang = await database.get_lang(callback.from_user.id)

    await callback.message.delete()
    await callback.message.answer(
        languages[lang]["enter_new_ref"],
        parse_mode="HTML"
    )

    await state.set_state(ChangeReferral.input_ref)

@router.message(ChangeReferral.input_ref)
async def change_referral_message_state(
    message: types.Message,
    state: FSMContext
):
    lang = await database.get_lang(message.from_user.id)

    await database.edit_ref(message.text)

    await message.answer(
        languages[lang]["ref_changed"],
        parse_mode="HTML"
    )

    await state.clear()
