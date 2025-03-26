from config.config_manager import NODE_ENV
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from constants import State
from constant.language_constant import get_text, user_data_store, LANG_DATA
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


# Handlers
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
                get_text(user_id, "btn_language"), callback_data="settings_language"
            )
        ],
        [
            InlineKeyboardButton(
                get_text(user_id, "btn_mobile_number"), callback_data="settings_mobile"
            )
        ],
        [
            InlineKeyboardButton(
                get_text(user_id, "btn_close_menu"), callback_data="settings_close"
            )
        ],
    ]
    await update.message.reply_text(
        get_text(user_id, "menu_settings_title"),
        reply_markup=InlineKeyboardMarkup(kb),
        parse_mode="HTML",
    )
    return State.SETTINGS_MENU


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
                    LANG_DATA["en"]["lang_button"], callback_data="setlang_en"
                ),
                InlineKeyboardButton(
                    LANG_DATA["zh"]["lang_button"], callback_data="setlang_zh"
                ),
                InlineKeyboardButton(
                    LANG_DATA["ms"]["lang_button"], callback_data="setlang_ms"
                ),
            ],
        ]
        await query.edit_message_text(
            text=get_text(user_id, "choose_language"),
            reply_markup=InlineKeyboardMarkup(kb),
            parse_mode="HTML",
        )
        return State.SETTINGS_MENU

    elif choice == "settings_mobile":
        # Mobile management
        mobiles = await get_user_mobiles(user_id)
        print(f"Getting the mobile numbers : {mobiles}")
        if not mobiles:
            await query.edit_message_text(
                get_text(user_id, "enter_mobile"), parse_mode="HTML"
            )
            return State.WAITING_FOR_MOBILE
        else:
            # Show saved mobile numbers
            kb = [
                [InlineKeyboardButton(f"📱 {mobile}", callback_data=f"mobile_{mobile}")]
                for mobile in mobiles
            ]
            kb.append(
                [
                    InlineKeyboardButton(
                        get_text(user_id, "btn_add_new"), callback_data="mobile_add"
                    )
                ]
            )
            await query.edit_message_text(
                get_text(user_id, "saved_mobile_numbers"),
                reply_markup=InlineKeyboardMarkup(kb),
                parse_mode="HTML",
            )
            return State.MOBILE_MANAGEMENT

    elif choice == "settings_close":
        # Close the menu
        await query.edit_message_text(
            get_text(user_id, "btn_close_menu"), parse_mode="HTML"
        )
        return State.END

    elif choice.startswith("setlang_"):
        new_lang = choice.replace("setlang_", "")
        await save_user_lang(user_id, new_lang)
        context.user_data["lang"] = new_lang
        if user_id not in user_data_store:
            user_data_store[user_id] = {}
        user_data_store[user_id]["lang"] = new_lang
        await query.edit_message_text(
            get_text(user_id, "lang_updated"), parse_mode="HTML"
        )
        return State.END

    elif choice.startswith("mobile_"):
        mobile = choice.replace("mobile_", "")

        if mobile == "add":
            await query.edit_message_text(
                get_text(user_id, "enter_mobile"), parse_mode="HTML"
            )
            return State.WAITING_FOR_MOBILE
        else:
            # Options for selected mobile
            kb = [
                [
                    InlineKeyboardButton(
                        get_text(user_id, "remove_mobile"),
                        callback_data=f"remove_{mobile}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        get_text(user_id, "back_to_mobile_menu"),
                        callback_data="settings_mobile",
                    )
                ],
            ]
            await query.edit_message_text(
                get_text(user_id, "selected_mobile_options").format(mobile=mobile),
                reply_markup=InlineKeyboardMarkup(kb),
                parse_mode="HTML",
            )
            return State.MOBILE_VERIFICATION

    elif choice.startswith("remove_"):
        mobile = choice.replace("remove_", "")
        await delete_user_mobile(user_id, mobile)
        await query.edit_message_text(
            get_text(user_id, "mobile_removed").format(mobile=mobile),
            parse_mode="HTML",
        )
        return State.MOBILE_MANAGEMENT

    else:
        await query.edit_message_text(
            get_text(user_id, "invalid_choice"), parse_mode="HTML"
        )
        return State.END


import os


@catch_async
async def handle_setting_mobile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the user's mobile number input."""
    user_id = update.effective_user.id
    mobile = update.message.text.strip()

    if not validate_mobile(mobile):
        await update.message.reply_text(get_text(user_id, "invalid_mobile_number"))
        return State.WAITING_FOR_MOBILE

    context.user_data["mobile"] = mobile

    if NODE_ENV == "production":
        # Generate TAC
        tac = generate_tac()

        # Save TAC and mobile in user data store
        if user_id not in user_data_store:
            user_data_store[user_id] = {}
        user_data_store[user_id]["mobile"] = mobile

        res = await send_otp(mobile)
        print(f"Getting the OTP: {res}")

        context.user_data["otp_id"] = res["otp_id"]
    else:
        # In development, just set a dummy OTP
        context.user_data["otp_id"] = "dummy_otp_id"
        print(f"Skipping OTP sending in {NODE_ENV} mode.")

    # Prompt user to enter TAC
    await update.message.reply_text(get_text(user_id, "enter_tac"))
    return State.CREATE_CASE_TAC


@catch_async
async def handle_setting_tac(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle TAC verification."""
    user_id = update.effective_user.id
    user_tac = update.message.text.strip()
    mobile = context.user_data.get("mobile")

    print(f"Getting the number which is: {mobile}")

    if NODE_ENV == "production":
        otp_verify = await verify_otp(context.user_data["otp_id"], user_tac)
        if not otp_verify["success"]:
            await update.message.reply_text(get_text(user_id, "tac_invalid"))
            return State.CREATE_CASE_TAC
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
                get_text(user_id, "btn_add_new"), callback_data="mobile_add"
            )
        ]
    )

    await update.message.reply_text(
        get_text(user_id, "mobile_verified_and_saved"),
        reply_markup=InlineKeyboardMarkup(kb),
        parse_mode="HTML",
    )
    return State.MOBILE_MANAGEMENT
