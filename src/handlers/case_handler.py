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
from handlers.start_handler import start
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
                InlineKeyboardButton(
                    get_text(user_id, "usdt_btn", "globals"), callback_data="USDT"
                ),
                InlineKeyboardButton(
                    get_text(user_id, "sol_btn", "globals"), callback_data="SOL"
                ),
            ]
        ]
        markup = InlineKeyboardMarkup(kb)

        await query.edit_message_text(
            get_text(user_id, "choose_wallet_header", "wallets"),
            reply_markup=markup,
            parse_mode="HTML",
        )
        return State.CHOOSE_OR_CREATE_WALLET

    else:
        await query.edit_message_text(get_text(user_id, "disagree_end", "globals"))
        return State.END


# == HANDLER: Ask for missing person name  == #
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
    await update.message.reply_text(
        get_text(user_id, "gender", "cases"), reply_markup=kb
    )
    return State.CREATE_CASE_SEX


# == HANDLER: Ask for missing person gender  == #
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


# == HANDLER: Ask for missing person age  == #
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


# === HANDLER: Ask for the missing person's relationship to the lodged person in the case === #
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


# == HANDLER: Ask for missing person photo  == #
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


# == HANDLER: Ask for missing person hair color  == #
async def handle_hair_color(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle input for hair color."""
    user_id = update.effective_user.id
    hair_color = update.message.text.strip()
    await update_or_create_case(user_id, hair_color=hair_color)
    context.user_data["case"]["hair_color"] = hair_color
    logger.info(f"User {user_id} entered hair color: {hair_color}")
    await update.message.reply_text(get_text(user_id, "eye_color", "cases"))
    return State.CREATE_CASE_EYE_COLOR


# == HANDLER: Ask for missing person eye color  == #
async def handle_eye_color(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle input for eye color."""
    user_id = update.effective_user.id
    eye_color = update.message.text.strip()
    await update_or_create_case(user_id, eye_color=eye_color)
    context.user_data["case"]["eye_color"] = eye_color
    logger.info(f"User {user_id} entered eye color: {eye_color}")
    await update.message.reply_text(get_text(user_id, "last_seen_location", "cases"))
    return State.CREATE_CASE_LAST_SEEN_LOCATION


# == HANDLER: Ask for missing person last seen location  == #
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


# == HANDLER: Ask for missing person height  == #
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


# == HANDLER: Ask for missing person weight  == #
async def handle_weight(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle input for weight."""
    user_id = update.effective_user.id
    weight = update.message.text.strip()

    if not weight.isdigit():
        await update.message.reply_text(
            get_text(user_id, "enter_valid_weight", "cases")
        )
        return State.CREATE_CASE_WEIGHT

    await update_or_create_case(user_id, weight=weight)
    context.user_data["case"]["weight"] = weight
    logger.info(f"User {user_id} entered weight: {weight}")
    await update.message.reply_text(get_text(user_id, "distinctive_features", "cases"))
    return State.CREATE_CASE_DISTINCTIVE_FEATURES


# == HANDLER: Ask for missing person distinctive features  == #
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


# == HANDLER: Ask for missing person reason for finding  == #
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
    if wallet.wallet_type == "SOL":
        await update.message.reply_text(
            get_text(user_id, "enter_reward_amount", "cases").format(
                type=wallet.wallet_type
            )
        )
    elif wallet.wallet_type == "USDT":
        await update.message.reply_text(
            get_text(user_id, "enter_reward_amount", "cases").format(
                type=wallet.wallet_type
            )
        )
    else:
        await update.message.reply_text(
            get_text(user_id, "enter_reward_amount_unknown", "cases")
        )

    return State.CREATE_CASE_ASK_REWARD


# === Handler: Ask Reward Amount ===
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
        await update.message.reply_text(
            get_text(user_id, "reward_amount_invalid", "cases")
        )
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

    # === Insufficient balance case ===
    if wallet_balance < reward_amount:
        msg = (
            "🚫 <b>Insufficient Balance</b>\n\n"
            f"⚠️ Your current balance is {wallet_balance} USDT.\n"
            f"To continue, you’ll need to fund your wallet with {reward_amount} USDT.\n\n"
            "🔐 <b>Your Wallet Address:</b>\n"
            f"<code>{wallet.public_key}</code>\n\n"
            "🌐 Network: TRC20 (Tron Network)\n\n"
            "📥 <b>To top up:</b>\n\n"
            "1️⃣ Open your crypto wallet\n"
            "2️⃣ Select Send\n"
            "3️⃣ Paste your wallet address\n"
            "4️⃣ Select the correct network (TRC20)\n"
            "5️⃣ Enter amount and confirm\n\n"
            "🔁 Once you’ve completed the transfer, press <b>Refresh</b> to update your balance."
        )

        buttons = [
            [
                InlineKeyboardButton(
                    "🔄 Refresh", callback_data=f"refresh_balance:{reward_amount}"
                )
            ],
            [
                InlineKeyboardButton(
                    "🔙 Back", callback_data=f"back_to_reason:{reward_amount}"
                )
            ],
        ]

        await update.message.reply_text(
            msg, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(buttons)
        )
        return State.CREATE_CASE_ASK_REWARD

    # === Balance is OK ===
    case.reward = reward_amount
    await case.save()

    # === CHANGED: Reward < 1000 flow ===
    if reward_amount < 1000:
        if context.user_data.get("increase_reward_mode"):
            context.user_data["increase_reward_mode"] = False
            await update.message.reply_text(
                get_text(user_id, "reward_amount_confirmed", "cases").format(
                    reward_amount
                ),
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "📤 Submit Case", callback_data="submit_case"
                            )
                        ],
                        [InlineKeyboardButton("🔁 Edit", callback_data="edit_case")],
                        [
                            InlineKeyboardButton(
                                "❌ Cancel", callback_data="cancel_case"
                            )
                        ],
                    ]
                ),
            )
            return State.CREATE_CASE_CONFIRM_TRANSFER

        # === CHANGED: Simplified prompt without last-entered amount ===
        msg = (
            f"💸 <b>Reward set to {reward_amount} USDT</b>\n\n"
            "💡 <b>Tip:</b> The higher the reward, the more eyes you attract!\n"
            "Offering a generous reward motivates more people to join the search — "
            "increasing your chances of finding the person faster. 🕵️‍♂️💬\n"
            "A little extra can go a long way in rallying a powerful crowd behind your case."
        )

        buttons = [
            [
                InlineKeyboardButton(
                    "💰 Increase Reward", callback_data="increase_reward"
                )
            ],
            # === CHANGED: Back -> Continue button ===
            [
                InlineKeyboardButton(
                    "✅ Continue", callback_data=f"continue_with_reward:{reward_amount}"
                )
            ],
        ]

        await update.message.reply_text(
            msg, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(buttons)
        )
        return State.CREATE_CASE_ASK_REWARD

    # === CHANGED: For reward >= 1000, show new confirmation screen ===
    await update.message.reply_text(
        "Once the balance is confirmed, your case will be published and shared with the PeopleTrace community.\n\n"
        f"Reward: <b>{reward_amount} USDT</b>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("📤 Submit Case", callback_data="submit_case")],
                [InlineKeyboardButton("🔁 Edit", callback_data="edit_case")],
                [InlineKeyboardButton("❌ Cancel", callback_data="cancel_case")],
            ]
        ),
    )
    return State.CREATE_CASE_CONFIRM_TRANSFER


# # === Handler: Ask Reward Amount ===
# @catch_async
# async def handle_ask_reward_amount(
#     update: Update, context: ContextTypes.DEFAULT_TYPE
# ) -> int:
#     """Handle asking for reward amount and check wallet balance."""
#     user_id = update.effective_user.id
#     text = update.message.text.strip()

#     print(f"[ASK_REWARD] User input: {text}")

#     try:
#         reward_amount = float(text)
#     except ValueError:
#         await update.message.reply_text(
#             get_text(user_id, "reward_amount_invalid", "cases")
#         )
#         return State.CREATE_CASE_ASK_REWARD

#     if reward_amount <= 0:
#         await update.message.reply_text(
#             get_text(user_id, "reward_amount_negative", "cases").format(reward_amount)
#         )
#         return State.CREATE_CASE_ASK_REWARD

#     # Fetch draft case & wallet
#     case = await Case.find_one({"user_id": user_id, "status": CaseStatus.DRAFT})
#     wallet = await case.wallet.fetch()

#     wallet_type = wallet.wallet_type
#     wallet_balance = (
#         await WalletService.get_sol_balance(wallet.public_key)
#         if wallet_type == "SOL"
#         else await TronWallet.get_usdt_balance(wallet.public_key)
#     )

#     # === Insufficient balance case ===
#     if wallet_balance < reward_amount:
#         msg = (
#             "🚫 <b>Insufficient Balance</b>\n\n"
#             f"⚠️ Your current balance is {wallet_balance} USDT.\n"
#             f"To continue, you'll need to fund your wallet with {reward_amount} USDT.\n\n"
#             "🔐 <b>Your Wallet Address:</b>\n"
#             f"<code>{wallet.public_key}</code>\n\n"
#             "🌐 Network: TRC20 (Tron Network)\n\n"
#             "📥 <b>To top up:</b>\n\n"
#             "1️⃣ Open your crypto wallet\n"
#             "2️⃣ Select Send\n"
#             "3️⃣ Paste your wallet address\n"
#             "4️⃣ Select the correct network (TRC20)\n"
#             "5️⃣ Enter amount and confirm\n\n"
#             "🔁 Once you've completed the transfer, press <b>Refresh</b> to update your balance."
#         )

#         buttons = [
#             [
#                 InlineKeyboardButton(
#                     "🔄 Refresh", callback_data=f"refresh_balance:{reward_amount}"
#                 )
#             ],
#             [
#                 InlineKeyboardButton(
#                     "🔙 Back", callback_data=f"back_to_reason:{reward_amount}"
#                 )
#             ],
#         ]

#         await update.message.reply_text(
#             msg, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(buttons)
#         )
#         return State.CREATE_CASE_ASK_REWARD

#     # === Balance is OK ===
#     case.reward = reward_amount
#     await case.save()

#     # === STANDARDIZED CONFIRMATION SCREEN FOR ALL REWARD AMOUNTS ===
#     confirmation_msg = (
#         "Once the balance is confirmed, your case will be published and shared with the PeopleTrace community.\n\n"
#         f"Reward: <b>{reward_amount} USDT</b>"
#     )

#     buttons = [
#         [
#             InlineKeyboardButton(
#                 "📤 Submit Case", callback_data="submit_case"
#             )
#         ],
#         [
#             InlineKeyboardButton(
#                 "🔁 Edit", callback_data="edit_case"
#             )
#         ],
#         [
#             InlineKeyboardButton(
#                 "❌ Cancel", callback_data="cancel_case"
#             )
#         ],
#     ]

#     # === CHANGED: Always show the same confirmation screen regardless of reward amount ===
#     await update.message.reply_text(
#         text=confirmation_msg,
#         parse_mode="HTML",
#         reply_markup=InlineKeyboardMarkup(buttons),
#     )
#     return State.CREATE_CASE_CONFIRM_TRANSFER


# === NEW: Submit Case Handler - Shows Detailed Summary ===
async def handle_submit_case(
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

    if user_input in ["submit_case", "confirm_transfer"]:   # <-- FIX HERE
        try:
            wallet_balance = (
                await WalletService.get_sol_balance(wallet.public_key)
                if wallet.wallet_type == "SOL"
                else await TronWallet.get_usdt_balance(wallet.public_key)
            )

            if wallet.wallet_type in ["USDT", "TRX"] and wallet_balance < reward_amount:
                await query.answer()
                await query.edit_message_text(
                    get_text(user_id, "insurfficient_balance", "cases").format(
                        wallet_balance=wallet_balance,
                        wallet_type=wallet_type,
                        reward_amount=reward_amount,
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
                # platform_fee = round(reward_amount * 0.05, 2)
                # net_escrow = round(reward_amount - platform_fee, 2)

                # advertiser_message = get_text(
                #     user_id, "congratulates_advertiser", "cases"
                # ).format(
                #     reward_amount=reward_amount,
                #     wallet_type=wallet_type,
                #     case_name=case.person_name or "Unknown",
                #     location=case.city or "Unknown",
                #     platform_fee=platform_fee,
                #     net_amount=net_escrow,
                # )

                # Calculate fees
                platform_fee = round(case.reward * 0.05, 2)
                net_escrow = round(case.reward - platform_fee, 2)

                # Format location properly - handle all possible combinations
                location_parts = []
                if case.city:
                    location_parts.append(case.city)
                if case.province:
                    location_parts.append(case.province)
                if case.country:
                    location_parts.append(case.country)

                location = ", ".join(location_parts) if location_parts else "Not specified"

                # Create detailed summary message with proper HTML formatting
                advertiser_message = (
                    "🎉 <b>Congratulations!</b> Your case has been submitted to the PeopleTrace community.\n\n"
                    "<b>Summary of Submission:</b>\n\n"
                    f"• Case Name: {case.person_name or 'Unknown'}\n"
                    f"• Location: {location}\n"
                    f"• Reward Offered: {case.reward} USDT\n"
                    f"• Platform Fee (5%): {platform_fee} USDT\n"
                    f"• Net Held in Escrow: <b>{net_escrow} USDT</b>\n\n"
                    "🔒 Your reward is securely held in escrow and will be released only upon verified, successful leads.\n\n"
                    "✅ Your case has been published to the PeopleTrace community!"
                )

                # Buttons for post-submission actions
                buttons = [
                    [InlineKeyboardButton("✏️ Edit Case", callback_data="edit_published_case")],
                    [InlineKeyboardButton("❌ Cancel Case", callback_data="cancel_published_case")],
                    [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")],
                ]

                # ✅ Send message to advertiser
                await context.bot.send_message(
                    chat_id=user_id,
                    text=advertiser_message,
                    parse_mode="HTML",
                    reply_markup=InlineKeyboardMarkup(buttons)
                )

                # ✅ Send message to owner
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
                context.user_data["case"] = case  # keep case reference for edits

                return State.POST_SUBMISSION_MENU


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

    else:
        await query.answer()
        await query.edit_message_text(
            get_text(user_id, "invalid_choice", "cases"), parse_mode="HTML"
        )
        return State.CREATE_CASE_CONFIRM_TRANSFER





# === NEW: Cancel Case Selection Handler ===
@catch_async
async def handle_cancel_case(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Cancels (deletes) the user's draft case."""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    case = await Case.find_one({"user_id": user_id, "status": CaseStatus.DRAFT})

    if case:
        await case.delete()   # make sure delete is awaited
        await query.edit_message_text("✅ Your draft case has been deleted.")
    else:
        await query.edit_message_text("⚠️ No draft case found to delete.")

    await start(update, context)




# === NEW: Cancel Case Selection Handler ===
@catch_async
async def handle_cancel_case_selection(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Show cancellation reason options when user selects 'Cancel Case'."""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    case = await Case.find_one({"user_id": user_id, "status": CaseStatus.DRAFT})

    if not case:
        await query.edit_message_text("❌ Case not found. Please start over.")
        return State.MAIN_MENU

    # Store case ID in context for later use
    context.user_data["cancel_case_id"] = str(case.id)

    # Show cancellation reason options
    cancel_msg = (
        "❗ <b>You are about to cancel this case.</b>\n"
        "Please tell us the reason for cancellation:\n\n"
        "<i>Your reason will be recorded for review. Cases submitted in bad faith may result in a ban.</i>"
    )

    buttons = [
        [
            InlineKeyboardButton(
                "✅ Found the person", callback_data="cancel_reason:found"
            )
        ],
        [
            InlineKeyboardButton(
                "🕒 No longer relevant", callback_data="cancel_reason:irrelevant"
            )
        ],
        [
            InlineKeyboardButton(
                "❌ Posted by mistake", callback_data="cancel_reason:mistake"
            )
        ],
        [
            InlineKeyboardButton(
                "📝 Other", callback_data="cancel_reason:other"
            )
        ],
    ]

    await query.edit_message_text(
        text=cancel_msg,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

    return State.CASE_CANCEL_SELECT_REASON


# === NEW: Cancellation Reason Handler ===
@catch_async
async def handle_cancel_reason(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Process selected cancellation reason or prompt for custom reason."""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = query.data.split(":")[1] if len(query.data.split(":")) > 1 else ""

    if data == "other":
        # Prompt for custom reason
        await query.edit_message_text(
            text="✍️ Please type your reason for cancellation:",
            parse_mode="HTML"
        )
        return State.CASE_CANCEL_ENTER_REASON

    # Process predefined reason
    return await _process_cancel_reason(update, context, data)


# === NEW: Custom Reason Handler ===
@catch_async
async def handle_custom_cancel_reason(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Process custom cancellation reason entered by user."""
    user_id = update.effective_user.id
    text = update.message.text.strip()

    # Process the custom reason
    return await _process_cancel_reason(update, context, "custom", text)


# === Helper: Process Cancellation Reason ===
async def _process_cancel_reason(
    update: Update, context: ContextTypes.DEFAULT_TYPE, reason_type: str, custom_reason: str = None
) -> int:
    """Common logic to process cancellation reason and update case."""
    user_id = update.effective_user.id
    query = update.callback_query if update.callback_query else None

    # Get case ID from context
    case_id = context.user_data.get("cancel_case_id")
    if not case_id:
        if query:
            await query.edit_message_text("❌ Error: Case ID not found.")
        else:
            await update.message.reply_text("❌ Error: Case ID not found.")
        return State.MAIN_MENU

    # Get the case
    case = await Case.get(case_id)
    if not case:
        if query:
            await query.edit_message_text("❌ Case not found.")
        else:
            await update.message.reply_text("❌ Case not found.")
        return State.MAIN_MENU

    # Determine cancel reason text
    reason_map = {
        "found": "Found the person",
        "irrelevant": "No longer relevant",
        "mistake": "Posted by mistake",
        "other": "Other"
    }

    if reason_type == "custom":
        cancel_reason = custom_reason
    else:
        cancel_reason = reason_map.get(reason_type, "Other")

    # Update case with cancellation reason
    case.status = CaseStatus.CANCELLED
    case.cancel_reason = cancel_reason
    await case.save()

    # Calculate fee deduction
    platform_fee = round(case.reward * 0.05, 2) if case.reward else 0

    # Create confirmation message
    confirmation_msg = (
        "✅ <b>Thank you. Your case has been cancelled.</b>\n\n"
        f"⛔ A 5% admin fee ({platform_fee} USDT) has been deducted from your escrow balance. "
        "Remaining balance will be transferred to your wallet in 24-48 hours."
    )

    # Show confirmation message
    if query:
        await query.edit_message_text(
            text=confirmation_msg,
            parse_mode="HTML"
        )
    else:
        await update.message.reply_text(
            text=confirmation_msg,
            parse_mode="HTML"
        )

    return State.MAIN_MENU


# === Callback Handler: Continue with smaller reward ===
@catch_async
async def handle_continue_with_reward(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Proceed to confirmation even if reward < 1000."""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    reward_amount = float(query.data.split(":")[1])

    await query.edit_message_text(
        text="Once the balance is confirmed, your case will be published and shared with the PeopleTrace community.\n\n"
             f"Reward: <b>{reward_amount} USDT</b>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📤 Submit Case", callback_data="submit_case"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🔁 Edit", callback_data="edit_case"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "❌ Cancel", callback_data="cancel_case"
                    )
                ],
            ]
        ),
    )
    return State.CREATE_CASE_CONFIRM_TRANSFER


