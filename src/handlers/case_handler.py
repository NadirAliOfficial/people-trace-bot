import re
from config.config_manager import (
    CLIENT,
    OWNER_TELEGRAM_ID,
    STAKE_WALLET_PUBLIC_KEY,
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


# --- Create Case Handlers (with separate states for each person detail) ---


async def handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the user's name input."""
    user_id = update.effective_user.id
    name = update.message.text.strip()
    await update_or_create_case(user_id, name=name)
    context.user_data["case"] = {"name": name}

    # Check if the user has existing mobile numbers
    existing_mobiles = await get_user_mobiles(user_id)

    if existing_mobiles:
        # Show existing mobile numbers with an option to select one
        kb = [
            [InlineKeyboardButton(mobile, callback_data=f"select_mobile_{mobile}")]
            for mobile in existing_mobiles
        ]
        kb.append([InlineKeyboardButton("➕ Add New", callback_data="mobile_add")])
        await update.message.reply_text(
            get_text(user_id, "choose_existing_mobile"),
            reply_markup=InlineKeyboardMarkup(kb),
        )
        return State.MOBILE_MANAGEMENT
    else:
        # Ask for a new mobile number if none exists
        await update.message.reply_text(get_text(user_id, "enter_mobile"))
        return State.CREATE_CASE_MOBILE


async def handle_select_mobile(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle the selection of an existing mobile number or adding a new one."""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "mobile_add":
        # Handle 'Add New' click: Ask the user to input a new mobile number
        await query.edit_message_text(get_text(user_id, "enter_mobile"))
        return State.CREATE_CASE_MOBILE  # Transition to state for mobile number input
    else:
        selected_mobile = query.data.replace("select_mobile_", "")

        # Fetch the MobileNumber reference from the database
        mobile_number = await MobileNumber.find_one({"number": selected_mobile})

        if not mobile_number:
            await query.edit_message_text(
                "The selected mobile number does not exist in the database. Please try again."
            )
            return State.CREATE_CASE_MOBILE

        # Store the mobile number reference in user_data for further use
        context.user_data["mobile"] = selected_mobile
        context.user_data["selected_number"] = (
            selected_mobile  # Save the MobileNumber reference
        )

        res = await send_otp(selected_mobile)

        context.user_data["case"]["otp_id"] = res["otp_id"]

        # Notify the user that the mobile number was selected
        await query.edit_message_text(
            f"Selected mobile number: {selected_mobile} - A TAC is sent to you on this number"
        )

        # Proceed to the next step
        await query.message.reply_text(get_text(user_id, "enter_tac"))
        return State.CREATE_CASE_TAC


async def handle_new_mobile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the input of a new mobile number."""
    user_id = update.effective_user.id
    mobile_number = update.message.text.strip()

    if re.match(r"^\+?\d{10,15}$", mobile_number):  # Basic validation for mobile number
        context.user_data["mobile"] = mobile_number

        context.user_data["selected_number"] = mobile_number
        # Update or create the case with the new mobile number
        print(f"Mobile number: {mobile_number}")

        tac = generate_tac()  # Generate TAC for the new mobile number
        context.user_data["tac"] = tac
        print(f"Tac are: {tac}")

        res = await send_otp(mobile_number)

        context.user_data["case"]["otp_id"] = res["otp_id"]

        await update.message.reply_text(
            f"Mobile number {mobile_number} added. A TAC has been sent to your number."
        )

        # Proceed to the next step: Enter the TAC
        await update.message.reply_text(get_text(user_id, "enter_tac"))
        return State.CREATE_CASE_TAC
    else:
        # If invalid, prompt the user to enter a valid mobile number format
        await update.message.reply_text(get_text(user_id, "enter_valid_mobile"))
        return State.CREATE_CASE_MOBILE


async def handle_tac(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle TAC verification."""
    user_id = update.effective_user.id
    user_tac = update.message.text.strip()
    stored_tac = context.user_data.get("tac")
    selected_number = context.user_data.get("selected_number")

    otp_verify = await verify_otp(context.user_data["case"]["otp_id"], user_tac)
    if otp_verify["success"]:
        await update.message.reply_text(get_text(user_id, "tac_verified"))

        # After TAC verification, update the case with the mobile reference
        await update_or_create_case(user_id, mobile=selected_number)

        # Proceed to the next step
        await show_disclaimer_2(update, context)
        return State.CREATE_CASE_DISCLAIMER
    else:
        await update.message.reply_text(get_text(user_id, "tac_invalid"))
        return State.CREATE_CASE_TAC


async def show_disclaimer_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show Disclaimer 2."""
    user_id = update.effective_user.id
    kb = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    get_text(user_id, "agree_btn"), callback_data="agree"
                )
            ],
            [
                InlineKeyboardButton(
                    get_text(user_id, "disagree_btn"), callback_data="disagree"
                )
            ],
        ]
    )
    await update.message.reply_text(get_text(user_id, "disclaimer_2"), reply_markup=kb)
    return State.CREATE_CASE_DISCLAIMER


