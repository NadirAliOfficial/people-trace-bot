import re
from config.config_manager import (
    CLIENT,
    NODE_ENV,
    OWNER_TELEGRAM_ID,
    SOL_WALLET_PUBLIC_KEY,
    TRON_WALLET_PRIVATE_KEY,
    TRON_WALLET_PUBLIC_KEY,
)
from constant.language_constant import get_text
from models.case_model import Case, CaseStatus
import os
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
from services.wallet_service import WalletService
from utils.error_wrapper import catch_async
from utils.twilio import generate_tac
from utils.wallet import load_user_wallet
from utils.cloudinary import upload_image
from solana.rpc.api import Client
from models.wallet_model import Wallet
from services.user_service import get_user_mobiles, save_user_mobiles, validate_mobile
from services.tron_wallet_service import TronWallet

client = Client(CLIENT)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)




async def create_case_disclaimer_2_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle Disclaimer 2 agreement."""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    print(f"User {user_id} entered disclaimer 2")
    if query.data == "agree":
        kb = [
            [
                InlineKeyboardButton(get_text(user_id, "usdt_btn", "globals"), callback_data="USDT"),
                InlineKeyboardButton(get_text(user_id, "sol_btn", "globals"), callback_data="SOL"),
            ]
        ]
        markup = InlineKeyboardMarkup(kb)

        await query.edit_message_text(
            get_text(user_id, "choose_wallet_header", "wallets"),
            reply_markup=markup,
            parse_mode="HTML"
        )
        return State.CHOOSE_OR_CREATE_WALLET

    else:
        await query.edit_message_text(get_text(user_id, "disagree_end", "globals"))
        return State.END


# _________ PERSON
async def handle_person_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle input for the person's name (the case target)."""
    user_id = update.effective_user.id
    person_name = update.message.text.strip()
    await update_or_create_case(user_id, person_name=person_name)
    context.user_data["case"]["person_name"] = person_name
    logger.info(f"User {user_id} entered person name: {person_name}")
    kb = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    get_text(user_id, "male_option", "cases"), callback_data="male"
                ),
                InlineKeyboardButton(
                    get_text(user_id, "female_option", "cases"), callback_data="female"
                ),
            ]
        ]
    )
    await update.message.reply_text(get_text(user_id, "gender", "cases"), reply_markup=kb)
    return State.CREATE_CASE_SEX


