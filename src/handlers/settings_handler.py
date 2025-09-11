from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

from config.config_manager import NODE_ENV
from constant.language_constant import LANG_DATA, get_text, user_data_store
from constants import State
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


# ======================================================================================================================
# /settings command entry point
# ======================================================================================================================
async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Entry point for /settings command."""
    user_id = update.effective_user.id
    user_lang = await get_user_lang(user_id)
    if user_lang:
        user_data_store[user_id] = {"lang": user_lang}
        context.user_data["lang"] = user_lang

    kb = _get_main_settings_keyboard(user_id)
    reply_markup = InlineKeyboardMarkup(kb)
    text = get_text(user_id, "menu_settings_title", "settings")

    if update.message:
        await update.message.reply_text(
            text, reply_markup=reply_markup, parse_mode="HTML"
        )
    elif update.callback_query:
        await update.callback_query.edit_message_text(
            text, reply_markup=reply_markup, parse_mode="HTML"
        )

    return State.SETTINGS.SETTINGS_MENU


# ======================================================================================================================
# Main menu callback handler
# ======================================================================================================================
async def settings_menu_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle settings menu actions."""
    query = update.callback_query
    await query.answer()
    choice = query.data

    if choice == "settings_language":
        return await _handle_language_selection(query)
    if choice == "settings_mobile":
        return await _handle_mobile_management(query)
    if choice == "settings_close":
        return await _handle_close_menu(query)
    if choice.startswith("setlang_"):
        return await _handle_set_language(query, context)
    if choice.startswith("mobile_"):
        return await _handle_mobile_selection(query)
    if choice.startswith("remove_"):
        return await _handle_remove_mobile(query)

    await query.edit_message_text(
        get_text(query.from_user.id, "invalid_choice", "globals"), parse_mode="HTML"
    )
    return State.SETTINGS.END


# ======================================================================================================================
# Mobile number input and verification handlers
# ======================================================================================================================
@catch_async
async def handle_setting_mobile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user's mobile number input."""
    user_id = update.effective_user.id
    mobile = update.message.text.strip()

    if not validate_mobile(mobile):
        await update.message.reply_text(
            get_text(user_id, "invalid_mobile_number", "settings")
        )
        return State.SETTINGS.WAITING_FOR_MOBILE

    if await MobileNumber.find_one({"number": mobile}):
        await update.message.reply_text(
            get_text(user_id, "number_already_registered", "settings")
        )
        return ConversationHandler.END

    context.user_data["mobile"] = mobile

    if NODE_ENV == "production":
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

    await save_user_mobiles(user_id, mobile)
    mobiles = await get_user_mobiles(user_id)
    kb = _get_mobile_management_keyboard(user_id, mobiles)

    await update.message.reply_text(
        get_text(user_id, "mobile_verified_and_saved", "settings"),
        reply_markup=InlineKeyboardMarkup(kb),
        parse_mode="HTML",
    )
    return State.SETTINGS.SETTINGS_MOBILE_MANAGEMENT


# ======================================================================================================================
# Helper functions for menu actions
# ======================================================================================================================
async def _handle_language_selection(query) -> int:
    """Show language selection menu."""
    user_id = query.from_user.id
    kb = _get_language_keyboard()
    await query.edit_message_text(
        text=get_text(user_id, "choose_language", "settings"),
        reply_markup=InlineKeyboardMarkup(kb),
        parse_mode="HTML",
    )
    return State.SETTINGS.SETTINGS_MENU


async def _handle_mobile_management(query) -> int:
    """Show mobile number management menu."""
    user_id = query.from_user.id
    mobiles = await get_user_mobiles(user_id)
    if not mobiles:
        await query.edit_message_text(
            get_text(user_id, "enter_mobile", "settings"), parse_mode="Markdown"
        )
        return State.SETTINGS.WAITING_FOR_MOBILE

    kb = _get_mobile_management_keyboard(user_id, mobiles)
    await query.edit_message_text(
        get_text(user_id, "saved_mobile_numbers", "settings"),
        reply_markup=InlineKeyboardMarkup(kb),
        parse_mode="HTML",
    )
    return State.SETTINGS.SETTINGS_MOBILE_MANAGEMENT


async def _handle_close_menu(query) -> int:
    """Close the settings menu."""
    user_id = query.from_user.id
    await query.edit_message_text(
        text=get_text(user_id, "menu_close", "settings"),
        parse_mode="HTML",
        reply_markup=None,
    )
    return State.SETTINGS.END


async def _handle_set_language(query, context) -> int:
    """Save the selected language."""
    user_id = query.from_user.id
    new_lang = query.data.replace("setlang_", "")
    await save_user_lang(user_id, new_lang)
    context.user_data["lang"] = new_lang
    user_data_store.setdefault(user_id, {})["lang"] = new_lang
    await query.edit_message_text(
        get_text(user_id, "lang_updated", "settings"), parse_mode="HTML"
    )
    return State.SETTINGS.END


async def _handle_mobile_selection(query) -> int:
    """Handle selection of a mobile number."""
    user_id = query.from_user.id
    mobile = query.data.replace("mobile_", "")

    if mobile == "add":
        await query.edit_message_text(
            get_text(user_id, "enter_mobile", "settings"), parse_mode="Markdown"
        )
        return State.SETTINGS.WAITING_FOR_MOBILE

    kb = _get_selected_mobile_keyboard(user_id, mobile)
    await query.edit_message_text(
        get_text(user_id, "selected_mobile_options", "settings").format(mobile=mobile),
        reply_markup=InlineKeyboardMarkup(kb),
        parse_mode="HTML",
    )
    return State.SETTINGS.MOBILE_VERIFICATION


async def _handle_remove_mobile(query) -> int:
    """Remove a mobile number."""
    user_id = query.from_user.id
    mobile = query.data.replace("remove_", "")
    await delete_user_mobile(user_id, mobile)
    await query.edit_message_text(
        get_text(user_id, "mobile_removed", "settings").format(mobile=mobile),
        parse_mode="HTML",
    )
    # After removing, show the updated list of mobile numbers
    return await _handle_mobile_management(query)


# ======================================================================================================================
# Keyboard layout helper functions
# ======================================================================================================================
def _get_main_settings_keyboard(user_id: int) -> list:
    """Returns the main settings keyboard."""
    return [
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


def _get_language_keyboard() -> list:
    """Returns the language selection keyboard."""
    langs = [
        ("english", "chinese"),
        ("malay", "thai"),
        ("vietnamese", "urdu"),
        ("japanese", "korean"),
        ("khmer", "indonesian"),
    ]
    return [
        [
            InlineKeyboardButton(
                LANG_DATA["globals"][lang]["lang_button"], callback_data=f"setlang_{lang}"
            )
            for lang in row
        ]
        for row in langs
    ]


def _get_mobile_management_keyboard(user_id: int, mobiles: list) -> list:
    """Returns the mobile management keyboard."""
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
    return kb


def _get_selected_mobile_keyboard(user_id: int, mobile: str) -> list:
    """Returns the keyboard for a selected mobile."""
    return [
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