async def disclaimer_2_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle Disclaimer 2 agreement."""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "agree":

        await query.edit_message_text("Please enter the person's name.")
        return State.CREATE_CASE_PERSON_NAME
    else:
        await query.edit_message_text(get_text(user_id, "disagree_end"))
        return State.END


async def handle_person_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle input for the person's name (the case target)."""
    user_id = update.effective_user.id
    person_name = update.message.text.strip()
    await update_or_create_case(user_id, person_name=person_name)
    context.user_data["case"]["person_name"] = person_name
    logger.info(f"User {user_id} entered person name: {person_name}")
    await update.message.reply_text(get_text(user_id, "relationship"))
    return State.CREATE_CASE_RELATIONSHIP


async def handle_relationship(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle input for relationship detail."""
    user_id = update.effective_user.id
    relationship = update.message.text.strip()
    await update_or_create_case(user_id, relationship=relationship)
    context.user_data["case"]["relationship"] = relationship
    logger.info(f"User {user_id} entered relationship: {relationship}")

    await update.message.reply_text(get_text(user_id, "upload_photo"))
    return State.CREATE_CASE_PHOTO


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle photo upload and store it on Cloudinary."""
    user_id = update.effective_user.id

    # Check if the user sent a photo
    if not update.message.photo:
        await update.message.reply_text(get_text(user_id, "no_photo_found"))
        return State.CREATE_CASE_PHOTO

    # Get the highest quality photo from the list (the last element)
    photo_file = await update.message.photo[-1].get_file()

    # Define the absolute path for the photos directory
    photo_dir = os.path.join(os.getcwd(), "photos")

    # Create the directory if it doesn't exist
    os.makedirs(photo_dir, exist_ok=True)

    # Define the path to save the photo
    photo_path = os.path.join(photo_dir, f"{user_id}_photo.jpg")

    # Debug log for the path
    logger.info(f"Saving photo at path: {photo_path}")

    # Download the photo to the server
    await photo_file.download_to_drive(photo_path)

    # Upload the photo to Cloudinary
    upload_result = await upload_image(photo_path)
    if upload_result:
        logger.info(f"Uploaded Photo URL: {upload_result}")

        await update_or_create_case(user_id, case_photo=upload_result)
        context.user_data["case"][
            "photo_url"
        ] = upload_result  # Store URL instead of local path

    # Move to the next step (e.g., last seen location)
    await update.message.reply_text(get_text(user_id, "last_seen_location"))
    return State.CREATE_CASE_LAST_SEEN_LOCATION


async def handle_last_seen_location(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle input for last seen location."""
    user_id = update.effective_user.id
    location = update.message.text.strip()
    await update_or_create_case(user_id, last_seen_location=location)
    context.user_data["case"]["last_seen_location"] = location
    logger.info(f"User {user_id} entered last seen location: {location}")

    # Provide options for sex
    kb = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Male", callback_data="male"),
                InlineKeyboardButton("Female", callback_data="female"),
            ],
            [
                InlineKeyboardButton("Other", callback_data="other"),
            ],
        ]
    )
    await update.message.reply_text(get_text(user_id, "sex"), reply_markup=kb)
    return State.CREATE_CASE_SEX


async def handle_sex(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle input for sex."""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    sex = query.data
    await update_or_create_case(user_id, gender=sex)
    context.user_data["case"]["sex"] = sex
    logger.info(f"User {user_id} selected sex: {sex}")
    await query.edit_message_text(get_text(user_id, "age"))
    return State.CREATE_CASE_AGE


async def handle_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle input for age."""
    user_id = update.effective_user.id
    age = update.message.text.strip()

    if not age.isdigit():
        await update.message.reply_text("Please enter a valid number for age.")
        return State.CREATE_CASE_AGE

    await update_or_create_case(user_id, age=age)
    context.user_data["case"]["age"] = age
    logger.info(f"User {user_id} entered age: {age}")
    await update.message.reply_text(get_text(user_id, "hair_color"))
    return State.CREATE_CASE_HAIR_COLOR


async def handle_hair_color(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle input for hair color."""
    user_id = update.effective_user.id
    hair_color = update.message.text.strip()
    await update_or_create_case(user_id, hair_color=hair_color)
    context.user_data["case"]["hair_color"] = hair_color
    logger.info(f"User {user_id} entered hair color: {hair_color}")
    await update.message.reply_text(get_text(user_id, "eye_color"))
    return State.CREATE_CASE_EYE_COLOR


async def handle_eye_color(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle input for eye color."""
    user_id = update.effective_user.id
    eye_color = update.message.text.strip()
    await update_or_create_case(user_id, eye_color=eye_color)
    context.user_data["case"]["eye_color"] = eye_color
    logger.info(f"User {user_id} entered eye color: {eye_color}")
    await update.message.reply_text(get_text(user_id, "height"))
    return State.CREATE_CASE_HEIGHT


async def handle_height(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle input for height."""
    user_id = update.effective_user.id
    height = update.message.text.strip()

    if not height.isdigit():
        await update.message.reply_text("Please enter a valid number for height.")
        return State.CREATE_CASE_HEIGHT

    await update_or_create_case(user_id, height=height)
    context.user_data["case"]["height"] = height
    logger.info(f"User {user_id} entered height: {height}")
    await update.message.reply_text(get_text(user_id, "weight"))
    return State.CREATE_CASE_WEIGHT


async def handle_weight(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle input for weight."""
    user_id = update.effective_user.id
    weight = update.message.text.strip()

    if not weight.isdigit():
        await update.message.reply_text("Please enter a valid number for weight.")
        return State.CREATE_CASE_WEIGHT

    await update_or_create_case(user_id, weight=weight)
    context.user_data["case"]["weight"] = weight
    logger.info(f"User {user_id} entered weight: {weight}")
    await update.message.reply_text(get_text(user_id, "distinctive_features"))
    return State.CREATE_CASE_DISTINCTIVE_FEATURES


async def handle_distinctive_features(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle input for distinctive features."""
    user_id = update.effective_user.id
    features = update.message.text.strip()

    await update_or_create_case(user_id, distinctive_features=features)
    context.user_data["case"]["distinctive_features"] = features
    logger.info(f"User {user_id} entered distinctive features: {features}")
    await update.message.reply_text(get_text(user_id, "reason_for_finding"))
    return State.CREATE_CASE_ASK_REASON


# Handlers for each state
async def handle_reason_for_finding(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle input for reason for finding and ask for reward amount."""
    user_id = update.effective_user.id
    reason = update.message.text.strip()

    # Fetch the case for the user
    case = await Case.find_one(
        {"user_id": user_id, "status": CaseStatus.DRAFT}, fetch_links=True
    )

    if not case:
        await update.message.reply_text(get_text(user_id, "case_not_found"))
        return State.END

    # Store reason in case and ask for reward amount
    case.reason = reason
    await case.save()

    print(f"Case: {case}")

    # Ask for reward amount based on the wallet type (SOL or USDT)
    wallet = case.wallet
    if wallet.wallet_type == "SOL":
        await update.message.reply_text(get_text(user_id, "enter_reward_amount_sol"))
    elif wallet.wallet_type == "USDT":
        await update.message.reply_text(get_text(user_id, "enter_reward_amount_usdt"))
    else:
        await update.message.reply_text(
            get_text(user_id, "enter_reward_amount_unknown")
        )

    return State.CREATE_CASE_ASK_REWARD


# Handlers for each state


async def handle_ask_reward_amount(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle asking for reward amount and check wallet balance."""
    user_id = update.effective_user.id
    print(f"I am calling from the ask reward amount handler")
    reward_amount = float(update.message.text.strip())  # User's input as float

    # Fetch the case and wallet info
    case = await Case.find_one({"user_id": user_id, "status": CaseStatus.DRAFT})
    wallet = await case.wallet.fetch()

    print(f"Wallet: {wallet}")

    # Get wallet balance (assuming you have a method to fetch balance)
    wallet_balance = (
        await WalletService.get_sol_balance(wallet.public_key)
        if wallet.wallet_type == "SOL"
        else await TronWallet.get_usdt_balance(wallet.public_key)
    )

    print(f"Wallet balance: {wallet_balance}")

    # Check if the reward amount is greater than available balance
    if reward_amount < 0:
        await update.message.reply_text(
            get_text(user_id, "reward_amount_negative").format(reward_amount)
        )
        return State.CREATE_CASE_ASK_REWARD

    if wallet_balance < reward_amount:
        await update.message.reply_text(
            get_text(user_id, "insufficient_balance").format(wallet_balance)
        )
        await update.message.reply_text(get_text(user_id, "refresh_wallet_balance"))
        return State.CREATE_CASE_ASK_REWARD

    # If balance is sufficient, save the reward amount in the case
    case.reward = reward_amount
    await case.save()

    # Confirm the reward amount and proceed with a button
    await update.message.reply_text(
        get_text(user_id, "reward_amount_confirmed").format(reward_amount),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Confirm", callback_data="confirm_transfer"),
                    InlineKeyboardButton("Cancel", callback_data="cancel_transfer"),
                ]
            ]
        ),
    )

    return State.CREATE_CASE_CONFIRM_TRANSFER


@catch_async
async def handle_transfer_confirmation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle confirmation of the reward transfer."""
    user_id = update.effective_user.id
    query = update.callback_query
    user_input = query.data.strip().lower()

    # Fetch the case to retrieve reward amount and wallet info
    print("Calling in handle transfer confirmation")
    case = await Case.find_one(
        {"user_id": user_id, "status": CaseStatus.DRAFT}, fetch_links=True
    )
    print(case)
    wallet = case.wallet
    reward_amount = case.reward
    wallet_type = wallet.wallet_type
    print("------------------------------------")
    print(f"Wallet: {wallet}")
    print(f"Case: {case}")
    print(f"Wallet Type: {wallet_type}")

    if user_input == "confirm_transfer":
        # Proceed with the transfer
        try:
            # Check if wallet has sufficient balance
            wallet_balance = (
                await WalletService.get_sol_balance(wallet.public_key)
                if wallet.wallet_type == "SOL"
                else await TronWallet.get_usdt_balance(wallet.public_key)
            )

            print(f"Wallet Balance: {wallet_balance}")

            if wallet.wallet_type in ["USDT", "TRX"] and wallet_balance < reward_amount:
                await query.answer()
                await query.edit_message_text(
                    get_text(user_id, "insufficient_balance_for_transfer").format(
                        wallet_balance=wallet_balance,
                        reward_amount=reward_amount,
                        wallet_type=wallet_type,
                    )
                )
                return State.CREATE_CASE_CONFIRM_TRANSFER

            # Transfer the reward (this is just a placeholder, you need to implement transfer logic)
            transfer_success = False
            print(f"Transfer to owner: {wallet.public_key}")
            print(f"Reward amount: {reward_amount}")

            transfer_success = (
                await WalletService.send_sol(
                    wallet.private_key, STAKE_WALLET_PUBLIC_KEY, reward_amount
                )
                if wallet.wallet_type == "SOL"
                else await TronWallet.transfer_usdt(
                    wallet.private_key, TRON_WALLET_PUBLIC_KEY, reward_amount
                )
            )

            print("Getting the balance of the wallet")
            print(f"Transfer_success: {transfer_success}")

            print(f"Debug No: 1", transfer_success)
            if transfer_success:
                # Notify the advertiser
                advertiser_message = (
                    f"🎉 Congratulations! Your advertisement has been successfully processed.\n\n"
                    f"Case ID: {case.id}\n"
                    f"Reward Amount: {reward_amount} {wallet_type}\n"
                    f"Wallet Type: {wallet_type}\n\n"
                    f"Thank you for choosing our platform!"
                )
                await query.message.reply_text(advertiser_message)

                print(f"Debug No: 2")

                # Notify the owner
                owner_message = (
                    f"📢 **New Advertisement Notification**\n\n"
                    f"🎯 **A new case has been successfully advertised!**\n\n"
                    f"🆔 **Advertiser ID:** {user_id}\n"
                    f"📄 **Case ID:** {case.id}\n"
                    f"💰 **Reward Amount:** {reward_amount} {wallet_type}\n"
                    f"🔒 **Wallet Type:** {wallet_type}\n\n"
                    f"✅ **The funds have been securely transferred.**\n"
                    f"📋 Use `/listing` to view all available cases."
                )

                await context.bot.send_message(
                    chat_id=OWNER_TELEGRAM_ID, text=owner_message
                )

                # Update case status
                case.status = CaseStatus.ADVERTISE
                await case.save()

                # Clear user data
                context.user_data["case"] = None

                return State.END
            else:
                await query.answer()
                await query.edit_message_text(get_text(user_id, "transfer_failed"))
        except Exception as e:
            print(f"Transfer failed: {e}")
            await query.answer()
            await query.edit_message_text(get_text(user_id, "transfer_error"))

    elif user_input == "cancel_transfer":
        await query.answer()
        await query.edit_message_text(get_text(user_id, "transfer_canceled"))
        return State.CREATE_CASE_ASK_REWARD

    else:
        await query.answer()
        await query.edit_message_text(get_text(user_id, "invalid_confirmation"))
        return State.CREATE_CASE_CONFIRM_TRANSFER


# async def handle_case_finished(
#     update: Update, context: ContextTypes.DEFAULT_TYPE
# ) -> int:
#     """Handle the case completion state."""
#     user_id = update.effective_user.id
#     await update.message.reply_text(get_text(user_id, "case_completed"))
#     return State.CREATE_CASE_FINISHED
