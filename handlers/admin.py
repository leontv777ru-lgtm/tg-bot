from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from database.db import DataBase
from states.change_ref import ChangeReferral

router = Router()

ADMIN_ID = 123456789  # ← поставь свой Telegram ID

@router.callback_query(F.data == "change_ref")
async def change_ref(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Нет доступа", show_alert=True)
        return

    await callback.message.answer("Введи новую реферальную ссылку:")
    await state.set_state(ChangeReferral.input_ref)
    await callback.answer()

@router.message(ChangeReferral.input_ref)
async def save_ref(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return

    await DataBase.edit_ref(message.text)
    await message.answer("✅ Реферальная ссылка обновлена")
    await state.clear()