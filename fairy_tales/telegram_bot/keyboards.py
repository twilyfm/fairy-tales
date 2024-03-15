from aiogram import types


def keyboard_settings():
    buttons_settings = [
        [
            types.InlineKeyboardButton(text="Age", callback_data="user_age"),
            types.InlineKeyboardButton(
                text="Read time", callback_data="user_time"
            ),
        ],
        [
            types.InlineKeyboardButton(
                text="Description", callback_data="user_prompt"
            )
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons_settings)
    return keyboard


def keyboard_age():
    buttons_age = [
        [
            types.InlineKeyboardButton(
                text="< 5 лет", callback_data="age_one"
            ),
            types.InlineKeyboardButton(
                text="7-10 лет", callback_data="age_three"
            ),
        ],
        [
            types.InlineKeyboardButton(
                text="5-7 лет", callback_data="age_two"
            ),
            types.InlineKeyboardButton(
                text="> 10 лет", callback_data="age_four"
            ),
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons_age)
    return keyboard


def keyboard_time():
    buttons_time = [
        [
            types.InlineKeyboardButton(
                text="< 2 мин", callback_data="time_one"
            ),
            types.InlineKeyboardButton(
                text="5-7 мин", callback_data="time_three"
            ),
        ],
        [
            types.InlineKeyboardButton(
                text="2-5 мин", callback_data="time_two"
            ),
            types.InlineKeyboardButton(
                text="> 7 мин", callback_data="time_four"
            ),
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons_time)
    return keyboard
