from handlers.listing_handler import (
    advertiser_wallet_name_handler,
    advertiser_wallet_selection_callback,
    advertiser_wallet_type_callback,
    approve_extend_callback,
    ask_reward_amount,
    cancel_delete_callback,
    cancel_edit_callback,
    cancel_extend_callback,
    cancel_reward,
    confirm_extend_callback,
    confirm_reward,
    delete_case_callback,
    edit_field_callback,
    extend_reward_callback,
    finder_details_callback,
    listing_command,
    listing_complaint_callback,
    process_city,
    process_country,
    process_reward_transfer,
    refresh_wallet_balances_callback,
    reward_case_callback,
    select_wallet_callback,
    update_case_field,
    update_choose_country,
)
from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    filters,
)
from constants import State
from handlers.start_handler import (
    choose_city,
    city_callback,
    country_callback,
    cancel,
)

listing_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("listing", listing_command)], # In Use
    states={
         State.LISTING.VIEW_COMPLAINTS: [
            CallbackQueryHandler(
                listing_complaint_callback,
                pattern="^(complaint_next_|complaint_back_|edit_|delete_)",
            ),
        ], # In Use
        State.CASE_DETAILS: [
        
            # Reward Flow
            CallbackQueryHandler(reward_case_callback, pattern=r"^reward_.*$"),
            CallbackQueryHandler(finder_details_callback, pattern=r"^finder_details_.*$"),

            # Extend Flow
            CallbackQueryHandler(extend_reward_callback, pattern=r"^extend_reward_.*$"),

            # Edit/Delete (existing handlers remain untouched)
   
            CallbackQueryHandler(edit_field_callback, pattern="^edit_field_.*$"), # In Use
            CallbackQueryHandler(delete_case_callback, pattern=r"^confirm_delete$"),
            CallbackQueryHandler(cancel_edit_callback, pattern=r"^cancel_edit$"),
            CallbackQueryHandler(cancel_delete_callback, pattern=r"^delete_cancel$"),
        ],
        State.ENTER_COUNTRY: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, process_country),
        ],
        State.ENTER_CITY: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, process_city),
        ],
        State.EDIT_FIELD: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, update_case_field), # In Use
        ],
        State.CONFIRM_EXTEND: [
            CallbackQueryHandler(approve_extend_callback, pattern=r"^approve_extend_.*$"),
            CallbackQueryHandler(cancel_extend_callback, pattern=r"^cancel_extend$"),
        ],
        State.SELECT_WALLET_FOR_EXTEND: [
            CallbackQueryHandler(select_wallet_callback, pattern=r"^select_wallet_.*$"),
        ],
        State.REWARD_TRANSFER_PROCESS: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, process_reward_transfer),
        ],
        State.CONFIRM_REWARD: [
            CallbackQueryHandler(confirm_reward, pattern=r"^confirm_reward$"),
            CallbackQueryHandler(cancel_reward, pattern=r"^cancel_reward$"),
        ],
        State.CHOOSE_WALLET_TYPE: [
            CallbackQueryHandler(advertiser_wallet_type_callback, pattern=r"^(SOL|USDT)$"),
            CallbackQueryHandler(advertiser_wallet_selection_callback, pattern=r"^wallet_.*$"),
            CallbackQueryHandler(advertiser_wallet_name_handler, pattern=r"^create_new_wallet$"),
            CallbackQueryHandler(refresh_wallet_balances_callback, pattern=r"^refresh_wallet_balances$"),
        ],
        State.NAME_WALLET: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, advertiser_wallet_name_handler),
        ],
        State.CHOOSE_COUNTRY: [
            CallbackQueryHandler(country_callback, pattern=r"^(country_select_|country_page_)"),
            MessageHandler(filters.TEXT & ~filters.COMMAND, update_choose_country),
        ],
        State.CHOOSE_CITY: [
            CallbackQueryHandler(city_callback, pattern=r"^(city_select_|city_page_)"),
            MessageHandler(filters.TEXT & ~filters.COMMAND, choose_city),
        ],
    },
    fallbacks=[
        CommandHandler("cancel", cancel),
    ],
    allow_reentry=True,
)