# _________ WHAT IS THE GENDER OF HIS
async def handle_sex(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle input for sex."""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    sex = query.data
    await update_or_create_case(user_id, gender=sex)
    context.user_data["case"]["sex"] = sex
    logger.info(f"User {user_id} selected sex: {sex}")
    await query.edit_message_text(get_text(user_id, "age", "cases"))
    return State.CREATE_CASE_AGE


# _________ AGE OF THE PERSON
async def handle_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle input for age."""
    user_id = update.effective_user.id
    age = update.message.text.strip()

    if not age.isdigit():
        await update.message.reply_text(get_text(user_id, "valid_age", "cases"))
        return State.CREATE_CASE_AGE

    await update_or_create_case(user_id, age=age)
    context.user_data["case"]["age"] = age
    logger.info(f"User {user_id} entered age: {age}")
    await update.message.reply_text(get_text(user_id, "relationship", "cases"))
    return State.CREATE_CASE_RELATIONSHIP


# _________ RELATION TO THE PERSON
async def handle_relationship(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle input for relationship detail."""
    user_id = update.effective_user.id
    relationship = update.message.text.strip()
    await update_or_create_case(user_id, relationship=relationship)
    context.user_data["case"]["relationship"] = relationship
    logger.info(f"User {user_id} entered relationship: {relationship}")

    await update.message.reply_text(get_text(user_id, "upload_photo", "cases"))
    return State.CREATE_CASE_PHOTO


# _________ PHOTO OF HIS/HER
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle photo upload and store it on Cloudinary."""
    user_id = update.effective_user.id

    if not update.message.photo:
        await update.message.reply_text(get_text(user_id, "no_photo_found", "cases"))
        return State.CREATE_CASE_PHOTO
    photo_file = await update.message.photo[-1].get_file()
    photo_dir = os.path.join(os.getcwd(), "photos")
    os.makedirs(photo_dir, exist_ok=True)
    photo_path = os.path.join(photo_dir, f"{user_id}_photo.jpg")
    logger.info(f"Saving photo at path: {photo_path}")
    await photo_file.download_to_drive(photo_path)
    upload_result = await upload_image(photo_path)
    if upload_result:
        logger.info(f"Uploaded Photo URL: {upload_result}")

        await update_or_create_case(user_id, case_photo=upload_result)
        context.user_data["case"][
            "photo_url"
        ] = upload_result  # Store URL instead of local path

    await update.message.reply_text(get_text(user_id, "hair_color", "cases"))
    return State.CREATE_CASE_HAIR_COLOR


# _________ HAIR COLOR OF THE PERSON
async def handle_hair_color(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle input for hair color."""
    user_id = update.effective_user.id
    hair_color = update.message.text.strip()
    await update_or_create_case(user_id, hair_color=hair_color)
    context.user_data["case"]["hair_color"] = hair_color
    logger.info(f"User {user_id} entered hair color: {hair_color}")
    await update.message.reply_text(get_text(user_id, "eye_color", "cases"))
    return State.CREATE_CASE_EYE_COLOR


# _________ EYE COLOR OF THE PERSON
async def handle_eye_color(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle input for eye color."""
    user_id = update.effective_user.id
    eye_color = update.message.text.strip()
    await update_or_create_case(user_id, eye_color=eye_color)
    context.user_data["case"]["eye_color"] = eye_color
    logger.info(f"User {user_id} entered eye color: {eye_color}")
    await update.message.reply_text(get_text(user_id, "last_seen_location", "cases"))
    return State.CREATE_CASE_LAST_SEEN_LOCATION


# _________ LOCATION OF THE PERSON WHERE IT CAN BE SEEN
async def handle_last_seen_location(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle input for last seen location."""
    user_id = update.effective_user.id
    location = update.message.text.strip()
    await update_or_create_case(user_id, last_seen_location=location)
    context.user_data["case"]["last_seen_location"] = location
    logger.info(f"User {user_id} entered last seen location: {location}")

    await update.message.reply_text(get_text(user_id, "height", "cases"))
    return State.CREATE_CASE_HEIGHT


# _________ HEIGHT OF THE PERSON
async def handle_height(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle input for height."""
    user_id = update.effective_user.id
    height = update.message.text.strip()
    print("Step 1")
    if not height.isdigit():
        await update.message.reply_text("Please enter a valid number for height.")
        return State.CREATE_CASE_HEIGHT

    await update_or_create_case(user_id, height=height)
    context.user_data["case"]["height"] = height
    logger.info(f"User {user_id} entered height: {height}")
    print("Step 2")
    await update.message.reply_text(get_text(user_id, "weight", "cases"))
    return State.CREATE_CASE_WEIGHT


# _________ WEIGHT OF THE PERSON
async def handle_weight(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle input for weight."""
    user_id = update.effective_user.id
    weight = update.message.text.strip()

    if not weight.isdigit():
        await update.message.reply_text(get_text(user_id, "enter_valid_weight", "cases"))
        return State.CREATE_CASE_WEIGHT

    await update_or_create_case(user_id, weight=weight)
    context.user_data["case"]["weight"] = weight
    logger.info(f"User {user_id} entered weight: {weight}")
    await update.message.reply_text(get_text(user_id, "distinctive_features", "cases"))
    return State.CREATE_CASE_DISTINCTIVE_FEATURES


# _________ DISTINCTIVE FEATURE
async def handle_distinctive_features(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle input for distinctive features."""
    user_id = update.effective_user.id
    features = update.message.text.strip()

    await update_or_create_case(user_id, distinctive_features=features)
    context.user_data["case"]["distinctive_features"] = features
    logger.info(f"User {user_id} entered distinctive features: {features}")
    await update.message.reply_text(get_text(user_id, "reason_for_finding", "cases"))
    return State.CREATE_CASE_ASK_REASON


# _________ REASON OF FINDING (TODO: Add a check to see if the user has already been notified)
async def handle_reason_for_finding(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle input for reason for finding and ask for reward amount."""
    user_id = update.effective_user.id
    reason = update.message.text.strip()

    case = await Case.find_one(
        {"user_id": user_id, "status": CaseStatus.DRAFT}, fetch_links=True
    )

    if not case:
        await update.message.reply_text(get_text(user_id, "case_not_found", "cases"))
        return State.END

    case.reason = reason
    await case.save()
    wallet = case.wallet
    print("Getting the sol", wallet.wallet_type)
    
    # Use the new reward setup prompt
    await update.message.reply_text(
        get_text(user_id, "reward_setup_prompt_usdt", "cases")
    )

    return State.CREATE_CASE_ASK_REWARD


# _________ REWARD AMOUNT OF THE CASE
@catch_async
async def handle_ask_reward_amount(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle asking for reward amount and check wallet balance."""
    user_id = update.effective_user.id
    text = update.message.text.strip()

    print(f"[ASK_REWARD] User input: {text}")

    try:
        reward_amount = float(text)
    except ValueError:
        await update.message.reply_text(get_text(user_id, "reward_amount_invalid", "cases"))
        return State.CREATE_CASE_ASK_REWARD

    if reward_amount <= 0:
        await update.message.reply_text(
            get_text(user_id, "reward_amount_negative", "cases").format(reward_amount)
        )
        return State.CREATE_CASE_ASK_REWARD

    # Fetch draft case & wallet
    case = await Case.find_one({"user_id": user_id, "status": CaseStatus.DRAFT})
    wallet = await case.wallet.fetch()

    wallet_type = wallet.wallet_type
    wallet_balance = (
        await WalletService.get_sol_balance(wallet.public_key)
        if wallet_type == "SOL"
        else await TronWallet.get_usdt_balance(wallet.public_key)
    )

    # Store reward amount temporarily
    case.reward = reward_amount
    await case.save()

    # === Insufficient balance case ===
    if wallet_balance < reward_amount:
        msg = get_text(user_id, "insufficient_balance_detailed", "cases").format(
            wallet_balance=wallet_balance,
            reward_amount=reward_amount,
            wallet_address=wallet.public_key
        )

        buttons = [
            [InlineKeyboardButton(get_text(user_id, "refresh_button", "cases"), callback_data=f"refresh_balance:{reward_amount}")],
            [InlineKeyboardButton(get_text(user_id, "back_btn", "cases"), callback_data="back_to_reason")]
        ]

        await update.message.reply_text(msg, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(buttons))
        return State.CREATE_CASE_ASK_REWARD

    # === Balance is OK - Show reward confirmation with tip and buttons ===
    msg = get_text(user_id, "reward_set_with_tip", "cases").format(amount=reward_amount)
    
    buttons = [
        [
            InlineKeyboardButton(get_text(user_id, "increase_reward_btn", "cases"), callback_data="increase_reward"),
            InlineKeyboardButton(get_text(user_id, "back_btn", "cases"), callback_data="back_to_reason"),
        ]
    ]

    await update.message.reply_text(
        msg, 
        parse_mode="HTML", 
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    
    # Show balance check message and final submission buttons
    await update.message.reply_text(
        get_text(user_id, "case_ready_to_publish", "cases"),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(get_text(user_id, "submit_case_button", "cases"), callback_data="confirm_transfer"),
                InlineKeyboardButton(get_text(user_id, "edit_button", "cases"), callback_data="edit_case"),
            ],
            [
                InlineKeyboardButton(get_text(user_id, "cancel_button", "cases"), callback_data="cancel_transfer"),
            ]
        ])
    )
    
    return State.CREATE_CASE_CONFIRM_TRANSFER


# _________ NEW HANDLER FOR INCREASE REWARD
@catch_async
async def handle_increase_reward(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle increase reward button callback."""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    # Go back to asking for reward amount
    await query.edit_message_text(
        get_text(user_id, "reward_setup_prompt_usdt", "cases"),
        parse_mode="HTML"
    )
    return State.CREATE_CASE_ASK_REWARD


# Removed helper function - logic moved to individual handlers


# === Callback Handler for Continue with smaller reward ===
@catch_async
async def handle_continue_with_reward(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Proceed to confirmation even if reward < 1000."""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    reward_amount = float(query.data.split(":")[1]) if ":" in query.data else 0

    case = await Case.find_one({"user_id": user_id, "status": CaseStatus.DRAFT})
    wallet = await case.wallet.fetch()
    
    await query.edit_message_text(
        text=get_text(user_id, "case_ready_to_publish", "cases"),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(get_text(user_id, "submit_case_button", "cases"), callback_data="confirm_transfer"),
                InlineKeyboardButton(get_text(user_id, "edit_button", "cases"), callback_data="edit_case"),
            ],
            [
                InlineKeyboardButton(get_text(user_id, "cancel_button", "cases"), callback_data="cancel_transfer"),
            ]
        ])
    )
    return State.CREATE_CASE_CONFIRM_TRANSFER


# === Callback Handler for Going Back with prompt ===
@catch_async
async def handle_back_to_reason(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Re-prompt user for reward amount, showing what they entered last."""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    await query.edit_message_text(
        text=get_text(user_id, "reward_setup_prompt_usdt", "cases"), 
        parse_mode="HTML"
    )
    return State.CREATE_CASE_ASK_REWARD


# === Callback Handler for Refreshing Balance ===
@catch_async
async def handle_refresh_balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Re-check wallet balance when user presses Refresh button."""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = query.data.split(":")
    reward_amount = float(data[1]) if len(data) > 1 else 0

    # Get draft case & wallet
    case = await Case.find_one({"user_id": user_id, "status": CaseStatus.DRAFT})
    wallet = await case.wallet.fetch()

    wallet_balance = (
        await WalletService.get_sol_balance(wallet.public_key)
        if wallet.wallet_type == "SOL"
        else await TronWallet.get_usdt_balance(wallet.public_key)
    )

    if wallet_balance < reward_amount:
        await query.edit_message_text(
            text=get_text(user_id, "insufficient_balance_detailed", "cases").format(
                wallet_balance=wallet_balance,
                reward_amount=reward_amount,
                wallet_address=wallet.public_key
            ),
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(get_text(user_id, "refresh_button", "cases"), callback_data=f"refresh_balance:{reward_amount}")],
                [InlineKeyboardButton(get_text(user_id, "back_btn", "cases"), callback_data="back_to_reason")]
            ])
        )
        return State.CREATE_CASE_ASK_REWARD

    # ✅ Balance now sufficient - proceed to final confirmation
    await query.edit_message_text(
        text=get_text(user_id, "case_ready_to_publish", "cases"),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(get_text(user_id, "submit_case_button", "cases"), callback_data="confirm_transfer"),
                InlineKeyboardButton(get_text(user_id, "edit_button", "cases"), callback_data="edit_case"),
            ],
            [
                InlineKeyboardButton(get_text(user_id, "cancel_button", "cases"), callback_data="cancel_transfer"),
            ]
        ])
    )
    return State.CREATE_CASE_CONFIRM_TRANSFER


