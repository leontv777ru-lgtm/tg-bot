from aiogram.fsm.state import State, StatesGroup

class ChangeReferral(StatesGroup):
    input_ref = State()