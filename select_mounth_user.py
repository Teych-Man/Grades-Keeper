from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext

import os
import logging

import FSM as fsm
from button import select_from_ex, select_mounth, start_button_admin
from Databases.main_databases import select_first_and_last_name
import create_table

#! ----------------------------------------------------------------------------------------------------------------

router = Router()

#! ----------------------------------------------------------------------------------------------------------------

@router.message(fsm.Starts.select_ex)
async def deffer_users(message: Message, state: FSMContext):
    if message.text == "ПМ-1":
        await state.update_data(subject=1)  
        await message.answer("Выберите месяц", reply_markup=select_mounth)
        await state.set_state(fsm.Starts.select_mounth)
        logging.info(f"{message.from_user.id} | {message.from_user.full_name} | {message.from_user.first_name} {message.from_user.last_name} -> Пользователь выбрал предмет ПМ-1")

    elif message.text == "ПМ-2":
        await state.update_data(subject=2)
        await message.answer("Выберите месяц", reply_markup=select_mounth)
        await state.set_state(fsm.Starts.select_mounth)
        logging.info(f"{message.from_user.id} | {message.from_user.full_name} | {message.from_user.first_name} {message.from_user.last_name} -> Пользователь выбрал предмет ПМ-2")

    elif message.text == "ПМ-3":
        await state.update_data(subject=3)
        await message.answer("Выберите месяц", reply_markup=select_mounth)
        await state.set_state(fsm.Starts.select_mounth)
        logging.info(f"{message.from_user.id} | {message.from_user.full_name} | {message.from_user.first_name} {message.from_user.last_name} -> Пользователь выбрал предмет ПМ-3")

    else:
        await message.answer(f'Действия "{message.text}" не существует! Попробуйте еще раз', reply_markup=select_from_ex)
        logging.info(f"{message.from_user.id} | {message.from_user.full_name} | {message.from_user.first_name} {message.from_user.last_name} -> Пользователь выбрал несуществующее действие {message.text}")

#! ----------------------------------------------------------------------------------------------------------------

@router.message(fsm.Starts.select_mounth)
async def deffer_month(message: Message, state: FSMContext):
    data = await state.get_data()
    subject = data.get("subject") 
    
    if message.text == "Назад": 
        last_first_name_str = await select_first_and_last_name(message)
        if 'Ердос' in last_first_name_str or 'Роман' in last_first_name_str:
            await message.answer("Чтобы выбрать предмет или добавить оценки нажмите на кнопку", reply_markup=start_button_admin)
            await state.set_state(fsm.AdminStarts.select_ex)
            logging.info(f"{message.from_user.id} | {message.from_user.full_name} | {message.from_user.first_name} {message.from_user.last_name} -> Администратор вернулся назад на выбор предмета")
        else:
            await message.answer("Выберите предмет", reply_markup=select_from_ex)
            await state.set_state(fsm.Starts.select_ex)
            logging.info(f"{message.from_user.id} | {message.from_user.full_name} | {message.from_user.first_name} {message.from_user.last_name} -> Пользователь вернулся назад на выбор предмета")

    elif message.text == "Июль" or message.text == "Август":
        await message.answer(f"Невозможно посмотреть оценки за {message.text}!")
        await state.set_state(fsm.Starts.select_mounth)
        logging.info(f"{message.from_user.id} | {message.from_user.full_name} | {message.from_user.first_name} {message.from_user.last_name} -> Пользователь выбрал месяц {message.text} в котором невозможно посмотреть оценки")

    else:
        if message.text in ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]:
            
            if subject == 1:
                mounth_sender = message.text

            elif subject == 2:
                mounth_sender = message.text
                
            elif subject == 3:
                mounth_sender = message.text

            else:
                await message.answer("Неправильный выбор. Попробуйте ещё раз.")
                logging.info(f"{message.from_user.id} | {message.from_user.full_name} | {message.from_user.first_name} {message.from_user.last_name} -> Пользователь выбрал несуществующий предмет {message.text}")
        else:
            await message.answer(f"Месяца {message.text} не существует! Выберите другой месяц")
            logging.info(f"{message.from_user.id} | {message.from_user.full_name} | {message.from_user.first_name} {message.from_user.last_name} -> Пользователь выбрал несуществующий месяц {message.text}")
        await create_photo_and_send(message, state, subject, mounth_sender)