# === NEW HANDLER FOR EDIT CASE ===
@catch_async
async def handle_edit_case(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle edit case button - return to reward amount setting."""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    await query.edit_message_text(
        get_text(user_id, "reward_setup_prompt_usdt", "cases"),
        parse_mode="HTML"
    )
    return State.CREATE_CASE_ASK_REWARD


# _________ CONFIRMATION OF THE REWARD BY ASKING YES OR NO & IF YES THEN TRANSFER THE COIN TO THE STAKE WALLET
async def handle_transfer_confirmation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle confirmation of the reward transfer."""
    user_id = update.effective_user.id
    query = update.callback_query
    user_input = query.data.strip().lower()

    case = await Case.find_one(
        {"user_id": user_id, "status": CaseStatus.DRAFT}, fetch_links=True
    )
    wallet = case.wallet
    reward_amount = case.reward
    wallet_type = wallet.wallet_type

    if user_input == "confirm_transfer":
        try:
            wallet_balance = (
                await WalletService.get_sol_balance(wallet.public_key)
                if wallet.wallet_type == "SOL"
                else await TronWallet.get_usdt_balance(wallet.public_key)
            )

            if wallet.wallet_type in ["USDT", "TRX"] and wallet_balance < reward_amount:
                await query.answer()
                await query.edit_message_text(
                    get_text(user_id, "insufficient_balance_detailed", "cases").format(
                        wallet_balance=wallet_balance,
                        reward_amount=reward_amount,
                        wallet_address=wallet.public_key
                    ),
                    parse_mode="HTML",
                )
                return State.CREATE_CASE_CONFIRM_TRANSFER

            transfer_success = (
                await WalletService.send_sol(
                    wallet.private_key, SOL_WALLET_PUBLIC_KEY, reward_amount
                )
                if wallet.wallet_type == "SOL"
                else await TronWallet.transfer_usdt(
                    wallet.private_key, TRON_WALLET_PUBLIC_KEY, reward_amount
                )
            )

            print(f"Transfer_success: {transfer_success}")
            if transfer_success:
                # Notify the advertiser (user who confirmed)
                platform_fee = round(reward_amount * 0.05, 2)
                net_escrow = round(reward_amount - platform_fee, 2)

                advertiser_message = get_text(
                    user_id, "congratulates_advertiser", "cases"
                ).format(
                    reward_amount=reward_amount,
                    wallet_type=wallet_type,
                    case_name=case.person_name or "Unknown",
                    location=case.city or "Unknown",
                    platform_fee=platform_fee,
                    net_amount=net_escrow,
                )

                # Notify the bot owner
                owner_message = get_text(user_id, "owner_message", "cases").format(
                    user_id=user_id,
                    case=case,
                    reward_amount=reward_amount,
                    wallet_type=wallet_type,
                    wallet=wallet,
                )
                await context.bot.send_message(
                    chat_id=OWNER_TELEGRAM_ID, text=owner_message, parse_mode="HTML"
                )

                case.status = CaseStatus.ADVERTISE
                await case.save()
                context.user_data["case"] = None

                await query.edit_message_text(advertiser_message, parse_mode="HTML")
                return State.END

            else:
                await query.answer()
                await query.edit_message_text(
                    get_text(user_id, "transaction_failed", "cases"), parse_mode="HTML"
                )

        except Exception as e:
            print(f"Transfer failed: {e}")
            await query.answer()
            await query.edit_message_text(
                get_text(user_id, "transfer_failed", "cases"), parse_mode="HTML"
            )

    elif user_input == "cancel_transfer":
        await query.answer()
        await query.edit_message_text(
            get_text(user_id, "transfer_canceled", "cases"), parse_mode="HTML"
        )
        return State.CREATE_CASE_ASK_REWARD

    elif user_input == "edit_case":
        return await handle_edit_case(update, context)

    else:
        await query.answer()
        await query.edit_message_text(
            get_text(user_id, "invalid_choice", "cases"), parse_mode="HTML"
        )
        return State.CREATE_CASE_CONFIRM_TRANSFER

    return State.CREATE_CASE_CONFIRM_TRANSFER