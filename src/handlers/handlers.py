from handlers.case_handler import (
    create_case_disclaimer_2_callback,
    handle_age,
    handle_ask_reward_amount,
    handle_back_to_menu,
    handle_back_to_reason,
    handle_cancel_case,
    handle_cancel_case_selection,
    handle_cancel_published_case,
    handle_cancel_reason,
    handle_continue_with_reward,
    handle_custom_cancel_reason,
    handle_distinctive_features,
    handle_edit_case,
    handle_edit_published_case,
    handle_eye_color,
    handle_hair_color,
    handle_height,
    handle_increase_reward,
    handle_last_seen_location,
    handle_person_name,
    handle_photo,
    handle_reason_for_finding,
    handle_refresh_balance,
    handle_relationship,
    handle_sex,
    handle_publish_case,
    handle_submit_case,
    handle_weight,
)
from handlers.settings_handler import handle_setting_mobile, handle_setting_tac, settings_command, settings_menu_callback
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
    handle_proof,
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
from handlers.main.main_wallets_handler import wallet_handler
from handlers.main.main_listing_handler import listing_handler
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
from constant.language_constant import get_text
from handlers.main.main_settings_handler import settings_handler
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
        State.LANGUAGE_SELECTED: [
            CallbackQueryHandler(select_lang_callback, pattern="^lang_")
        ],
        State.CHOOSE_COUNTRY: [
            CallbackQueryHandler(
                country_callback, pattern="^(country_select_|country_page_)"
            ),
            MessageHandler(filters.TEXT & ~filters.COMMAND, choose_country),
        ],
        State.SHOW_DISCLAIMER: [
            CallbackQueryHandler(disclaimer_callback, pattern="^(agree|disagree)$")
        ],
        State.START_CHOOSE_PROVINCE: [
            CallbackQueryHandler(
                start_province_callback,
                pattern="^(start_province_select_|start_province_page_)",
            ),
            MessageHandler(filters.TEXT & ~filters.COMMAND, start_choose_province),
        ],
        State.CHOOSE_CITY: [
            CallbackQueryHandler(city_callback, pattern="^(city_select_|city_page_)"),
            MessageHandler(filters.TEXT & ~filters.COMMAND, choose_city),
        ],
        State.CHOOSE_ACTION: [
            CallbackQueryHandler(action_callback, pattern="^(advertise|find_people)$")
        ],
        # ------------------ START MOBILE NUMBER HANDLER ------------------------------
        State.CREATE_CASE_MOBILE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_new_mobile)
        ],
        State.MOBILE_MANAGEMENT: [
            CallbackQueryHandler(
                handle_select_mobile, pattern="^(select_mobile_.*|mobile_add)$"
            ),
        ],
        State.CREATE_CASE_TAC: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_tac)
        ],
        State.CHOOSE_OR_CREATE_WALLET: [
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
        State.NAME_WALLET: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, wallet_name_handler),
        ],
        # Handle all of the button like create case , find people , settings , help
        State.HANDLE_REPLY: [
            CallbackQueryHandler(
                message_router, pattern="(create_case|find_people|settings|help)$"
            )
        ],
        State.CREATE_CASE_DISCLAIMER: [
            CallbackQueryHandler(
                create_case_disclaimer_2_callback, pattern="^(agree|disagree)$"
            )
        ],
        State.CREATE_CASE_PERSON_NAME: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_person_name)
        ],
        State.CREATE_CASE_RELATIONSHIP: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_relationship)
        ],
        State.CREATE_CASE_PHOTO: [MessageHandler(filters.PHOTO, handle_photo)],
        State.CREATE_CASE_LAST_SEEN_LOCATION: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_last_seen_location)
        ],
        State.CREATE_CASE_SEX: [CallbackQueryHandler(handle_sex)],
        State.CREATE_CASE_AGE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_age)
        ],
        State.CREATE_CASE_HAIR_COLOR: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_hair_color)
        ],
        State.CREATE_CASE_EYE_COLOR: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_eye_color)
        ],
        State.CREATE_CASE_HEIGHT: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_height)
        ],
        State.CREATE_CASE_WEIGHT: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_weight)
        ],
        State.CREATE_CASE_DISTINCTIVE_FEATURES: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_distinctive_features)
        ],
        State.CREATE_CASE_ASK_REASON: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_reason_for_finding)
        ],
        ##SECTION -  Ask For the reward and handle various cases
        State.CREATE_CASE_ASK_REWARD: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_ask_reward_amount),
            CallbackQueryHandler(handle_refresh_balance, pattern="^refresh_balance:"),
            CallbackQueryHandler(handle_back_to_reason, pattern="^back_to_reason:"),
            CallbackQueryHandler(
                handle_continue_with_reward, pattern="^continue_with_reward:"
            ),
            CallbackQueryHandler(handle_increase_reward, pattern="^increase_reward$"),
            CallbackQueryHandler(handle_submit_case, pattern="^submit_case$"),
            CallbackQueryHandler(handle_edit_case, pattern="^edit_case$"),
            CallbackQueryHandler(handle_cancel_case_selection, pattern="^cancel_case$"),
        ],
        ##!SECTION -  Handle Links  -  to transfer or cancel case 
        State.CREATE_CASE_CONFIRM_TRANSFER: [
            CallbackQueryHandler(handle_submit_case, pattern="^submit_case$"),
            CallbackQueryHandler(handle_edit_case, pattern="^edit_case$"),
            CallbackQueryHandler(handle_cancel_case, pattern="^cancel_case$"),
        ],
        ##!SECTION -  Handle Links  -  to transfer or cancel case
        State.CASE_CANCEL_SELECT_REASON: [
            CallbackQueryHandler(handle_cancel_reason, pattern="^cancel_reason:"),
        ],
        State.CASE_CANCEL_ENTER_REASON: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, handle_custom_cancel_reason
            ),
        ],
        ##!SECTION - After Published Show the detail what to edit / cancel / back to the menu 
        State.POST_SUBMISSION_MENU: [
            CallbackQueryHandler(handle_edit_published_case, pattern="^edit_published_case$"),
            CallbackQueryHandler(handle_cancel_published_case, pattern="^cancel_published_case$"),
            CallbackQueryHandler(handle_back_to_menu, pattern="^back_to_menu$"),
        ],
        
        
        ##SECTION -   Finder
        State.FINDER.CREATE_CASE_MOBILE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_finder_new_mobile)
        ],
        State.FINDER.MOBILE_MANAGEMENT: [
            CallbackQueryHandler(
                handle_finder_select_mobile, pattern="^(select_mobile_.*|mobile_add)$"
            ),
        ],
        State.FINDER.CREATE_CASE_TAC: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_finder_tac)
        ],
        State.FINDER.FINDER_DISCLAIMER: [
            CallbackQueryHandler(
                finder_disclaimer_callback, pattern="^(agree|disagree)$"
            )
        ],
        State.FINDER.CHOOSE_COUNTRY: [
            CallbackQueryHandler(
                finder_country_callback, pattern="^(country_select_|country_page_)"
            ),
            MessageHandler(filters.TEXT & ~filters.COMMAND, finder_choose_country),
        ],
        State.FINDER.CHOOSE_PROVINCE: [
            CallbackQueryHandler(
                finder_province_callback,
                pattern="^(province_select_|province_page_)",
            ),
            MessageHandler(filters.TEXT & ~filters.COMMAND, finder_choose_province),
        ],
        State.FINDER.VIEW_COMPLAINTS: [
            CallbackQueryHandler(
                finder_complaint_callback,
                pattern="^(complaint_next_|complaint_back_|lead_|reward_)",
            )
        ],
        
        State.UPLOAD_PROOF: [
            MessageHandler(filters.PHOTO | filters.VIDEO, handle_proof)
        ],
        State.ENTER_LOCATION: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_enter_location)
        ],
        
        
        ## TODO: WOrking on it
        State.FINDER_CHOOSE_WALLET_TYPE: [
            CallbackQueryHandler(finder_wallet_type_callback, pattern="^(SOL|USDT)$"),
            CallbackQueryHandler(finder_wallet_selection_callback, pattern="^wallet_"),
            CallbackQueryHandler(
                finder_wallet_name_handler, pattern="^create_new_wallet$"
            ),  # Handle create_new_wallet
        ],
        State.FINDER_NAME_WALLET: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, finder_wallet_name_handler),
        ],

        

        State.EXTEND_REWARD: [
            CallbackQueryHandler(
                handle_extend_reward, pattern="^(yes_extend|no_extend)$"
            )
        ],
    
        State.FINDER_CONFIRM_TRANSACTION: [
            CallbackQueryHandler(
                finder_handle_transaction_confirmation,
                pattern="^(confirm_transfer|cancel_transfer)$",
            )
        ],
        State.TRANSFER_CONFIRMATION: [
            CallbackQueryHandler(
                handle_publish_case,
                pattern="^(confirm_transfer|cancel_transfer)$",
            )
        ],
        State.CONFIRM_FOUND: [
            CallbackQueryHandler(
                handle_confirm_found, pattern="^(confirm_found|cancel_found)$"
            )
        ],
        State.EXTEND_REWARD_AMOUNT: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_extend_reward_amount)
        ],
        State.ADVERTISER_RESPONSE: [
            CallbackQueryHandler(
                handle_advertiser_response, pattern="^(accept_extend|reject_extend)$"
            )
        ],
        # ---------------------- Settings Start ---------------------
        State.SETTINGS.SETTINGS_MENU: [
            CallbackQueryHandler(
                settings_menu_callback,
                pattern="^(settings_language|settings_mobile|settings_close|setlang_)",
            ),
        ],
        State.SETTINGS.WAITING_FOR_MOBILE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_setting_mobile),
        ],
        State.SETTINGS.SETTINGS_MOBILE_MANAGEMENT: [
            CallbackQueryHandler(settings_menu_callback, pattern="^(mobile_|remove_)"),
        ],
        State.SETTINGS.MOBILE_VERIFICATION: [
            CallbackQueryHandler(
                settings_menu_callback, pattern="^(remove_|settings_mobile)"
            ),
        ],
        State.SETTINGS.SETTINGS_CREATE_CASE_TAC: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_setting_tac),
        ],
        # ---------------------- Settings End ---------------------
        State.END: [CommandHandler("start", start)],
        # FINDER FUNCTIONALITY (FINDER)
        
    },
    fallbacks=[
        CommandHandler("cancel", cancel),
        CommandHandler("settings", settings_command),
    ],
    allow_reentry=True,
    name="wallet",
)


