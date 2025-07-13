import re
from config.config_manager import (
    CLIENT,
    NODE_ENV,
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

# ---------------------------- Case Mobile Number  Start ---------------------------

  



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
            get_text(user_id, "enter_mobile_post_case"), 
            parse_mode="Markdown"
        )        
        return State.CREATE_CASE_MOBILE  
    else:
        selected_mobile = query.data.replace("select_mobile_", "")

        mobile_number = await MobileNumber.find_one({"number": selected_mobile})

        if not mobile_number:
            await query.edit_message_text(get_text(user_id, "mobile_number_doesnt_exist"))
            return State.CREATE_CASE_MOBILE

        context.user_data["mobile"] = selected_mobile
        context.user_data["selected_number"] = (
            selected_mobile  
        )

        if NODE_ENV == "production":
            res = await send_otp(selected_mobile)
            print(f"Response would be :{res}")
            context.user_data["case"]["otp_id"] = res["otp_id"]
        else: 
            context.user_data["case"]["otp_id"] = "dummy_otp_id"
            print(f"Skipping OTP sending in {NODE_ENV} mode.")
        
        await query.edit_message_text(
            get_text(user_id, "mobile_selected_with_tac").format(mobile_number=selected_mobile)
        )

        # Proceed to the next step
        await query.message.reply_text(get_text(user_id, "enter_tac"))
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
            print(f"Tac are: {tac}")


            res = await send_otp(mobile_number)

            print(f"Getting the otp: ${res}")

            context.user_data["case"]["otp_id"] = res["otp_id"]

            await update.message.reply_text(
                get_text(user_id, "mobile_selected_with_tac").format(mobile_number=mobile_number)
            )
        else: 
            context.user_data["case"]["otp_id"] = "dummy_otp_id"
            print(f"Skipping OTP sending in {NODE_ENV} mode.")
            

        await update.message.reply_text(get_text(user_id, "enter_tac"))
        return State.CREATE_CASE_TAC
    else:
        await update.message.reply_text(get_text(user_id, "enter_valid_mobile"))
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
            await update.message.reply_text(get_text(user_id, "tac_verified"))

            # After TAC verification, update the case with the mobile reference
            await update_or_create_case(user_id, mobile=selected_number)
            kb =[]

            kb.append([
                InlineKeyboardButton("💵 USDT (TRC20 - Tron Network)", callback_data="USDT"),
                InlineKeyboardButton("⚡ Solana (SOL)", callback_data="SOL"),
            ])

            markup = InlineKeyboardMarkup(kb)
            
            await update.message.reply_text(
                "💼 Before posting your case, you’ll need a crypto wallet for the reward bounty. Please choose a wallet type to proceed:",
                        reply_markup=markup,
                        parse_mode="HTML",
                    )
            return State.CHOOSE_WALLET_TYPE
            # # Proceed to the next step
            # await show_disclaimer_2(update, context)
            
            # return State.CREATE_CASE_DISCLAIMER
        else:
            await update.message.reply_text(get_text(user_id, "tac_invalid"))
            return State.CREATE_CASE_TAC
    else: 
        print(f"Skipping OTP verification in {NODE_ENV} mode.")
        await update.message.reply_text(get_text(user_id, "tac_verified"))
        kb =[]

        kb.append([
            InlineKeyboardButton("💵 USDT (TRC20 - Tron Network)", callback_data="USDT"),
            InlineKeyboardButton("⚡ Solana (SOL)", callback_data="SOL"),
        ])
        markup = InlineKeyboardMarkup(kb)
        
        await update.message.reply_text(
            "💼 Before posting your case, you’ll need a crypto wallet for the reward bounty. Please choose a wallet type to proceed:",
                    reply_markup=markup,
                    parse_mode="HTML",
                )
        return State.CHOOSE_WALLET_TYPE
        # await show_disclaimer_2(update, context)


# ---------------------- Case Mobile Number End ----------------------


