from handlers.case_handler import (
    create_case_disclaimer_2_callback,
    handle_age,
    handle_ask_reward_amount,
    handle_back_to_reason,
    handle_continue_with_reward,
    handle_distinctive_features,
    handle_eye_color,
    handle_hair_color,
    handle_height,
    handle_last_seen_location,
    handle_person_name,
    handle_photo,
    handle_reason_for_finding,
    handle_refresh_balance,
    handle_relationship,
    handle_sex,
    handle_transfer_confirmation,
    handle_weight,
)
from handlers.start_finder_number_handler import (
    finder_disclaimer_callback,
    handle_finder_new_mobile,
    handle_finder_select_mobile,
    handle_finder_tac,
)
from handlers.start_number_handler import (
    handle_new_mobile,
    handle_select_mobile,
    handle_tac,
)
from handlers.finder_handler import (
    finder_choose_country,
    finder_choose_province,
    finder_complaint_callback,
    finder_country_callback,
    finder_handle_transaction_confirmation,
    finder_province_callback,
    finder_wallet_name_handler,
    finder_wallet_selection_callback,
    finder_wallet_type_callback,
    handle_advertiser_response,
    handle_confirm_found,
    handle_enter_location,
    handle_extend_reward,
    handle_extend_reward_amount,
    handle_pagination,
    show_advertisements,
    case_details,
    handle_proof,
    handle_found_case,
)
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
    case_details_callback,
    confirm_extend_callback,
    confirm_reward,
    delete_case_callback,
    edit_case_callback,
    edit_field_callback,
    extend_reward_callback,
    finder_details_callback,
    listing_command,
    pagination_callback,
    process_city,
    process_country,
    process_reward_transfer,
    reward_case_callback,
    select_wallet_callback,
    update_case_field,
    update_choose_country,
)
from handlers.stats_handler import (
    back_to_stats,
    handle_local_province_city,
    invalid_selection,
    my_case_detail_callback,
    stats_command,
    stats_menu_callback,
    unsolved_country_callback,
    view_my_cases_callback,
)
from handlers.wallet_handler import (
    back_to_wallet_menu,
    cancel_delete_wallet,
    confirm_delete_wallet,
    create_wallet,
    delete_wallet,
    process_create_wallet,
    process_delete_wallet,
    refresh_wallets,
    request_private_key,
    select_wallet_type,
    show_address,
    show_private_key,
    show_sol_wallet_detail,
    show_specific_address,
    show_usdt_wallet_detail,
    sol_wallets,
    usdt_wallets,
    view_history,
    view_specific_history,
    wallet_command,
)
from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    filters,
)
import logging

# Import your text-getting function and other constants
from constants import State
from states import StartState, WalletState, SettingsState, FinderState
from constant.language_constant import get_text
from handlers.settings_handler import (
    handle_setting_mobile,
    handle_setting_tac,
    settings_command,
    settings_menu_callback,
)
from handlers.start_handler import (
    action_callback,
    choose_city,
    city_callback,
    interrupt_current_flow,
    message_router,
    start,
    select_lang_callback,
    choose_country,
    country_callback,
    disclaimer_callback,
    cancel,
    start_choose_province,
    start_province_callback,
)
from handlers.start_wallet_handler import (
    wallet_name_handler,
    wallet_pagination_handler,
    wallet_selection_callback,
    wallet_type_callback,
    show_existing_wallets_handler,
)

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

