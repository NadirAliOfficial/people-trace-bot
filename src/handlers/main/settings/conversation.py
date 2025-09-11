from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    filters,
)

from constants import State
from handlers.settings_handler import (
    settings_command,
    settings_menu_callback,
    handle_setting_mobile,
    handle_setting_tac,
)
from handlers.start_handler import cancel

settings_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("settings", settings_command)],
    states={
        State.SETTINGS.SETTINGS_MENU: [
            CallbackQueryHandler(settings_menu_callback, pattern="^settings_"),
            CallbackQueryHandler(settings_menu_callback, pattern="^setlang_"),
        ],
        State.SETTINGS.WAITING_FOR_MOBILE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_setting_mobile),
        ],
        State.SETTINGS.SETTINGS_MOBILE_MANAGEMENT: [
            CallbackQueryHandler(settings_menu_callback, pattern="^mobile_"),
        ],
        State.SETTINGS.MOBILE_VERIFICATION: [
            CallbackQueryHandler(settings_menu_callback, pattern="^remove_"),
            CallbackQueryHandler(settings_menu_callback, pattern="^settings_mobile"),
        ],
        State.SETTINGS.SETTINGS_CREATE_CASE_TAC: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_setting_tac),
        ],
    },
    fallbacks=[
        CommandHandler("cancel", cancel),
    ],
    allow_reentry=True,
)
