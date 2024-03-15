import asyncio
import logging

import hydra
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters.command import Command
from omegaconf import DictConfig, OmegaConf

# Диспетчер
dp = Dispatcher()

# типо бд
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


@dp.message(Command("settings"))
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


@dp.callback_query(F.data.startswith("user_"))
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


@dp.callback_query(F.data.startswith("age_"))
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


@dp.callback_query(F.data.startswith("time_"))
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


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Лалалалалал про этот бот. Про передаваемые параметры..."
    )


async def main():
    # скорее всего это плохо, надо поменять....
    @hydra.main(version_base=None, config_path="../conf", config_name="config")
    def extract_config(cfg: DictConfig):
        OmegaConf.to_yaml(cfg)
        global token
        token = cfg.telebot.Telegram_token

    extract_config()
    bot = Bot(token)
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
