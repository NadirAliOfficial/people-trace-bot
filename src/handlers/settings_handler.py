from config.config_manager import NODE_ENV
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from constants import State
from constant.language_constant import get_text, user_data_store, LANG_DATA
from models.mobile_number_model import MobileNumber
from services.otp_service import send_otp, verify_otp
from services.user_service import (
    delete_user_mobile,
    get_user_lang,
    get_user_mobiles,
    save_user_lang,
    save_user_mobiles,
    validate_mobile,
)
from utils.error_wrapper import catch_async
from utils.helper import generate_tac
from telegram.ext import (
    ConversationHandler,
    ContextTypes,
)


# Initialization of settings
async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Entry point for /settings command - shows an inline menu."""
    user_id = update.effective_user.id

    user_lang = await get_user_lang(user_id)
    if user_lang:
        user_data_store[user_id] = {"lang": user_lang}
        context.user_data["lang"] = user_lang

    kb = [
        [
            InlineKeyboardButton(
                get_text(user_id, "btn_language", "settings"),
                callback_data="settings_language",
            )
        ],
        [
            InlineKeyboardButton(
                get_text(user_id, "btn_mobile_number", "settings"),
                callback_data="settings_mobile",
            )
        ],
        [
            InlineKeyboardButton(
                get_text(user_id, "btn_close_menu", "settings"),
                callback_data="settings_close",
            )
        ],
    ]
    if update.message:
        await update.message.reply_text(
            get_text(user_id, "menu_settings_title", "settings"),
            reply_markup=InlineKeyboardMarkup(kb),
            parse_mode="HTML",
        )
    elif update.callback_query:
        await update.callback_query.edit_message_text(
            get_text(user_id, "menu_settings_title", "settings"),
            reply_markup=InlineKeyboardMarkup(kb),
            parse_mode="HTML",
        )

    return State.SETTINGS.SETTINGS_MENU


# Listiner of button selection
async def settings_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the settings menu actions."""
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    choice = query.data

    if choice == "settings_language":
        # Language selection
        kb = [
            [
                InlineKeyboardButton(
                    f"{LANG_DATA["globals"]['english']['lang_button']}",
                    callback_data="setlang_english",
                ),
                InlineKeyboardButton(
                    f"{LANG_DATA["globals"]['chinese']['lang_button']}",
                    callback_data="setlang_chinese",
                ),
            ],
            [
                InlineKeyboardButton(
                    f"{LANG_DATA["globals"]['malay']['lang_button']}",
                    callback_data="setlang_malay",
                ),
                InlineKeyboardButton(
                    f"{LANG_DATA["globals"]['thai']['lang_button']}",
                    callback_data="setlang_thai",
                ),
            ],
            [
                InlineKeyboardButton(
                    f"{LANG_DATA["globals"]['vietnamese']['lang_button']}",
                    callback_data="setlang_vietnamese",
                ),
                InlineKeyboardButton(
                    f"{LANG_DATA["globals"]['urdu']['lang_button']}",
                    callback_data="setlang_urdu",
                ),
            ],
            [
                InlineKeyboardButton(
                    f"{LANG_DATA["globals"]['japanese']['lang_button']}",
                    callback_data="setlang_japanese",
                ),
                InlineKeyboardButton(
                    f"{LANG_DATA["globals"]['korean']['lang_button']}",
                    callback_data="setlang_korean",
                ),
            ],
            [
                InlineKeyboardButton(
                    f"{LANG_DATA["globals"]['khmer']['lang_button']}",
                    callback_data="setlang_khmer",
                ),
                InlineKeyboardButton(
                    f"{LANG_DATA["globals"]['indonesian']['lang_button']}",
                    callback_data="setlang_indonesian",
                ),
            ],
        ]
        await query.edit_message_text(
            text=get_text(user_id, "choose_language", "settings"),
            reply_markup=InlineKeyboardMarkup(kb),
            parse_mode="HTML",
        )
        return State.SETTINGS.SETTINGS_MENU

    elif choice == "settings_mobile":
        # Mobile management
        mobiles = await get_user_mobiles(user_id)
        if not mobiles:
            await query.edit_message_text(
                get_text(user_id, "enter_mobile", "settings"), parse_mode="Markdown"
            )
            return State.SETTINGS.WAITING_FOR_MOBILE
        else:
            # Show saved mobile numbers
            kb = [
                [InlineKeyboardButton(f"📱 {mobile}", callback_data=f"mobile_{mobile}")]
                for mobile in mobiles
            ]
            kb.append(
                [
                    InlineKeyboardButton(
                        get_text(user_id, "btn_add_new", "settings"),
                        callback_data="mobile_add",
                    )
                ]
            )
            await query.edit_message_text(
                get_text(user_id, "saved_mobile_numbers", "settings"),
                reply_markup=InlineKeyboardMarkup(kb),
                parse_mode="HTML",
            )
            return State.SETTINGS.SETTINGS_MOBILE_MANAGEMENT

    elif choice == "settings_close":
        await query.edit_message_text(
            text=get_text(user_id, "menu_close", "settings"),
            parse_mode="HTML",
            reply_markup=None,
        )
        return State.SETTINGS.END

    elif choice.startswith("setlang_"):
        new_lang = choice.replace("setlang_", "")
        await save_user_lang(user_id, new_lang)
        context.user_data["lang"] = new_lang
        if user_id not in user_data_store:
            user_data_store[user_id] = {}
        user_data_store[user_id]["lang"] = new_lang
        await query.edit_message_text(
            get_text(user_id, "lang_updated", "settings"), parse_mode="HTML"
        )
        return State.SETTINGS.END

    elif choice.startswith("mobile_"):
        mobile = choice.replace("mobile_", "")

        if mobile == "add":
            await query.edit_message_text(
                get_text(user_id, "enter_mobile", "settings"), parse_mode="Markdown"
            )
            return State.SETTINGS.WAITING_FOR_MOBILE
        else:
            # Options for selected mobile
            kb = [
                [
                    InlineKeyboardButton(
                        get_text(user_id, "remove_mobile", "settings"),
                        callback_data=f"remove_{mobile}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        get_text(user_id, "back_to_mobile_menu", "settings"),
                        callback_data="settings_mobile",
                    )
                ],
            ]
            await query.edit_message_text(
                get_text(user_id, "selected_mobile_options", "settings").format(
                    mobile=mobile
                ),
                reply_markup=InlineKeyboardMarkup(kb),
                parse_mode="HTML",
            )
            return State.SETTINGS.MOBILE_VERIFICATION

    elif choice.startswith("remove_"):
        mobile = choice.replace("remove_", "")
        await delete_user_mobile(user_id, mobile)
        await query.edit_message_text(
            get_text(user_id, "mobile_removed", "settings").format(mobile=mobile),
            parse_mode="HTML",
        )
        return State.SETTINGS.SETTINGS_MOBILE_MANAGEMENT

    else:
        await query.edit_message_text(
            get_text(user_id, "invalid_choice", "globals"), parse_mode="HTML"
        )
        return State.SETTINGS.END