async def show_disclaimer_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show Disclaimer 2."""
    user_id = update.effective_user.id
    kb = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    get_text(user_id, "understood_and_agree"), callback_data="agree"
                )
            ],
            [
                InlineKeyboardButton(
                    get_text(user_id, "cancel_button"), callback_data="disagree"
                )
            ],
        ]
    )
    await update.message.reply_text(get_text(user_id, "disclaimer_2"), reply_markup=kb, parse_mode="Markdown")
    return State.CREATE_CASE_DISCLAIMER


async def disclaimer_2_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle Disclaimer 2 agreement."""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "agree":

        await query.edit_message_text(get_text(user_id, "enter_person_name"))
        return State.CREATE_CASE_PERSON_NAME
    else:
        await query.edit_message_text(get_text(user_id, "disagree_end"))
        return State.END


#__________________________ COMPLAINT DETAILS__________________________


# _________ PERSON   
async def handle_person_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle input for the person's name (the case target)."""
    user_id = update.effective_user.id
    person_name = update.message.text.strip()
    await update_or_create_case(user_id, person_name=person_name)
    context.user_data["case"]["person_name"] = person_name
    logger.info(f"User {user_id} entered person name: {person_name}")
    kb = InlineKeyboardMarkup([[InlineKeyboardButton(get_text(user_id, "male_option"), callback_data="male"), InlineKeyboardButton(get_text(user_id, "female_option"), callback_data="female")]])
    await update.message.reply_text(get_text(user_id, "sex"), reply_markup=kb)
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
    await query.edit_message_text(get_text(user_id, "age"))
    return State.CREATE_CASE_AGE


# _________ AGE OF THE PERSON 
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
    await update.message.reply_text(get_text(user_id, "relationship"))
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

    await update.message.reply_text(get_text(user_id, "upload_photo"))
    return State.CREATE_CASE_PHOTO


# _________ PHOTO OF HIS/HER
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle photo upload and store it on Cloudinary."""
    user_id = update.effective_user.id

    if not update.message.photo:
        await update.message.reply_text(get_text(user_id, "no_photo_found"))
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

    await update.message.reply_text(get_text(user_id, "hair_color"))
    return State.CREATE_CASE_HAIR_COLOR



# _________ HAIR COLOR OF THE PERSON 
async def handle_hair_color(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle input for hair color."""
    user_id = update.effective_user.id
    hair_color = update.message.text.strip()
    await update_or_create_case(user_id, hair_color=hair_color)
    context.user_data["case"]["hair_color"] = hair_color
    logger.info(f"User {user_id} entered hair color: {hair_color}")
    await update.message.reply_text(get_text(user_id, "eye_color"))
    return State.CREATE_CASE_EYE_COLOR

