import asyncio
import logging

import handlers
import hydra
from aiogram import Bot, Dispatcher
from omegaconf import DictConfig, OmegaConf


async def main():
    # скорее всего это плохо, надо поменять....
    @hydra.main(
        version_base=None, config_path="../../conf", config_name="config"
    )
    def extract_config(cfg: DictConfig):
        OmegaConf.to_yaml(cfg)
        global token
        token = cfg.telebot.Telegram_token

    extract_config()

    bot = Bot(token)
    dp = Dispatcher()

    dp.include_router(handlers.router)

    logging.basicConfig(level=logging.INFO)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