@catch_async
async def handle_setting_mobile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the user's mobile number input."""
    user_id = update.effective_user.id
    mobile = update.message.text.strip()

    if not validate_mobile(mobile):
        await update.message.reply_text(
            get_text(user_id, "invalid_mobile_number", "settings")
        )
        return State.SETTINGS.WAITING_FOR_MOBILE

    context.user_data["mobile"] = mobile

    is_already_exist = await MobileNumber.find_one({"number": mobile})

    if is_already_exist:
        await update.message.reply_text(
            get_text(user_id, "number_already_registered", "settings")
        )
        return ConversationHandler.END

    if NODE_ENV == "production":
        tac = generate_tac()

        if user_id not in user_data_store:
            user_data_store[user_id] = {}
        user_data_store[user_id]["mobile"] = mobile

        res = await send_otp(mobile)

        context.user_data["otp_id"] = res["otp_id"]
    else:
        context.user_data["otp_id"] = "dummy_otp_id"
        print(f"Skipping OTP sending in {NODE_ENV} mode.")

    await update.message.reply_text(get_text(user_id, "enter_tac", "settings"))
    return State.SETTINGS.SETTINGS_CREATE_CASE_TAC


@catch_async
async def handle_setting_tac(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle TAC verification."""
    user_id = update.effective_user.id
    user_tac = update.message.text.strip()
    mobile = context.user_data.get("mobile")

    if NODE_ENV == "production":
        otp_verify = await verify_otp(context.user_data["otp_id"], user_tac)
        if not otp_verify["success"]:
            await update.message.reply_text(
                get_text(user_id, "tac_invalid", "settings")
            )
            return State.SETTINGS.SETTINGS_CREATE_CASE_TAC
    else:
        print(f"Skipping OTP verification in {NODE_ENV} mode.")

    # Save the verified mobile number
    mobiles = await get_user_mobiles(user_id)
    if mobile not in mobiles:
        mobiles.append(mobile)
        await save_user_mobiles(user_id, mobile)

    # Show the list of saved mobile numbers
    kb = [
        [InlineKeyboardButton(f"📱 {number}", callback_data=f"mobile_{number}")]
        for number in mobiles
    ]
    kb.append(
        [
            InlineKeyboardButton(
                get_text(user_id, "btn_add_new", "settings"), callback_data="mobile_add"
            )
        ]
    )

    await update.message.reply_text(
        get_text(user_id, "mobile_verified_and_saved", "settings"),
        reply_markup=InlineKeyboardMarkup(kb),
        parse_mode="HTML",
    )
    return State.SETTINGS.SETTINGS_MOBILE_MANAGEMENT