# === Callback Handler: Going Back ===
@catch_async
async def handle_back_to_reason(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Re-prompt user for reward amount (simplified version)"""
    query = update.callback_query
    await query.answer()

    # === CHANGED: Removed last-entered amount display ===
    msg = (
        "💰 <b>Reward Setup</b>\n\n"
        "What reward would you like to offer for verified leads? (in USDT)"
    )

    await query.edit_message_text(text=msg, parse_mode="HTML")
    return State.CREATE_CASE_ASK_REWARD

# === Callback Handler: Refresh Balance ===
@catch_async
async def handle_refresh_balance(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Re-check wallet balance when user presses Refresh button."""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = query.data.split(":")
    reward_amount = float(data[1]) if len(data) > 1 else 0

    # Get draft case & wallet
    case = await Case.find_one({"user_id": user_id, "status": CaseStatus.DRAFT})
    wallet = await case.wallet.fetch()

    wallet_type = wallet.wallet_type
    wallet_balance = (
        await WalletService.get_sol_balance(wallet.public_key)
        if wallet_type == "SOL"
        else await TronWallet.get_usdt_balance(wallet.public_key)
    )

    if wallet_balance < reward_amount:
        await query.edit_message_text(
            text=(
                "🚫 <b>Insufficient Balance</b>\n\n"
                f"⚠️ Your current balance is {wallet_balance} USDT.\n"
                f"You still need at least {reward_amount} USDT to continue.\n\n"
                "🔁 Please top up and press Refresh again."
            ),
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔄 Refresh",
                            callback_data=f"refresh_balance:{reward_amount}",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "🔙 Back", callback_data=f"back_to_reason:{reward_amount}"
                        )
                    ],
                ]
            ),
        )
        return State.CREATE_CASE_ASK_REWARD

    # ✅ Balance now sufficient
    case.reward = reward_amount
    await case.save()

    await query.edit_message_text(
        text=get_text(user_id, "reward_amount_confirmed", "cases").format(
            reward_amount
        ),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        get_text(user_id, "confirm_button", "globals"),
                        callback_data="confirm_transfer",
                    ),
                    InlineKeyboardButton(
                        get_text(user_id, "cancel_edit_button", "globals"),
                        callback_data="cancel_transfer",
                    ),
                ]
            ]
        ),
    )
    return State.CREATE_CASE_CONFIRM_TRANSFER


