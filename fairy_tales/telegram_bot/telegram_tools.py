from aiogram import types
from keyboards import keyboard_age, keyboard_time

users_info = {}


async def get_user_info(user_id):
    # будет ходить в бд
    if user_id not in users_info:
        users_info[user_id] = {"age": "Не выбран", "time_read": "Не выбрано"}
    return users_info[user_id]["age"], users_info[user_id]["time_read"]


async def update_user_age_info(user_id, new_age):
    # будет ходить в бд
    if user_id not in users_info:
        await get_user_info(user_id)
    users_info[user_id]["age"] = new_age


async def update_user_time_info(user_id, new_time):
    # будет ходить в бд
    if user_id not in users_info:
        await get_user_info(user_id)
    users_info[user_id]["time_read"] = new_time


async def update_age(message: types.Message, curr_age):
    await message.edit_text(
        f"Текущий возраст: {curr_age}\n\n"
        f"Выберите возраст на который хотите изменить настройки",
        reply_markup=keyboard_age(),
    )


async def update_time(message: types.Message, curr_time):
    await message.edit_text(
        f"curr time is {curr_time}", reply_markup=keyboard_time()
    )
