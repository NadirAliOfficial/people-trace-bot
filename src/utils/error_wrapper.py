from functools import wraps
from config.config_manager import NODE_ENV
from telegram import Update
from telegram.ext import ContextTypes

import traceback
import logging
import os

logger = logging.getLogger(__name__)


def catch_async(func):
    """Decorator to catch exceptions for asynchronous functions."""

    @wraps(func)
    async def wrapper(
        update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs
    ):
        try:
            return await func(update, context, *args, **kwargs)
        except Exception as e:
            if not NODE_ENV == "production":
                # Full traceback in development
                error_message = "".join(
                    traceback.format_exception(type(e), e, e.__traceback__)
                )
                logger.error(f"Exception in {func.__name__}:\n{error_message}")

                # Send detailed error message in development (optional)
                user_message = f"⚠️  Debug Error:\n```{error_message}```"
            else:
                # Shorter message in production
                logger.error(f"Error in {func.__name__}: {str(e)}")
                user_message = f"⚠️  An error occurred. Please try again later."

            # Check if we have message or callback_query
            if update.message:
                await update.message.reply_text(user_message, parse_mode="Markdown")
            elif update.callback_query:
                if update.callback_query.message:
                    await update.callback_query.message.reply_text(
                        user_message, parse_mode="Markdown"
                    )

            return None  # Optionally, return a default value or end the conversation

    return wrapper
