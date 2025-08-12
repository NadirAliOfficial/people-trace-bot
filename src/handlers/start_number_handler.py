import re
from config.config_manager import (
    CLIENT,
    NODE_ENV,
)
from constant.language_constant import get_text
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ContextTypes,
)
import logging
from constants import (
    State,
)

from models.mobile_number_model import MobileNumber
from services.case_service import update_or_create_case
from services.otp_service import send_otp, verify_otp
from utils.twilio import generate_tac
from solana.rpc.api import Client

client = Client(CLIENT)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# --- Create Case Handlers (with separate states for each person detail) ---


async def handle_select_mobile(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle the selection of an existing mobile number or adding a new one."""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    print("Getting the query data which is ", query.data)

    if query.data == "mobile_add":
        await query.edit_message_text(
            get_text(user_id, "enter_mobile_post_case", "start-mobile"), parse_mode="Markdown"
        )
        return State.CREATE_CASE_MOBILE
    else:
        selected_mobile = query.data.replace("select_mobile_", "")

        mobile_number = await MobileNumber.find_one({"number": selected_mobile})

        if not mobile_number:
            await query.edit_message_text(
                get_text(user_id, "mobile_number_doesnt_exist", "start-mobile")
            )
            return State.CREATE_CASE_MOBILE

        context.user_data["mobile"] = selected_mobile
        context.user_data["selected_number"] = selected_mobile

        if NODE_ENV == "production":
            res = await send_otp(selected_mobile)
            print(f"Response would be :{res}")
            context.user_data["case"]["otp_id"] = res["otp_id"]
        else:
            if "case" not in context.user_data:
                context.user_data["case"] = {}
            context.user_data["case"]["otp_id"] = "dummy_otp_id"
            print(f"Skipping OTP sending in {NODE_ENV} mode.")

        await query.edit_message_text(get_text(user_id, "enter_tac", "start-mobile"))
        return State.CREATE_CASE_TAC


async def handle_new_mobile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the input of a new mobile number."""
    user_id = update.effective_user.id
    mobile_number = update.message.text.strip()

    if "case" not in context.user_data:
        context.user_data["case"] = {}

    print("Mobile Number is:", mobile_number)
    if re.match(r"^\+?\d{10,15}$", mobile_number):
        context.user_data["mobile"] = mobile_number
        context.user_data["selected_number"] = mobile_number
        if NODE_ENV == "production":
            tac = generate_tac()
            context.user_data["tac"] = tac
            res = await send_otp(mobile_number)
            context.user_data["case"]["otp_id"] = res["otp_id"]
            await update.message.reply_text(
                get_text(user_id, "mobile_selected_with_tac", "start-mobile").format(
                    mobile_number=mobile_number
                )
            )
        else:
            if "case" not in context.user_data:
                context.user_data["case"] = {}
            context.user_data["case"]["otp_id"] = "dummy_otp_id"
            print(f"Skipping OTP sending in {NODE_ENV} mode.")
        await update.message.reply_text(get_text(user_id, "enter_tac", "start-mobile"))
        return State.CREATE_CASE_TAC
    else:
        await update.message.reply_text(
            get_text(user_id, "enter_valid_mobile", "start-mobile")
        )
        return State.CREATE_CASE_MOBILE


async def handle_tac(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle TAC verification."""
    user_id = update.effective_user.id
    user_tac = update.message.text.strip()
    stored_tac = context.user_data.get("tac")
    selected_number = context.user_data.get("selected_number")

    if NODE_ENV == "production":
        otp_verify = await verify_otp(context.user_data["case"]["otp_id"], user_tac)
        if otp_verify["success"]:
            await update.message.reply_text(
                get_text(user_id, "tac_verified", "start-mobile")
            )

            # Update case with selected mobile number
            await update_or_create_case(user_id, mobile=selected_number)

            # Show disclaimer before proceeding
            disclaimer_text = get_text(user_id, "case_poster_disclaimer", "case")
            buttons = [
                [
                    InlineKeyboardButton(
                        get_text(user_id, "understood_and_agree", "globals"),
                        callback_data="agree",
                    ),
                    InlineKeyboardButton(
                        get_text(user_id, "cancel_button", "globals"),
                        callback_data="disagree",
                    ),
                ]
            ]
            markup = InlineKeyboardMarkup(buttons)

            await update.message.reply_text(
                disclaimer_text, reply_markup=markup, parse_mode="Markdown"
            )
            return State.CREATE_CASE_DISCLAIMER

        else:
            await update.message.reply_text(get_text(user_id, "tac_invalid"))
            return State.CREATE_CASE_TAC

    else:
        print(f"Skipping OTP verification in {NODE_ENV} mode.")
        await update.message.reply_text(
            get_text(user_id, "tac_verified", "start-mobile")
        )
        await update_or_create_case(user_id, mobile=selected_number)

        # Show disclaimer before proceeding
        disclaimer_text = get_text(user_id, "case_poster_disclaimer", "case")
        buttons = [
            [
                InlineKeyboardButton(
                    get_text(user_id, "understood_and_agree", "globals"),
                    callback_data="agree",
                ),
                InlineKeyboardButton(
                    get_text(user_id, "cancel_button", "globals"),
                    callback_data="disagree",
                ),
            ]
        ]
        markup = InlineKeyboardMarkup(buttons)

        await update.message.reply_text(
            disclaimer_text, reply_markup=markup, parse_mode="Markdown"
        )
        print("This block runs")
        return State.CREATE_CASE_DISCLAIMER