#! ----------------------------------------------------------------------------------------------------------------

async def create_photo_and_send(message, state, subject, mounth_sender):
    if subject == 1:
        if os.path.exists(fr"Excel/PM_1/{mounth_sender}/pm_1.xlsx") == True:
            logging.info(f"{message.from_user.id} | {message.from_user.full_name} | {message.from_user.first_name} {message.from_user.last_name} -> Отправка фото с оценками по ПМ-1")
            await message.answer("Происходит отправка фото с оценками...")
            path_to_excel = fr"Excel/PM_1/{mounth_sender}/pm_1.xlsx"

            select_name = await select_first_and_last_name(message)

            path_to_image = await create_table.create_table_from_excel(select_name, mounth_sender, path_to_excel, message)

            await message.answer_photo(photo=FSInputFile(path_to_image))
            
            os.remove(path_to_image)
            logging.info(f"{message.from_user.id} | {message.from_user.full_name} | {message.from_user.first_name} {message.from_user.last_name} -> Фото с оценками по ПМ-1 отправлено")   
            
        else:
            await message.answer(f"Оценки за {mounth_sender} по предмету ПМ-1 не найдены", reply_markup=select_mounth)
            await state.set_state(fsm.Starts.select_mounth)
            logging.info(f"{message.from_user.id} | {message.from_user.full_name} | {message.from_user.first_name} {message.from_user.last_name} -> Оценки за {mounth_sender} по предмету ПМ-1 не найдены")

    elif subject == 2:
        if os.path.exists(fr"Excel/PM_2/{mounth_sender}/pm_2.xlsx") == True:
            logging.info(f"{message.from_user.id} | {message.from_user.full_name} | {message.from_user.first_name} {message.from_user.last_name} -> Отправка фото с оценками по ПМ-2")
            await message.answer("Происходит отправка фото с оценками...")
            path_to_excel = fr"Excel/PM_2/{mounth_sender}/pm_2.xlsx"

            select_name = await select_first_and_last_name(message)

            path_to_image = await create_table.create_table_from_excel(select_name, mounth_sender, path_to_excel, message)

            await message.answer_photo(photo=FSInputFile(path_to_image))

            os.remove(path_to_image)
            logging.info(f"{message.from_user.id} | {message.from_user.full_name} | {message.from_user.first_name} {message.from_user.last_name} -> Фото с оценками по ПМ-2 отправлено")
        else:
            await message.answer(f"Оценки за {mounth_sender} по предмету ПМ-2 не найдены", reply_markup=select_mounth)
            await state.set_state(fsm.Starts.select_mounth)
            logging.info(f"{message.from_user.id} | {message.from_user.full_name} | {message.from_user.first_name} {message.from_user.last_name} -> Оценки за {mounth_sender} по предмету ПМ-2 не найдены")

    elif subject == 3:
        if os.path.exists(fr"Excel/PM_3/{mounth_sender}/pm_3.xlsx") == True:
            logging.info(f"{message.from_user.id} | {message.from_user.full_name} | {message.from_user.first_name} {message.from_user.last_name} -> Отправка фото с оценками по ПМ-3")
            await message.answer("Происходит отправка фото с оценками...")
            path_to_excel = fr"Excel/PM_3/{mounth_sender}/pm_3.xlsx"

            select_name = await select_first_and_last_name(message)

            path_to_image = await create_table.create_table_from_excel(select_name, mounth_sender, path_to_excel, message)

            await message.answer_photo(photo=FSInputFile(path_to_image))

            os.remove(path_to_image)
            logging.info(f"{message.from_user.id} | {message.from_user.full_name} | {message.from_user.first_name} {message.from_user.last_name} -> Фото с оценками по ПМ-3 отправлено")
        else:
            await message.answer(f"Оценки за {mounth_sender} по предмету ПМ-3 не найдены", reply_markup=select_mounth)
            await state.set_state(fsm.Starts.select_mounth)
            logging.info(f"{message.from_user.id} | {message.from_user.full_name} | {message.from_user.first_name} {message.from_user.last_name} -> Оценки за {mounth_sender} по предмету ПМ-3 не найдены")
        
    else:
        await message.answer("Произошла ошибка, попробуйте позже")
        logging.info(f"{message.from_user.id} | {message.from_user.full_name} | {message.from_user.first_name} {message.from_user.last_name} -> Произошла ошибка при отправке фото (create_photo_and_send)")