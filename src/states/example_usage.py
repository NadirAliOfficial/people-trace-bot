"""
Example usage of the separated state structure
This file demonstrates how to use the new state classes in conversation handlers
"""

from telegram.ext import ConversationHandler, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from states import StartState, WalletState, SettingsState, FinderState, StatsState, ListingState, CaseState

# Example: Start Handler using StartState
def start_handler_example():
    return ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            StartState.LANGUAGE_SELECTED: [
                CallbackQueryHandler(handle_language, pattern="^lang_")
            ],
            StartState.CHOOSE_COUNTRY: [
                CallbackQueryHandler(handle_country, pattern="^country_"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_country_text)
            ],
            StartState.CREATE_CASE_PERSON_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_person_name)
            ],
            StartState.END: [CommandHandler("start", start_command)]
        },
        fallbacks=[CommandHandler("cancel", cancel_command)],
        allow_reentry=True
    )

# Example: Wallet Handler using WalletState
def wallet_handler_example():
    return ConversationHandler(
        entry_points=[CommandHandler("wallet", wallet_command)],
        states={
            WalletState.WALLET_MENU: [
                CallbackQueryHandler(handle_wallet_menu, pattern="^wallet_")
            ],
            WalletState.SOL_WALLET_DETAIL: [
                CallbackQueryHandler(handle_sol_wallet, pattern="^sol_")
            ],
            WalletState.USDT_WALLET_DETAIL: [
                CallbackQueryHandler(handle_usdt_wallet, pattern="^usdt_")
            ],
            WalletState.END: [CommandHandler("wallet", wallet_command)]
        },
        fallbacks=[CommandHandler("cancel", cancel_command)],
        allow_reentry=True
    )

# Example: Settings Handler using SettingsState
def settings_handler_example():
    return ConversationHandler(
        entry_points=[CommandHandler("settings", settings_command)],
        states={
            SettingsState.SETTINGS_MENU: [
                CallbackQueryHandler(handle_settings_menu, pattern="^settings_")
            ],
            SettingsState.WAITING_FOR_MOBILE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_mobile_input)
            ],
            SettingsState.END: [CommandHandler("settings", settings_command)]
        },
        fallbacks=[CommandHandler("cancel", cancel_command)],
        allow_reentry=True
    )

# Example: Finder Handler using FinderState
def finder_handler_example():
    return ConversationHandler(
        entry_points=[CommandHandler("finder", finder_command)],
        states={
            FinderState.CREATE_CASE_MOBILE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_finder_mobile)
            ],
            FinderState.CHOOSE_COUNTRY: [
                CallbackQueryHandler(handle_finder_country, pattern="^country_")
            ],
            FinderState.END: [CommandHandler("finder", finder_command)]
        },
        fallbacks=[CommandHandler("cancel", cancel_command)],
        allow_reentry=True
    )

# Example: Stats Handler using StatsState
def stats_handler_example():
    return ConversationHandler(
        entry_points=[CommandHandler("stats", stats_command)],
        states={
            StatsState.SHOW_STATS_MENU: [
                CallbackQueryHandler(handle_stats_menu, pattern="^stats_")
            ],
            StatsState.SHOW_UNSOLVED_COUNTRIES: [
                CallbackQueryHandler(handle_unsolved_countries, pattern="^country_")
            ],
            StatsState.END: [CommandHandler("stats", stats_command)]
        },
        fallbacks=[CommandHandler("cancel", cancel_command)],
        allow_reentry=True
    )

# Example: Listing Handler using ListingState
def listing_handler_example():
    return ConversationHandler(
        entry_points=[CommandHandler("listing", listing_command)],
        states={
            ListingState.CASE_DETAILS: [
                CallbackQueryHandler(handle_case_details, pattern="^case_")
            ],
            ListingState.EDIT_FIELD: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_edit_field)
            ],
            ListingState.END: [CommandHandler("listing", listing_command)]
        },
        fallbacks=[CommandHandler("cancel", cancel_command)],
        allow_reentry=True
    )

# Example: Case Handler using CaseState
def case_handler_example():
    return ConversationHandler(
        entry_points=[CommandHandler("case", case_command)],
        states={
            CaseState.CONFIRM_TRANSFER: [
                CallbackQueryHandler(handle_transfer, pattern="^transfer_")
            ],
            CaseState.ENTER_PRIVATE_KEY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_private_key)
            ],
            CaseState.END: [CommandHandler("case", case_command)]
        },
        fallbacks=[CommandHandler("cancel", cancel_command)],
        allow_reentry=True
    )

# Example: Mixed states in a single handler
def mixed_handler_example():
    return ConversationHandler(
        entry_points=[CommandHandler("mixed", mixed_command)],
        states={
            # Start states
            StartState.CHOOSE_ACTION: [
                CallbackQueryHandler(handle_action, pattern="^action_")
            ],
            # Wallet states
            WalletState.WALLET_MENU: [
                CallbackQueryHandler(handle_wallet, pattern="^wallet_")
            ],
            # Settings states
            SettingsState.SETTINGS_MENU: [
                CallbackQueryHandler(handle_settings, pattern="^settings_")
            ],
            # End state
            StartState.END: [CommandHandler("mixed", mixed_command)]
        },
        fallbacks=[CommandHandler("cancel", cancel_command)],
        allow_reentry=True
    )

# Dummy functions for the examples (these would be your actual handler functions)
def start_command(update, context): pass
def wallet_command(update, context): pass
def settings_command(update, context): pass
def finder_command(update, context): pass
def stats_command(update, context): pass
def listing_command(update, context): pass
def case_command(update, context): pass
def mixed_command(update, context): pass
def cancel_command(update, context): pass

# Handler functions
def handle_language(update, context): pass
def handle_country(update, context): pass
def handle_country_text(update, context): pass
def handle_person_name(update, context): pass
def handle_wallet_menu(update, context): pass
def handle_sol_wallet(update, context): pass
def handle_usdt_wallet(update, context): pass
def handle_settings_menu(update, context): pass
def handle_mobile_input(update, context): pass
def handle_finder_mobile(update, context): pass
def handle_finder_country(update, context): pass
def handle_stats_menu(update, context): pass
def handle_unsolved_countries(update, context): pass
def handle_case_details(update, context): pass
def handle_edit_field(update, context): pass
def handle_transfer(update, context): pass
def handle_private_key(update, context): pass
def handle_action(update, context): pass
def handle_wallet(update, context): pass
def handle_settings(update, context): pass