# ---------------------- Wallet Conversation Handler End  ---------------------

# ---------------------- Listing Conversation Handler Start  ---------------------

# # handlers/stats_handler.py

stats_handler = ConversationHandler(
    entry_points=[CommandHandler("stats", stats_command)],
    states={
        State.STATS.SHOW_STATS_MENU: [
            CallbackQueryHandler(stats_menu_callback, pattern="^(view_unsolved|view_local_stats|view_my_cases|back_to_main_menu)$"),
            CallbackQueryHandler(back_to_stats, pattern="^back_to_stats$"),
        ],
        State.STATS.SHOW_UNSOLVED_COUNTRIES: [
            CallbackQueryHandler(unsolved_country_callback, pattern="^country_"),
            CallbackQueryHandler(back_to_stats, pattern="^back_to_stats$"),
        ],
        State.STATS.SHOW_MY_CASES: [
            CallbackQueryHandler(my_case_detail_callback, pattern="^mycase_"),
            CallbackQueryHandler(view_my_cases_callback, pattern="^view_my_cases$"),
            CallbackQueryHandler(back_to_stats, pattern="^back_to_stats$"),
        ],
        State.STATS.ASK_LOCAL_PROVINCE_CITY: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_local_province_city),
        ],
    },
    fallbacks=[
        CallbackQueryHandler(invalid_selection),
        CommandHandler("cancel", cancel),
    ],
)
