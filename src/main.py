import asyncio
import logging


from models.extend_reward_model import ExtendReward
from models.finder_model import Finder
from models.mobile_number_model import MobileNumber
from models.user_model import User
import os
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), "src"))


from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from telegram.ext import ApplicationBuilder

from config.config_manager import MONGODB_NAME, MONGODB_URI, NODE_ENV
from handlers.handlers import (
    start_handler,
    settings_handler,
    wallet_handler,
    listing_handler,
    stats_handler
)
from handlers.start_handler import error_handler
from models.case_model import Case
from config.config_manager import TOKEN
from models.wallet_model import Wallet
from utils.helper import setup_logging

setup_logging()


async def main_setup():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(start_handler)
    application.add_handler(wallet_handler)
    application.add_handler(settings_handler)
    application.add_handler(listing_handler)
    application.add_handler(stats_handler)

    application.add_error_handler(error_handler)

    logger = logging.getLogger(__name__)
    logger.info("Bot is starting...")
    await application.run_polling()


async def init_db():
    try:
        print(f"MONGODB_URI = {MONGODB_URI}")
        print(f"{NODE_ENV.lower() == "production"}")
        client = AsyncIOMotorClient(
            MONGODB_URI if NODE_ENV.lower() == "production" else "mongodb://localhost:27017/finder_advertiser"
        )
        await init_beanie(
            database=client[MONGODB_NAME],
            document_models=[User, Case, Wallet, MobileNumber, Finder, ExtendReward],
        )
        print("Database Connected Successfully 🚀.")
        await main_setup()
    except Exception as e:
        print(f"\033[91mError initializing database: {e}\033[0m")


async def main():
    await init_db()


if __name__ == "__main__":
    import nest_asyncio

    nest_asyncio.apply()

    try:
        loop = asyncio.get_running_loop()
        loop.run_until_complete(main())
    except RuntimeError:
        asyncio.run(main())
