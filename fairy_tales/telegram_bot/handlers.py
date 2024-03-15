from aiogram import F, Router, types
from aiogram.filters.command import Command
from keyboards import keyboard_settings
from telegram_tools import (
    get_user_info,
    update_age,
    update_time,
    update_user_age_info,
    update_user_time_info,
)

router = Router()


@router.message(Command("settings"))
async def cmd_settings(message: types.Message, user_id=None):
    if not user_id:
        user_id = message.from_user.id
    user_age, user_time = await get_user_info(user_id)

    await message.answer(
        f"Здесь вы можете ввести или изменить ранее выбранные параметры.\n"
        f"\n"
        f"Текущие параметры: \n"
        f" * Возраст: {user_age}\n"
        f" * Время чтения: {user_time}",
        reply_markup=keyboard_settings(),
    )


@router.callback_query(F.data.startswith("user_"))
async def callbacks_settings(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_age, user_time = await get_user_info(user_id)
    action = callback.data.split("_")[1]

    if action == "age":
        await update_age(callback.message, user_age)

    elif action == "time":
        await update_time(callback.message, user_time)

    elif action == "prompt":
        await callback.message.edit_text(
            f"Текущие параметры: \n"
            f" * Возраст: {user_age}\n"
            f" * Время чтения: {user_time}\n\n"
            f"Можете написать краткое описание сказки"
        )


@router.callback_query(F.data.startswith("age_"))
async def callbacks_age(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    action = callback.data.split("_")[1]

    if action == "one":
        age_new = "< 5 лет"
    elif action == "two":
        age_new = "5-7 лет"
    elif action == "three":
        age_new = "7-10 лет"
    elif action == "four":
        age_new = "> 10 лет"

    await update_user_age_info(user_id, age_new)
    await callback.message.edit_text(f"Возраст изменен на {age_new}")
    await cmd_settings(callback.message, user_id)


@router.callback_query(F.data.startswith("time_"))
async def callbacks_time(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    action = callback.data.split("_")[1]

    if action == "one":
        time_new = "< 2 мин"
    elif action == "two":
        time_new = "2-5 мин"
    elif action == "three":
        time_new = "5-7 мин"
    elif action == "four":
        time_new = "> 7 мин"

    await update_user_time_info(user_id, time_new)
    await callback.message.edit_text(f"Время чтения изменено на {time_new}")
    await cmd_settings(callback.message, user_id)


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Лалалалалал про этот бот. Про передаваемые параметры..."
    )
