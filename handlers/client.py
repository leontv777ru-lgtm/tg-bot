from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database.db import DataBase
from keyboards.client import ClientKeyboard
from other.languages import languages
from config import VERIF_CHANNEL_ID

router = Router()

class ChangeReferral(StatesGroup):
    input_ref = State()

@router.message(F.chat.func(lambda chat: chat.id == int(VERIF_CHANNEL_ID)))
async def channel_verification_handler(message: types.Message):
    if await DataBase.get_user(int(message.text)) is None:
        lang = await DataBase.get_lang(int(message.text))
        await DataBase.update_verified(int(message.text))

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
    lang = await DataBase.get_lang(callback.from_user.id)
    await callback.message.delete()
    await callback.message.answer(languages[lang]["enter_new_ref"])
    await state.set_state(ChangeReferral.input_ref)

@router.message(ChangeReferral.input_ref)
async def change_referral_message_state(
    message: types.Message,
    state: FSMContext
):
    lang = await DataBase.get_lang(message.from_user.id)
    await DataBase.edit_ref(message.text)

    await message.answer(languages[lang]["ref_changed"])
    await state.clear()