start_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        #  ------------------ START HANDLER ------------------------------
        StartState.LANGUAGE_SELECTED: [
            CallbackQueryHandler(select_lang_callback, pattern="^lang_")
        ],
        StartState.CHOOSE_COUNTRY: [
            CallbackQueryHandler(
                country_callback, pattern="^(country_select_|country_page_)"
            ),
            MessageHandler(filters.TEXT & ~filters.COMMAND, choose_country),
        ],
        StartState.SHOW_DISCLAIMER: [
            CallbackQueryHandler(disclaimer_callback, pattern="^(agree|disagree)$")
        ],
        StartState.START_CHOOSE_PROVINCE: [
            CallbackQueryHandler(
                start_province_callback,
                pattern="^(start_province_select_|start_province_page_)",
            ),
            MessageHandler(filters.TEXT & ~filters.COMMAND, start_choose_province),
        ],
        StartState.CHOOSE_CITY: [
            CallbackQueryHandler(city_callback, pattern="^(city_select_|city_page_)"),
            MessageHandler(filters.TEXT & ~filters.COMMAND, choose_city),
        ],
        StartState.CHOOSE_ACTION: [
            CallbackQueryHandler(action_callback, pattern="^(advertise|find_people)$")
        ],
        # ------------------ START MOBILE NUMBER HANDLER ------------------------------
        StartState.CREATE_CASE_MOBILE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_new_mobile)
        ],
        StartState.MOBILE_MANAGEMENT: [
            CallbackQueryHandler(
                handle_select_mobile, pattern="^(select_mobile_.*|mobile_add)$"
            ),
        ],
        StartState.CREATE_CASE_TAC: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_tac)
        ],
        StartState.CHOOSE_OR_CREATE_WALLET: [
            CallbackQueryHandler(wallet_type_callback, pattern="^(USDT|SOL)$"),
            CallbackQueryHandler(wallet_name_handler, pattern="^create_new_wallet$"),
            CallbackQueryHandler(
                show_existing_wallets_handler, pattern="^use_existing_wallet$"
            ),
            CallbackQueryHandler(wallet_selection_callback, pattern="^wallet_"),
            CallbackQueryHandler(
                wallet_pagination_handler, pattern="^wallet_page_(next|prev)$"
            ),
        ],
        StartState.NAME_WALLET: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, wallet_name_handler),
        ],
        # Handle all of the button like create case , find people , settings , help
        StartState.HANDLE_REPLY: [
            CallbackQueryHandler(
                message_router, pattern="(create_case|find_people|settings|help)$"
            )
        ],
        StartState.CREATE_CASE_DISCLAIMER: [
            CallbackQueryHandler(
                create_case_disclaimer_2_callback, pattern="^(agree|disagree)$"
            )
        ],
        StartState.CREATE_CASE_PERSON_NAME: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_person_name)
        ],
        StartState.CREATE_CASE_RELATIONSHIP: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_relationship)
        ],
        StartState.CREATE_CASE_PHOTO: [MessageHandler(filters.PHOTO, handle_photo)],
        StartState.CREATE_CASE_LAST_SEEN_LOCATION: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_last_seen_location)
        ],
        StartState.CREATE_CASE_SEX: [CallbackQueryHandler(handle_sex)],
        StartState.CREATE_CASE_AGE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_age)
        ],
        StartState.CREATE_CASE_HAIR_COLOR: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_hair_color)
        ],
        StartState.CREATE_CASE_EYE_COLOR: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_eye_color)
        ],
        StartState.CREATE_CASE_HEIGHT: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_height)
        ],
        StartState.CREATE_CASE_WEIGHT: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_weight)
        ],
        StartState.CREATE_CASE_DISTINCTIVE_FEATURES: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_distinctive_features)
        ],
        StartState.CREATE_CASE_ASK_REASON: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_reason_for_finding)
        ],
        StartState.CREATE_CASE_ASK_REWARD: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_ask_reward_amount),
            CallbackQueryHandler(handle_refresh_balance, pattern="^refresh_balance:"),
            CallbackQueryHandler(handle_back_to_reason, pattern="^back_to_reason:"),
            CallbackQueryHandler(
                handle_continue_with_reward, pattern="^continue_with_reward:"
            ),
        ],
        StartState.CREATE_CASE_CONFIRM_TRANSFER: [
            CallbackQueryHandler(
                handle_transfer_confirmation,
                pattern="^(confirm_transfer|cancel_transfer)$",
            )
        ],
        StartState.CASE_LIST: [
            CallbackQueryHandler(show_advertisements, pattern=r"^page_(previous|next)"),
            CallbackQueryHandler(case_details, pattern=r"^case_"),
            CallbackQueryHandler(show_advertisements, pattern="^back_to_list"),
        ],
        StartState.CASE_DETAILS: [
            CallbackQueryHandler(handle_pagination, pattern="^case_page_"),
            CallbackQueryHandler(case_details, pattern="^case_"),
            CallbackQueryHandler(handle_found_case, pattern="^found_"),
            CallbackQueryHandler(show_advertisements, pattern="^back_to_list"),
        ],
        StartState.UPLOAD_PROOF: [
            MessageHandler(filters.PHOTO | filters.VIDEO, handle_proof)
        ],
        StartState.ENTER_LOCATION: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_enter_location)
        ],
        StartState.EXTEND_REWARD: [
            CallbackQueryHandler(
                handle_extend_reward, pattern="^(yes_extend|no_extend)$"
            )
        ],
        StartState.FINDER_CHOOSE_WALLET_TYPE: [
            CallbackQueryHandler(finder_wallet_type_callback, pattern="^(SOL|USDT)$"),
            CallbackQueryHandler(finder_wallet_selection_callback, pattern="^wallet_"),
            CallbackQueryHandler(
                finder_wallet_name_handler, pattern="^create_new_wallet$"
            ),  # Handle create_new_wallet
        ],
        StartState.FINDER_NAME_WALLET: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, finder_wallet_name_handler),
        ],
        StartState.FINDER_CONFIRM_TRANSACTION: [
            CallbackQueryHandler(
                finder_handle_transaction_confirmation,
                pattern="^(confirm_transfer|cancel_transfer)$",
            )
        ],
        StartState.TRANSFER_CONFIRMATION: [
            CallbackQueryHandler(
                handle_transfer_confirmation,
                pattern="^(confirm_transfer|cancel_transfer)$",
            )
        ],
        StartState.CONFIRM_FOUND: [
            CallbackQueryHandler(
                handle_confirm_found, pattern="^(confirm_found|cancel_found)$"
            )
        ],
        StartState.EXTEND_REWARD_AMOUNT: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_extend_reward_amount)
        ],
        StartState.ADVERTISER_RESPONSE: [
            CallbackQueryHandler(
                handle_advertiser_response, pattern="^(accept_extend|reject_extend)$"
            )
        ],
        # ---------------------- Settings Start ---------------------
        SettingsState.SETTINGS_MENU: [
            CallbackQueryHandler(
                settings_menu_callback,
                pattern="^(settings_language|settings_mobile|settings_close|setlang_)",
            ),
        ],
        SettingsState.WAITING_FOR_MOBILE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_setting_mobile),
        ],
        SettingsState.SETTINGS_MOBILE_MANAGEMENT: [
            CallbackQueryHandler(settings_menu_callback, pattern="^(mobile_|remove_)"),
        ],
        SettingsState.MOBILE_VERIFICATION: [
            CallbackQueryHandler(
                settings_menu_callback, pattern="^(remove_|settings_mobile)"
            ),
        ],
        SettingsState.SETTINGS_CREATE_CASE_TAC: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_setting_tac),
        ],
        # ---------------------- Settings End ---------------------
        StartState.END: [CommandHandler("start", start)],
        # FINDER FUNCTIONALITY (FINDER)
        FinderState.CREATE_CASE_MOBILE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_finder_new_mobile)
        ],
        FinderState.MOBILE_MANAGEMENT: [
            CallbackQueryHandler(
                handle_finder_select_mobile, pattern="^(select_mobile_.*|mobile_add)$"
            ),
        ],
        FinderState.CREATE_CASE_TAC: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_finder_tac)
        ],
        FinderState.FINDER_DISCLAIMER: [
            CallbackQueryHandler(
                finder_disclaimer_callback, pattern="^(agree|disagree)$"
            )
        ],
        FinderState.CHOOSE_COUNTRY: [
            CallbackQueryHandler(
                finder_country_callback, pattern="^(country_select_|country_page_)"
            ),
            MessageHandler(filters.TEXT & ~filters.COMMAND, finder_choose_country),
        ],
        FinderState.CHOOSE_PROVINCE: [
            CallbackQueryHandler(
                finder_province_callback,
                pattern="^(province_select_|province_page_)",
            ),
            MessageHandler(filters.TEXT & ~filters.COMMAND, finder_choose_province),
        ],
        FinderState.VIEW_COMPLAINTS: [
            CallbackQueryHandler(
                finder_complaint_callback,
                pattern="^(complaint_next_|complaint_back_|lead_|reward_)",
            )
        ],
    },
    fallbacks=[
        CommandHandler("cancel", cancel),
        CommandHandler("settings", settings_command),
    ],
    allow_reentry=True,
    name="wallet",
)


