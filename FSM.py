from aiogram.fsm.state import State, StatesGroup

class Autification(StatesGroup):
    login = State()
    
class Starts(StatesGroup):
    select_ex = State()
    select_mounth = State()
    
class AdminStarts(StatesGroup):
    select_ex = State()
    select_mounth = State()
    uploading_file = State()
    saving_file = State()