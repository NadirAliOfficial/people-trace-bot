from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes


def catch_async(func):
    """Decorator to catch exceptions for asynchronous functions."""

    @wraps(func)
    async def wrapper(
        update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs
    ):
        try:
            return await func(update, context, *args, **kwargs)
        except Exception as e:
            # Check if we have message or callback_query
            if update.message:
                await update.message.reply_text(f"⚠️  {str(e)}")
            elif update.callback_query:
                # Make sure we have the callback_query's message before replying
                if update.callback_query.message:
                    await update.callback_query.message.reply_text(f"⚠️  {str(e)}")
            return None  # Optionally, return a default value or end the conversation

    return wrapper
