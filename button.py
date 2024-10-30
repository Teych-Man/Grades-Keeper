from aiogram import types

#! ----------------------------------------------------------------------------------------------------------------

select_mounth = types.ReplyKeyboardMarkup(keyboard=[
    [
        types.KeyboardButton(text="Январь"), types.KeyboardButton(text="Февраль"), types.KeyboardButton(text="Март")
        ],
    [
        types.KeyboardButton(text="Апрель"), types.KeyboardButton(text="Май"), types.KeyboardButton(text="Июнь")
        ],
    [
        types.KeyboardButton(text="Июль"), types.KeyboardButton(text="Август"), types.KeyboardButton(text="Сентябрь")
        ],
    [
        types.KeyboardButton(text="Октябрь"), types.KeyboardButton(text="Ноябрь"), types.KeyboardButton(text="Декабрь")
        ],
    [
        types.KeyboardButton(text="Назад"), types.KeyboardButton(text="Перезапустить бота")
    ]

    ], resize_keyboard=True)

#! ----------------------------------------------------------------------------------------------------------------

select_from_ex = types.ReplyKeyboardMarkup(keyboard=[
        [
            types.KeyboardButton(text="ПМ-1"), types.KeyboardButton(text="ПМ-2")
            ],
        [types.KeyboardButton(text="ПМ-3")
            ],
        [types.KeyboardButton(text="Перезапустить бота")]
        
        ], resize_keyboard=True)

#! ----------------------------------------------------------------------------------------------------------------

start_button_admin = types.ReplyKeyboardMarkup(keyboard=[
        [
            types.KeyboardButton(text="ПМ-1"), types.KeyboardButton(text="ПМ-2")
            ],
        [types.KeyboardButton(text="ПМ-3")
            ],
        [types.KeyboardButton(text="Добавить оценки")
            ]
        
        ], resize_keyboard=True)

#! ----------------------------------------------------------------------------------------------------------------

select_to_add_ex_admin = types.ReplyKeyboardMarkup(keyboard=[
        [
            types.KeyboardButton(text="ПМ-1"), types.KeyboardButton(text="ПМ-2")
            ],
        [types.KeyboardButton(text="ПМ-3")
            ],
        [types.KeyboardButton(text="Назад")
            ]

        ], resize_keyboard=True)

#! ----------------------------------------------------------------------------------------------------------------

cancel_to_add_ex_admin = types.ReplyKeyboardMarkup(keyboard=[
        [
            types.KeyboardButton(text="Отмена")
        ]

        ], resize_keyboard=True)