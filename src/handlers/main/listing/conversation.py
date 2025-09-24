from handlers.listing_handler import (
    advertiser_wallet_name_handler,
    advertiser_wallet_selection_callback,
    advertiser_wallet_type_callback,
    approve_extend_callback,
    ask_reward_amount,
    back_to_case_callback,
    cancel_delete_callback,
    cancel_edit_callback,
    cancel_extend_callback,
    cancel_reward,
    confirm_extend_callback,
    confirm_reward,
    delete_case_callback,
    edit_field_callback,
    extend_reward_callback,
    # finder_details_callback,
    finder_detail_navigation_callback,
    finder_navigation_callback,
    listing_command,
    listing_complaint_callback,
    process_city,
    process_country,
    process_province,
    process_mobile_number,
    verify_mobile_otp,
    cancel_mobile_edit_callback,
    process_reward_transfer,
    refresh_wallet_balances_callback,
    # reward_case_callback,
    select_wallet_callback,
    update_case_field,
    update_choose_country,
    view_finder_callback,
    view_finder_proof_callback,
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
    entry_points=[CommandHandler("listing", listing_command)],  # In Use
    states={
        State.LISTING.VIEW_COMPLAINTS: [
            CallbackQueryHandler(
                listing_complaint_callback,
                pattern="^(complaint_next_|complaint_back_|edit_|delete_|view_finder_)",
            ),
        ],  # In Use
        State.LISTING.VIEW_FINDERS: [
            CallbackQueryHandler(
                finder_navigation_callback,
                pattern=r"^(finder_next_|finder_prev_|send_reward_|extend_reward_|view_proof_|back_to_case_)",
            ),
        ],
        State.LISTING.EDIT_FIELD_SELECTION: [
            CallbackQueryHandler(edit_field_callback, pattern="^edit_field_.*$"),
            CallbackQueryHandler(cancel_edit_callback, pattern=r"^cancel_edit$"),
        ],
        State.CASE_DETAILS: [
            # Reward Flow
            CallbackQueryHandler(view_finder_callback, pattern=r"^view_finder_.*$"),
            # CallbackQueryHandler(reward_case_callback, pattern=r"^reward_.*$"),
            #
            # CallbackQueryHandler(finder_details_callback, pattern=r"^finder_details_.*$"),
            # CallbackQueryHandler(finder_navigation_callback, pattern=r"^(finder_next_|finder_back_).*$"),
            # CallbackQueryHandler(finder_detail_navigation_callback, pattern=r"^(finder_next_|finder_prev_).*$"),
            # CallbackQueryHandler(view_finder_proof_callback, pattern=r"^view_proof_.*$"),
            # CallbackQueryHandler(back_to_case_callback, pattern=r"^back_to_case_.*$"),
            # # Extend Flow
            # CallbackQueryHandler(extend_reward_callback, pattern=r"^extend_reward_.*$"),
            # //Note: Edit the complaint by same user functionality checked
            CallbackQueryHandler(
                edit_field_callback, pattern="^edit_field_.*$"
            ),  # In Use
            CallbackQueryHandler(cancel_edit_callback, pattern=r"^cancel_edit$"),
            # //NOTE: Delete the complaint by same user functionality checked
            CallbackQueryHandler(delete_case_callback, pattern=r"^confirm_delete$"),
            CallbackQueryHandler(cancel_delete_callback, pattern=r"^delete_cancel$"),
        ],
        # # SECTION: EDIT FIELD
        State.EDIT_FIELD: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, update_case_field
            ),  # In Use
        ],
        # State.ENTER_COUNTRY: [
        #     MessageHandler(filters.TEXT & ~filters.COMMAND, process_country),
        # ],
        # State.ENTER_PROVINCE: [
        #     MessageHandler(filters.TEXT & ~filters.COMMAND, process_province),
        # ],
        # State.ENTER_CITY: [
        #     MessageHandler(filters.TEXT & ~filters.COMMAND, process_city),
        # ],
        # State.ENTER_MOBILE_NUMBER: [
        #     MessageHandler(filters.TEXT & ~filters.COMMAND, process_mobile_number),
        # ],
        # State.VERIFY_MOBILE_OTP: [
        #     MessageHandler(filters.TEXT & ~filters.COMMAND, verify_mobile_otp),
        #     CallbackQueryHandler(cancel_mobile_edit_callback, pattern=r"^cancel_mobile_edit$"),
        # ],
        # State.CONFIRM_EXTEND: [
        #     CallbackQueryHandler(approve_extend_callback, pattern=r"^approve_extend_.*$"),
        #     CallbackQueryHandler(cancel_extend_callback, pattern=r"^cancel_extend$"),
        # ],
        # State.SELECT_WALLET_FOR_EXTEND: [
        #     CallbackQueryHandler(select_wallet_callback, pattern=r"^select_wallet_.*$"),
        # ],
        State.REWARD_TRANSFER_PROCESS: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, process_reward_transfer),
        ],
        State.CONFIRM_REWARD: [
            CallbackQueryHandler(confirm_reward, pattern=r"^confirm_reward$"),
            CallbackQueryHandler(cancel_reward, pattern=r"^cancel_reward$"),
        ],
        # State.CHOOSE_WALLET_TYPE: [
        #     CallbackQueryHandler(advertiser_wallet_type_callback, pattern=r"^(SOL|USDT)$"),
        #     CallbackQueryHandler(advertiser_wallet_selection_callback, pattern=r"^wallet_.*$"),
        #     CallbackQueryHandler(advertiser_wallet_name_handler, pattern=r"^create_new_wallet$"),
        #     CallbackQueryHandler(refresh_wallet_balances_callback, pattern=r"^refresh_wallet_balances$"),
        # ],
        # State.NAME_WALLET: [
        #     MessageHandler(filters.TEXT & ~filters.COMMAND, advertiser_wallet_name_handler),
        # ],
        # State.CHOOSE_COUNTRY: [
        #     CallbackQueryHandler(country_callback, pattern=r"^(country_select_|country_page_)"),
        #     MessageHandler(filters.TEXT & ~filters.COMMAND, update_choose_country),
        # ],
        # State.CHOOSE_CITY: [
        #     CallbackQueryHandler(city_callback, pattern=r"^(city_select_|city_page_)"),
        #     MessageHandler(filters.TEXT & ~filters.COMMAND, choose_city),
        # ],
    },
    fallbacks=[
        CommandHandler("cancel", cancel),
    ],
    allow_reentry=True,
)
