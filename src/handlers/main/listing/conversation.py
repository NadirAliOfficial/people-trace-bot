from handlers.listing_handler import (
    advertiser_wallet_name_handler,
    advertiser_wallet_selection_callback,
    advertiser_wallet_type_callback,
    approve_extend_callback,
    ask_reward_amount,
    back_to_listing_callback,
    cancel_delete_callback,
    cancel_edit_callback,
    cancel_extend_callback,
    cancel_reward,
    case_details_callback,
    confirm_extend_callback,
    confirm_reward,
    delete_case_callback,
    edit_case_callback,
    edit_field_callback,
    extend_reward_callback,
    finder_details_callback,
    listing_command,
    listing_complaint_callback,
    pagination_callback,
    process_city,
    process_country,
    process_reward_transfer,
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



# listing_conv_handler = ConversationHandler(
#     entry_points=[CommandHandler("listing", listing_command)],
#     states={
#         State.CASE_DETAILS: [
#             # Case details and pagination
#             CallbackQueryHandler(case_details_callback, pattern="^case_.*$"),
#             CallbackQueryHandler(
#                 pagination_callback, pattern="^(page_previous|page_next)$"
#             ),
#             # Editing and deleting cases
#             CallbackQueryHandler(edit_field_callback, pattern="^edit_field_.*$"),
#             CallbackQueryHandler(edit_case_callback, pattern="^edit_.*$"),
#             CallbackQueryHandler(cancel_edit_callback, pattern="^cancel_edit$"),
#             CallbackQueryHandler(delete_case_callback, pattern="^delete_.*$"),
#             CallbackQueryHandler(cancel_delete_callback, pattern="^delete_cancel$"),
#             # Reward process
#             CallbackQueryHandler(
#                 reward_case_callback, pattern="^reward_.*$"
#             ),  # Show case & finders list
#             CallbackQueryHandler(
#                 finder_details_callback, pattern="^finder_details_.*$"
#             ),  # Show one finder details
#             CallbackQueryHandler(
#                 ask_reward_amount, pattern="^send_reward_.*$"
#             ),  # Ask for reward amount
#             # Extend Reward Handlers
#             CallbackQueryHandler(extend_reward_callback, pattern=r"^extend_reward_"),
#         ],
#         State.ENTER_COUNTRY: [
#             MessageHandler(filters.TEXT & ~filters.COMMAND, process_country),
#         ],
#         State.ENTER_CITY: [
#             MessageHandler(filters.TEXT & ~filters.COMMAND, process_city),
#         ],
#         State.EDIT_FIELD: [
#             MessageHandler(filters.TEXT & ~filters.COMMAND, update_case_field),
#         ],
#         # State.CONFIRM_EXTEND: [
#         #     CallbackQueryHandler(cancel_extend_callback, pattern=r"^cancel_extend$"),
#         # ],
#         # For the Extend Reward
#         State.CONFIRM_EXTEND: [
#             CallbackQueryHandler(approve_extend_callback, pattern=r"^approve_extend_"),
#             CallbackQueryHandler(confirm_extend_callback, pattern=r"^confirm_extend_"),
#             CallbackQueryHandler(cancel_extend_callback, pattern=r"^cancel_extend$"),
#         ],
#         State.SELECT_WALLET_FOR_EXTEND: [
#             CallbackQueryHandler(select_wallet_callback, pattern=r"^select_wallet_"),
#         ],
#         State.REWARD_TRANSFER_PROCESS: [
#             MessageHandler(filters.TEXT & ~filters.COMMAND, process_reward_transfer),
#         ],
#         State.CHOOSE_COUNTRY: [
#             CallbackQueryHandler(
#                 country_callback, pattern="^(country_select_|country_page_)"
#             ),
#             MessageHandler(filters.TEXT & ~filters.COMMAND, update_choose_country),
#         ],
#         State.CHOOSE_CITY: [
#             CallbackQueryHandler(city_callback, pattern="^(city_select_|city_page_)"),
#             MessageHandler(filters.TEXT & ~filters.COMMAND, choose_city),
#         ],
#         State.CONFIRM_REWARD: [
#             CallbackQueryHandler(confirm_reward, pattern="^confirm_reward$"),
#             CallbackQueryHandler(cancel_reward, pattern="^cancel_reward$"),
#         ],
#         # Advertiser to Extend the reward demanded by the finder
#         State.CHOOSE_WALLET_TYPE: [
#             CallbackQueryHandler(
#                 advertiser_wallet_type_callback, pattern="^(SOL|USDT)$"
#             ),
#             CallbackQueryHandler(
#                 advertiser_wallet_selection_callback, pattern="^wallet_"
#             ),
#             CallbackQueryHandler(
#                 advertiser_wallet_name_handler, pattern="^create_new_wallet$"
#             ),  # Handle create_new_wallet
#         ],
#         State.NAME_WALLET: [
#             MessageHandler(
#                 filters.TEXT & ~filters.COMMAND, advertiser_wallet_name_handler
#             ),
#         ],
#     },
#     fallbacks=[
#         CommandHandler("cancel", cancel),
#     ],
#     allow_reentry=True,
# )



listing_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("listing", listing_command)],
    states={
         State.LISTING.VIEW_COMPLAINTS: [
            CallbackQueryHandler(
                listing_complaint_callback,
                pattern="^(complaint_next_|complaint_back_|lead_|reward_)",
            )
        ],
        
        State.CASE_DETAILS: [
            CallbackQueryHandler(case_details_callback, pattern=r"^case_.*$"),
            CallbackQueryHandler(pagination_callback, pattern=r"^(page_previous|page_next)$"),
            CallbackQueryHandler(back_to_listing_callback, pattern=r"^back_to_listing$"),

            # Reward Flow
            CallbackQueryHandler(reward_case_callback, pattern=r"^reward_.*$"),
            CallbackQueryHandler(finder_details_callback, pattern=r"^finder_details_.*$"),

            # Extend Flow
            CallbackQueryHandler(extend_reward_callback, pattern=r"^extend_reward_.*$"),

            # Edit/Delete (existing handlers remain untouched)
            CallbackQueryHandler(edit_case_callback, pattern=r"^edit_.*$"),
            CallbackQueryHandler(delete_case_callback, pattern=r"^delete_.*$"),
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
            MessageHandler(filters.TEXT & ~filters.COMMAND, update_case_field),
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