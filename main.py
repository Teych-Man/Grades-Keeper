from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, BaseMiddleware, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from typing import Callable, Awaitable, Dict, Any
from cachetools import TTLCache

import asyncio
import logging
import datetime
import os

from button import select_from_ex, start_button_admin
import FSM as fsm
from Admins import start_admin
from Databases import main_databases
import select_mounth_user

#! ----------------------------------------------------------------------------------------------------------------


bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()


#! ----------------------------------------------------------------------------------------------------------------


class AntiFloodMiddleware(BaseMiddleware):

    def __init__(self, time_limit: int=1) -> None:
        self.limit = TTLCache(maxsize=10_000, ttl=time_limit)

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if event.chat.id in self.limit:
            await event.answer('Подождите немного перед следующей командой!')
            logging.warning(f"{event.from_user.id} | {event.from_user.full_name} | {event.from_user.first_name} {event.from_user.last_name} -> Флудит боту")
            return
        
        else:
            self.limit[event.chat.id] = None
        return await handler(event, data) 


#! ----------------------------------------------------------------------------------------------------------------


@dp.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    user_exists = await main_databases.check_user_exists(message.from_user)

    if not user_exists:
        await message.answer("Чтобы начать пользоваться ботом, введите ваш логин.", reply_markup=ReplyKeyboardRemove())
        logging.info(f"{message.from_user.id} | {message.from_user.full_name} | {message.from_user.first_name} {message.from_user.last_name} -> Не найден в базе данных. Началась авторизация")
        await state.set_state(fsm.Autification.login)

    else:
        last_first_name_str = await main_databases.select_first_and_last_name(message)
        if 'Иван' in last_first_name_str or 'Иван' in last_first_name_str:
            await message.answer(f"Здравствуйте {last_first_name_str}, чтобы выбрать предмет или добавить оценки нажмите на кнопку", reply_markup=start_button_admin)
            await state.clear()
            await state.set_state(fsm.AdminStarts.select_ex)
            logging.info(f"{message.from_user.id} | {message.from_user.full_name} | {message.from_user.first_name} {message.from_user.last_name} -> Администратор ввел команду /start")

        else:
            await message.answer(f"Здравствуйте {last_first_name_str}, чтобы выбрать предмет нажмите на кнопку", reply_markup=select_from_ex)
            await state.clear()
            await state.set_state(fsm.Starts.select_ex)
            logging.info(f"{message.from_user.id} | {message.from_user.full_name} | {message.from_user.first_name} {message.from_user.last_name} -> пользователь ввел команду /start")


@dp.message(fsm.Autification.login)
async def get_login(message: Message, state: FSMContext):
    logging.info(f"{message.from_user.id} | {message.from_user.full_name} | {message.from_user.first_name} {message.from_user.last_name} -> Ввел логин ({message.text}), выполнятеся проверка логина")
    await state.update_data(login=message.text)
    data = await state.get_data()
    await main_databases.add_user_to_database(message.from_user, message, data, state, cmd_start)


#! ----------------------------------------------------------------------------------------------------------------


@dp.message(F.text == "Перезапустить бота")
async def main_menu(message: Message, state: FSMContext):
    await cmd_start(message, state)
    logging.info(f"{message.from_user.id} | {message.from_user.full_name} | {message.from_user.first_name} {message.from_user.first_name} -> Перезапустил бота")


#! ----------------------------------------------------------------------------------------------------------------


async def main():
    today = datetime.datetime.today()
    file_exists = os.path.isfile(fr"Logs/{today.year}-{today.month}-{today.day}.log")
    filemode = "a" if file_exists else "w"
    logging.basicConfig(level=logging.INFO, filename=fr"Logs/{today.year}-{today.month}-{today.day}.log", filemode=filemode, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')
    logging.info(f"\n\n\n\n---------------------------------------- Запуск бота ----------------------------------------") 
    
    
    print("Запустился")
    dp.message.middleware(AntiFloodMiddleware())

    dp.include_routers(
        start_admin.router, 
        select_mounth_user.router
    )
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":    
    try:
        asyncio.run(main())   
    except KeyboardInterrupt:
        print("Выключение")