# === Callback Handler: Increase Reward ===
@catch_async
async def handle_increase_reward(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Let user input a higher reward again."""
    query = update.callback_query
    await query.answer()

    # Set flag so next input is treated as increase reward
    # context.user_data["increase_reward_mode"] = True

    msg = (
        "💰 <b>Reward Setup</b>\n\n"
        "Please enter a new (higher) reward amount in USDT."
    )

    await query.edit_message_text(text=msg, parse_mode="HTML")
    return State.CREATE_CASE_ASK_REWARD


# == HANDLER: just show the details when i submitted what you enter of each field after that allowing to submit   == #
async def handle_publish_case(
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
                    get_text(user_id, "insurfficient_balance", "cases").format(
                        wallet_balance=wallet_balance,
                        wallet_type=wallet_type,
                        reward_amount=reward_amount,
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

    else:
        await query.answer()
        await query.edit_message_text(
            get_text(user_id, "invalid_choice", "cases"), parse_mode="HTML"
        )
        return State.CREATE_CASE_CONFIRM_TRANSFER

# === NEW: Edit Case Handler ===
@catch_async
async def handle_edit_case(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Allow user to edit the case details."""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    case = await Case.find_one({"user_id": user_id, "status": CaseStatus.DRAFT})

    if not case:
        await query.edit_message_text("❌ Case not found. Please start over.")
        return State.MAIN_MENU

    # Go back to reason input step
    await query.edit_message_text(
        text="✏️ <b>Edit Case Details</b>\n\n"
             "What is the reason for creating this case?",
        parse_mode="HTML"
    )
    return State.CREATE_CASE_ASK_REASON



##!SECTION -   When user publish the case and what to edit it or cancel after published
@catch_async
async def handle_edit_published_case(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle request to edit a published case."""
    query = update.callback_query
    await query.answer()

    # For now, just notify the user it’s under development
    await query.edit_message_text(
        "✏️ Editing a published case is under development. Stay tuned!"
    )
    return State.POST_SUBMISSION_MENU


@catch_async
async def handle_cancel_published_case(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle request to cancel a published case."""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "❌ Case cancellation is under development. You will soon be able to cancel your active case."
    )
    return State.POST_SUBMISSION_MENU


@catch_async
async def handle_back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Return the user back to the main menu."""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "🔙 Returning to the main menu...", parse_mode="HTML"
    )
    # TODO: replace with your main menu handler
    return State.MAIN_MENU