# _________ EYE COLOR OF THE PERSON 
async def handle_eye_color(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle input for eye color."""
    user_id = update.effective_user.id
    eye_color = update.message.text.strip()
    await update_or_create_case(user_id, eye_color=eye_color)
    context.user_data["case"]["eye_color"] = eye_color
    logger.info(f"User {user_id} entered eye color: {eye_color}")
    await update.message.reply_text(get_text(user_id, "last_seen_location"))
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

    await update.message.reply_text(get_text(user_id, "height"))
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
    await update.message.reply_text(get_text(user_id, "weight"))
    return State.CREATE_CASE_WEIGHT

# _________ WEIGHT OF THE PERSON
async def handle_weight(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle input for weight."""
    user_id = update.effective_user.id
    weight = update.message.text.strip()

    if not weight.isdigit():
        await update.message.reply_text(get_text(user_id, "enter_valid_weight"))
        return State.CREATE_CASE_WEIGHT

    await update_or_create_case(user_id, weight=weight)
    context.user_data["case"]["weight"] = weight
    logger.info(f"User {user_id} entered weight: {weight}")
    await update.message.reply_text(get_text(user_id, "distinctive_features"))
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
    await update.message.reply_text(get_text(user_id, "reason_for_finding"))
    return State.CREATE_CASE_ASK_REASON


# _________ REASON OF FINDING 
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
        await update.message.reply_text(get_text(user_id, "case_not_found"))
        return State.END

    case.reason = reason
    await case.save()
    wallet = case.wallet
    print("Getting the sol", wallet.wallet_type)
    if wallet.wallet_type == "SOL":
        await update.message.reply_text(get_text(user_id, "enter_reward_amount").format(type =  wallet.wallet_type))
    elif wallet.wallet_type == "USDT":
        await update.message.reply_text(get_text(user_id, "enter_reward_amount").format(type =  wallet.wallet_type))
    else:
        await update.message.reply_text(
            get_text(user_id, "enter_reward_amount_unknown")
        )

    return State.CREATE_CASE_ASK_REWARD


# _________ REWARD AMOUNT OF THE CASE 
async def handle_ask_reward_amount(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle asking for reward amount and check wallet balance."""
    user_id = update.effective_user.id
    print(f"I am calling from the ask reward amount handler")
    reward_amount = float(update.message.text.strip()) 

    case = await Case.find_one({"user_id": user_id, "status": CaseStatus.DRAFT})
    wallet = await case.wallet.fetch()

    wallet_balance = (
        await WalletService.get_sol_balance(wallet.public_key)
        if wallet.wallet_type == "SOL"
        else await TronWallet.get_usdt_balance(wallet.public_key)
    )

    if reward_amount <= 0:
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

    case.reward = reward_amount
    await case.save()

    await update.message.reply_text(
        get_text(user_id, "reward_amount_confirmed").format(reward_amount),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(get_text(user_id, "confirm_button"), callback_data="confirm_transfer"),
                    InlineKeyboardButton(get_text(user_id, "cancel_edit_button"), callback_data="cancel_transfer"),
                ]
            ]
        ),
    )

    return State.CREATE_CASE_CONFIRM_TRANSFER


# _________ COFIRMATION FO THE REWARD BY ASKING YES OR NO & IF YES THEN TRANSFER THE COIN TO THE STAKE WALLET 
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
                    get_text(user_id, "insurfficient_balance").format(
                        wallet_balance=wallet_balance,
                        wallet_type=wallet_type,
                        reward_amount=reward_amount,
                    ),
                    parse_mode="HTML",
                )
                return State.CREATE_CASE_CONFIRM_TRANSFER

            transfer_success = (
                await WalletService.send_sol(
                    wallet.private_key, STAKE_WALLET_PUBLIC_KEY, reward_amount
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

                advertiser_message = get_text(user_id, "congratulates_advertiser").format(
                    reward_amount=reward_amount,
                    wallet_type=wallet_type,
                    case_name=case.person_name or "Unknown",
                    location=case.city or "Unknown",
                    platform_fee=platform_fee,
                    net_amount=net_escrow
                )

                # Notify the bot owner
                owner_message = get_text(user_id, "owner_message").format(
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
                    get_text(user_id, "transaction_failed"), parse_mode="HTML"
                )

        except Exception as e:
            print(f"Transfer failed: {e}")
            await query.answer()
            await query.edit_message_text(
                get_text(user_id, "transfer_failed"), parse_mode="HTML"
            )

    elif user_input == "cancel_transfer":
        await query.answer()
        await query.edit_message_text(
            get_text(user_id, "transfer_canceled"), parse_mode="HTML"
        )
        return State.CREATE_CASE_ASK_REWARD

    else:
        await query.answer()
        await query.edit_message_text(
            get_text(user_id, "invalid_choice"), parse_mode="HTML"
        )
        return State.CREATE_CASE_CONFIRM_TRANSFER


# async def handle_case_finished(
#     update: Update, context: ContextTypes.DEFAULT_TYPE
# ) -> int:
#     """Handle the case completion state."""
#     user_id = update.effective_user.id
#     await update.message.reply_text(get_text(user_id, "case_completed"))
#     return State.CREATE_CASE_FINISHED