# ---------------------- Wallet Conversation Handler End  ---------------------
# Define conversation handler
wallet_handler = ConversationHandler(
    entry_points=[CommandHandler("wallets", wallet_command)],
    states={
        WalletState.WALLET_MENU: [
            CallbackQueryHandler(refresh_wallets, pattern="^refresh_wallets$"),
            CallbackQueryHandler(sol_wallets, pattern="^sol_wallets$"),
            CallbackQueryHandler(usdt_wallets, pattern="^usdt_wallets$"),
            CallbackQueryHandler(show_address, pattern="^show_address$"),
            CallbackQueryHandler(view_history, pattern="^view_history$"),
            CallbackQueryHandler(create_wallet, pattern="^create_wallet$"),
            CallbackQueryHandler(delete_wallet, pattern="^delete_wallet$"),
            CallbackQueryHandler(
                back_to_wallet_menu, pattern="^back_to_wallet_menu$"
            ),  # TESTED
        ],
        WalletState.SOL_WALLET_DETAIL: [
            CallbackQueryHandler(show_sol_wallet_detail, pattern="^sol_detail_"),
            CallbackQueryHandler(back_to_wallet_menu, pattern="^back_to_wallet_menu$"),
        ],
        WalletState.SOL_WALLET_ACTIONS: [
            CallbackQueryHandler(request_private_key, pattern="^req_pk_"),
            CallbackQueryHandler(back_to_wallet_menu, pattern="^back_to_wallet_menu$"),
        ],
        WalletState.USDT_WALLET_DETAIL: [
            CallbackQueryHandler(show_usdt_wallet_detail, pattern="^usdt_detail_"),
            CallbackQueryHandler(back_to_wallet_menu, pattern="^back_to_wallet_menu$"),
        ],
        WalletState.USDT_WALLET_ACTIONS: [
            CallbackQueryHandler(request_private_key, pattern="^req_pk_"),
            CallbackQueryHandler(back_to_wallet_menu, pattern="^back_to_wallet_menu$"),
        ],
        WalletState.CONFIRM_PRIVATE_KEY: [
            CallbackQueryHandler(show_private_key, pattern="^(confirm_pk|cancel_pk)$"),
            CallbackQueryHandler(back_to_wallet_menu, pattern="^back_to_wallet_menu$"),
        ],
        WalletState.SHOW_ADDRESS: [
            CallbackQueryHandler(show_specific_address, pattern="^show_address_"),
            CallbackQueryHandler(back_to_wallet_menu, pattern="^back_to_wallet_menu$"),
        ],
        WalletState.VIEW_HISTORY: [
            CallbackQueryHandler(view_specific_history, pattern="^view_history_"),
            CallbackQueryHandler(back_to_wallet_menu, pattern="^back_to_wallet_menu$"),
        ],
        WalletState.SELECT_WALLET_TYPE: [
            CallbackQueryHandler(
                select_wallet_type, pattern="^(USDT|SOL)$"
            ),  # Handle wallet type selection
        ],
        WalletState.ENTER_WALLET_NAME: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, process_create_wallet
            ),  # Handle wallet name input
        ],
        WalletState.CONFIRM_DELETE_WALLET: [
            CallbackQueryHandler(
                confirm_delete_wallet, pattern="^confirm_delete_wallet_"
            ),
        ],
        WalletState.DELETE_WALLET: [
            CallbackQueryHandler(process_delete_wallet, pattern="^delete_wallet_"),
            CallbackQueryHandler(cancel_delete_wallet, pattern="^cancel_delete_wallet"),
        ],
        WalletState.END: [CommandHandler("wallet", wallet_command)],
    },
    fallbacks=[
        CommandHandler("cancel", cancel),
    ],
    allow_reentry=True,
)
# ---------------------- Wallet Conversation Handler End  ---------------------


# ---------------------- Settings Conversation Handler Start  ---------------------
settings_handler = ConversationHandler(
    entry_points=[CommandHandler("settings", settings_command)],
    states={
        SettingsState.SETTINGS_MENU: [
            CallbackQueryHandler(
                settings_menu_callback,
                pattern="^(settings_language|settings_mobile|settings_close|setlang_)",
            ),
        ],
        SettingsState.WAITING_FOR_MOBILE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_setting_mobile),
        ],
        SettingsState.SETTINGS_MOBILE_MANAGEMENT: [
            CallbackQueryHandler(settings_menu_callback, pattern="^(mobile_|remove_)"),
        ],
        SettingsState.MOBILE_VERIFICATION: [
            CallbackQueryHandler(
                settings_menu_callback, pattern="^(remove_|settings_mobile)"
            ),
        ],
        SettingsState.SETTINGS_CREATE_CASE_TAC: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_setting_tac),
        ],
        SettingsState.END: [CommandHandler("settings", settings_command)],
    },
    fallbacks=[
        CommandHandler("cancel", cancel),
    ],
    allow_reentry=True,
)
# ---------------------- Settings Conversation Handler End  ---------------------