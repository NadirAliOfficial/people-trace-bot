import asyncio
import json
import logging
from datetime import datetime
from typing import List, Optional, Tuple, Dict, Any, Union
from beanie import PydanticObjectId
from bson import ObjectId, errors
import traceback

from config.config_manager import (
    OWNER_TELEGRAM_ID,
    SOL_WALLET_PRIVATE_KEY,
    SOL_WALLET_PUBLIC_KEY,
    SOL_COLLECT_PUBLIC_KEY,
    TRON_COLLECT_PUBLIC_KEY,
    TRON_WALLET_PRIVATE_KEY,
)
from constant.language_constant import get_text
from constants import State
from models.case_model import Case, CaseStatus
from models.extend_reward_model import ExtendReward, ExtendRewardStatus
from models.finder_model import Finder, FinderStatus, RewardExtensionStatus
from models.wallet_model import Wallet
from services.case_service import update_case, update_or_create_case
from services.tron_wallet_service import TronWallet
from services.user_service import get_user_lang
from services.wallet_service import WalletService
from services.otp_service import send_otp, verify_otp
from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    error,
    CallbackQuery,
    InputMediaPhoto,
)
from telegram.helpers import escape_markdown
from telegram.ext import ContextTypes
from utils.get_network import get_network
from utils.logger import logger
from utils.error_wrapper import catch_async
from utils.helper import (
    get_city_matches,
    get_country_matches,
    get_username,
    paginate_list,
    get_province_matches,
)

# Constants
CALLBACK_PATTERNS = {
    "complaint_nav": r"^(complaint_next_|complaint_back_)",
    "edit": r"^edit_",
    "delete": r"^delete_",
    "reward": r"^reward_",
    "finder_details": r"^finder_details_",
    "extend_reward": r"^extend_reward_",
    "approve_extend": r"^approve_extend_",
    "confirm_extend": r"^confirm_extend_",
    "select_wallet": r"^select_wallet_",
    "send_reward": r"^send_reward_",
    "country_select": r"^country_select_",
    "country_page": r"^country_page_",
    "city_select": r"^city_select_",
    "city_page": r"^city_page_",
    "wallet": r"^wallet_",
}

WALLET_TYPES = ["SOL", "USDT"]
DEFAULT_PAGE_SIZE = 10
MAX_MOBILE_LENGTH = 10
MIN_MOBILE_LENGTH = 10

# Message templates
CASE_DISPLAY_TEMPLATE = (
    "🔍 Case {case_num}/{total}\n"
    "👤 Name: {person_name}\n"
    "📍 Last Seen: {last_seen_location}\n"
    "📅 Date: {created_date}\n"
    "🎂 Age: {age}\n"
    "💰 Reward: {reward} {reward_type}\n"
    "🧾 Posted by: @{username}\n"
    "👥 Finders: {finder_count}"
)

DELETE_CONFIRMATION_TEMPLATE = (
    "⚠️ Are you sure you want to delete case:\n\n"
    "👤 {person_name}\n"
    "📍 {last_seen_location}"
)

FINDER_DETAIL_TEMPLATE = (
    "🔍 <b>Case:</b> {person_name}\n"
    "📍 Case Location: {case_location}\n"
    "💰 Reward: {reward} {reward_type}\n\n"
    "👤 <b>Finder Details:</b>\n"
    "🆔 Finder ID: <code>{finder_id}</code>\n"
    "📍 Found Location: {reported_location}\n"
    "📅 Found Date: {found_date}\n"
    "📊 Status: {status}\n"
    "🖼️ Proof: {proof_info}\n"
    "💳 Wallet: {wallet_info}"
)

FINDER_LIST_TEMPLATE = (
    "🔍 <b>Case:</b> {person_name}\n"
    "📍 Location: {case_location}\n"
    "💰 Reward: {reward} {reward_type}\n\n"
    "👥 <b>Finders ({finder_count}):</b>\n"
    "Select a finder to view details and take action."
)

# Error messages
ERROR_MESSAGES = {
    "case_not_found": "❌ Case not found.",
    "invalid_case_index": "❌ Invalid case index.",
    "not_authorized": "❌ You are not authorized to perform this action.",
    "invalid_value": "❌ {error_message} Please enter a valid value.",
    "error_updating_field": "❌ An error occurred while updating the field. Please try again.",
    "error_displaying_case": "❌ Error displaying case details.",
    "invalid_action": "❌ Invalid action selected.",
    "transfer_failed": "❌ Transfer failed. Please check wallet balances and try again.",
    "insufficient_funds": "❌ Insufficient funds in your {wallet_type} wallet. Required: {required_amount}",
}

# ------------------------
# 🛠️ UTILITY CLASSES
# ------------------------


class MessageHandler:
    """Centralized message handling utilities."""

    @staticmethod
    async def send_or_edit_message(
        update: Update,
        text: str,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        parse_mode: str = "HTML",
        case_photo: Optional[str] = None,  # <-- allow passing photo
    ) -> None:
        """Send or edit a message while staying consistent with message type (photo vs text)."""
        try:
            if case_photo:
                # Photo flow
                if update.callback_query:
                    if update.callback_query.message.photo:
                        # ✅ Edit caption if message already contains a photo
                        await update.callback_query.message.edit_caption(
                            caption=text,
                            reply_markup=reply_markup,
                            parse_mode=parse_mode,
                        )
                    else:
                        # Replace with photo if original wasn’t photo
                        await update.callback_query.message.edit_text("⏳ Updating...")
                        await update.callback_query.message.delete()
                        await update.callback_query.message.reply_photo(
                            case_photo,
                            caption=text,
                            reply_markup=reply_markup,
                            parse_mode=parse_mode,
                        )
                else:
                    if update.message.photo:
                        # ✅ Edit caption directly
                        await update.message.edit_caption(
                            caption=text,
                            reply_markup=reply_markup,
                            parse_mode=parse_mode,
                        )
                    else:
                        await update.message.reply_photo(
                            case_photo,
                            caption=text,
                            reply_markup=reply_markup,
                            parse_mode=parse_mode,
                        )
            else:
                # Text-only flow
                if update.callback_query:
                    if not update.callback_query.message.photo:
                        await update.callback_query.message.edit_text(
                            text, reply_markup=reply_markup, parse_mode=parse_mode
                        )
                    else:
                        # Replace photo with plain text
                        await update.callback_query.message.edit_caption(
                            "⏳ Updating..."
                        )
                        await update.callback_query.message.delete()
                        await update.callback_query.message.reply_text(
                            text, reply_markup=reply_markup, parse_mode=parse_mode
                        )
                else:
                    if update.message.photo:
                        await update.message.edit_caption(
                            caption=text,
                            reply_markup=reply_markup,
                            parse_mode=parse_mode,
                        )
                    else:
                        await update.message.reply_text(
                            text, reply_markup=reply_markup, parse_mode=parse_mode
                        )

        except error.BadRequest as e:
            if "message is not modified" not in str(e):
                logger.error(f"Message handling error: {e}")
                raise

    @staticmethod
    async def send_error_message(
        update: Update,
        user_id: int,
        error_key: str,
        context_key: str = "listing",
        **kwargs,
    ) -> None:
        """Send standardized error message."""
        error_msg = get_text(user_id, error_key, context_key).format(**kwargs)
        await MessageHandler.send_or_edit_message(update, error_msg)


class CaseValidator:
    """Case validation utilities."""

    @staticmethod
    async def validate_case_access(
        case: Case, user_id: int, require_ownership: bool = False
    ) -> bool:
        """Validate user access to case."""
        if not case:
            return False

        if require_ownership and case.user_id != user_id:
            return False

        return True

    @staticmethod
    async def get_case_with_validation(
        case_id_str: str,
        user_id: int,
        context: ContextTypes.DEFAULT_TYPE,
        require_ownership: bool = False,
    ) -> Tuple[Optional[Case], bool]:
        """Fetch case with validation and error handling."""
        try:
            case_id = PydanticObjectId(case_id_str)
            case = await Case.find_one(
                {"_id": case_id, "deleted": False}, fetch_links=True
            )

            if not case:
                await MessageHandler.send_error_message(
                    Update(callback_query=context.bot), user_id, "case_not_found"
                )
                return None, False

            if not await CaseValidator.validate_case_access(
                case, user_id, require_ownership
            ):
                await MessageHandler.send_error_message(
                    Update(callback_query=context.bot), user_id, "not_authorized"
                )
                return None, False

            return case, True

        except (errors.InvalidId, Exception) as e:
            logger.error(f"Error validating case {case_id_str}: {e}")
            await MessageHandler.send_error_message(
                Update(callback_query=context.bot), user_id, "invalid_case_id"
            )
            return None, False


class WalletManager:
    """Wallet operation utilities."""

    @staticmethod
    async def get_wallet_balance(wallet_public_key: str, wallet_type: str) -> float:
        """Get wallet balance with error handling."""
        try:
            if wallet_type == "SOL":
                return await WalletService.get_sol_balance(wallet_public_key)
            elif wallet_type == "USDT":
                return await TronWallet.get_usdt_balance(wallet_public_key)
            else:
                logger.error(f"Unsupported wallet type for balance: {wallet_type}")
                return 0.0
        except Exception as e:
            logger.error(f"Error getting balance for {wallet_type}: {e}")
            return 0.0

    @staticmethod
    async def send_transfer(
        private_key: str, recipient_address: str, amount: float, wallet_type: str
    ) -> bool:
        """Send wallet transfer with error handling."""
        try:
            if wallet_type == "SOL":
                return await WalletService.send_sol(
                    private_key, recipient_address, amount
                )
            elif wallet_type == "USDT":
                return await TronWallet.transfer_usdt(
                    private_key, recipient_address, amount
                )
            else:
                logger.error(f"Unsupported wallet type: {wallet_type}")
                return False
        except Exception as e:
            logger.error(f"Transfer failed for {wallet_type}: {e}")
            return False

    @staticmethod
    async def refresh_wallet_balance(
        wallet_public_key: str, wallet_type: str
    ) -> Tuple[float, bool]:
        """Refresh wallet balance and return updated balance with success status."""
        try:
            # Force refresh by making a new request
            if wallet_type == "SOL":
                balance = await WalletService.get_sol_balance(
                    wallet_public_key, force_refresh=True
                )
            elif wallet_type == "USDT":
                balance = await TronWallet.get_usdt_balance(
                    wallet_public_key, force_refresh=True
                )
            else:
                logger.error(f"Unsupported wallet type for refresh: {wallet_type}")
                return 0.0, False

            return balance, True
        except Exception as e:
            logger.error(f"Error refreshing balance for {wallet_type}: {e}")
            return 0.0, False


class CaseDisplayBuilder:
    """Build case display components."""

    @staticmethod
    def build_case_text(
        case: Case, case_num: int, total: int, chat, finder_count: int
    ) -> str:
        """Build case display text."""
        return CASE_DISPLAY_TEMPLATE.format(
            case_num=case_num,
            total=total,
            person_name=case.person_name,
            last_seen_location=case.last_seen_location,
            created_date=case.created_at.strftime("%d %B %Y"),
            age=case.age,
            reward=case.reward,
            reward_type=case.wallet.wallet_type or "N/A",
            username=get_username(chat),
            finder_count=finder_count,
        )

    @staticmethod
    def build_case_keyboard(
        case: Case, index: int, total: int, finder_count: int, user_id: int
    ) -> List[List[InlineKeyboardButton]]:
        """Build case action keyboard."""
        keyboard = []

        # Action buttons (only for case owner)
        if case.user_id == user_id:
            keyboard.extend(
                [
                    [InlineKeyboardButton("🧩 Edit", callback_data=f"edit_{index}")],
                    [
                        InlineKeyboardButton(
                            "🧩 DELETE", callback_data=f"delete_{index}"
                        )
                    ],
                ]
            )

        # Navigation buttons
        nav_row = []
        if index > 0:
            nav_row.append(
                InlineKeyboardButton("◀️ Back", callback_data=f"complaint_back_{index}")
            )
        if index < total - 1:
            nav_row.append(
                InlineKeyboardButton("▶️ Next", callback_data=f"complaint_next_{index}")
            )
        if nav_row:
            keyboard.append(nav_row)

        # Finder button
        if finder_count > 0:
            keyboard.append(
                [
                    InlineKeyboardButton(
                        f"📬 View Finder ({finder_count})",
                        callback_data=f"view_finder_{index}",
                    )
                ]
            )

        return keyboard


class FinderDisplayBuilder:
    """Build finder display components."""

    @staticmethod
    def build_finder_detail_text(case: Case, finder: Finder, user_id: int) -> str:
        """Build detailed finder information text."""
        # Format proof information
        proof_info = "No proof provided"
        if finder.proof_url and len(finder.proof_url) > 0:
            proof_count = len(finder.proof_url)
            proof_info = f"{proof_count} proof(s) provided"

        # Format wallet information
        wallet_info = "No wallet linked"
        if finder.wallet:
            wallet_info = f"{finder.wallet.wallet_type} wallet linked"

        return FINDER_DETAIL_TEMPLATE.format(
            person_name=case.person_name,
            case_location=case.last_seen_location,
            reward=case.reward,
            reward_type=case.wallet.wallet_type if case.wallet else "N/A",
            finder_id=finder.user_id,
            reported_location=finder.reported_location or "Not specified",
            found_date=(
                finder.timestamp.strftime("%d %B %Y") if finder.timestamp else "Unknown"
            ),
            status=finder.status.value.title(),
            proof_info=proof_info,
            wallet_info=wallet_info,
        )

    @staticmethod
    async def build_finder_detail_keyboard(
        finder: Finder,
        case: Case,
        user_id: int,
        finder_index: int = 0,
        total_finders: int = 1,
    ) -> List[List[InlineKeyboardButton]]:
        """Build finder detail action keyboard with navigation."""
        keyboard = []

        # Check if user can take actions (case owner or admin)
        can_take_action = str(user_id) == str(case.user_id) or str(user_id) == str(
            OWNER_TELEGRAM_ID
        )

        if can_take_action and finder.status == FinderStatus.FIND:
            # Reward button
            keyboard.append(
                [
                    InlineKeyboardButton(
                        "💰 Send Reward",
                        callback_data=f"send_reward_{finder.id}_{case.id}",
                    )
                ]
            )

            print("case id: ", case.id)
            extend_reward_count = await ExtendReward.find({"case.$id": case.id}).count()
            print("Extend Count: ", extend_reward_count)
            # Extend reward button (if not already extended)
            if extend_reward_count > 0:
                keyboard.append(
                    [
                        InlineKeyboardButton(
                            f"⏩ Extend Reward ({extend_reward_count})",
                            callback_data=f"extend_reward_{finder.id}_{case.id}",
                        )
                    ]
                )

        # View proof button (if proof exists)
        if finder.proof_url and len(finder.proof_url) > 0:
            keyboard.append(
                [
                    InlineKeyboardButton(
                        f"🖼️ View Proof ({len(finder.proof_url)})",
                        callback_data=f"view_proof_{finder.id}_{case.id}",
                    )
                ]
            )

        # Navigation buttons (only if there are multiple finders)
        if total_finders > 1:
            nav_row = []
            if finder_index > 0:
                nav_row.append(
                    InlineKeyboardButton(
                        "◀️ Previous",
                        callback_data=f"finder_prev_{finder_index}_{case.id}",
                    )
                )
            if finder_index < total_finders - 1:
                nav_row.append(
                    InlineKeyboardButton(
                        "▶️ Next", callback_data=f"finder_next_{finder_index}_{case.id}"
                    )
                )
            if nav_row:
                keyboard.append(nav_row)

        # Back to case button
        keyboard.append(
            [
                InlineKeyboardButton(
                    "◀️ Back to Case", callback_data=f"back_to_case_{case.id}"
                )
            ]
        )

        return keyboard


async def _send_new_complaint_message(message, case, text, reply_markup):
    """Helper function to send a new complaint message."""
    if case.case_photo:
        await message.reply_photo(
            case.case_photo,
            caption=text,
            reply_markup=reply_markup,
            parse_mode="HTML",
        )
    else:
        await message.reply_text(
            text,
            reply_markup=reply_markup,
            parse_mode="HTML",
        )


# ------------------------
# 🚀 MAIN HANDLERS
# ------------------------


@catch_async  # In Use
async def listing_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display paginated list of ADVERTISE cases."""
    user_id = update.effective_user.id
    lang = await get_user_lang(user_id) or "en"
    context.user_data["lang"] = lang

    try:
        # Fetch all advertise cases, newest first
        all_cases = (
            await Case.find(
                {"status": CaseStatus.ADVERTISE, "deleted": False}, fetch_links=True
            )
            .sort(-Case.created_at)
            .to_list()
        )

        if not all_cases:
            await MessageHandler.send_error_message(
                update, user_id, "no_advertise_cases"
            )
            return State.END

        # Initialize pagination
        context.user_data["listing_complaints"] = all_cases
        context.user_data["listing_index"] = 0

        await show_complaint(user_id, update, context)
        return State.LISTING.VIEW_COMPLAINTS

    except Exception as e:
        logger.error(f"Error in listing_command: {e}")
        await MessageHandler.send_error_message(update, user_id, "error_fetching_cases")
        return State.END


async def show_complaint(
    user_id: int, update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Display a single complaint with navigation and action buttons."""
    complaints = context.user_data.get("listing_complaints", [])
    index = context.user_data.get("listing_index", 0)
    if not complaints or index >= len(complaints):
        await MessageHandler.send_error_message(update, user_id, "case_not_found")
        return
    case = complaints[index]
    total = len(complaints)

    # Get chat info and finder count in parallel
    chat_task = context.bot.get_chat(case.user_id)
    finder_count_task = Finder.find(
        {"case.$id": case.id, "status": FinderStatus.FIND.value}
    ).count()
    chat, finder_count = await asyncio.gather(chat_task, finder_count_task)

    # Build case display components
    text = CaseDisplayBuilder.build_case_text(
        case, index + 1, total, chat, finder_count
    )
    keyboard = CaseDisplayBuilder.build_case_keyboard(
        case, index, total, finder_count, user_id
    )
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Determine the message to act upon
    message = update.callback_query.message if update.callback_query else update.message

    # If it's a callback, edit the message
    if update.callback_query:
        try:
            if case.case_photo:
                # If the new message has a photo
                if message.photo:
                    # If the old message also had a photo, edit the media and caption
                    media = InputMediaPhoto(
                        media=case.case_photo, caption=text, parse_mode="HTML"
                    )
                    await message.edit_media(media=media, reply_markup=reply_markup)
                else:
                    # If the old message was text, delete it and send a new photo message
                    await message.delete()
                    await message.reply_photo(
                        case.case_photo,
                        caption=text,
                        reply_markup=reply_markup,
                        parse_mode="HTML",
                    )
            else:
                # If the new message is text-only
                if message.photo:
                    # If the old message had a photo, delete it and send a new text message
                    await message.delete()
                    await message.reply_text(
                        text, reply_markup=reply_markup, parse_mode="HTML"
                    )
                else:
                    # If the old message was also text, edit it
                    await message.edit_text(
                        text, reply_markup=reply_markup, parse_mode="HTML"
                    )

        except error.BadRequest as e:
            if "message is not modified" not in str(e).lower():
                logger.error(f"Error editing message: {e}")
                # Fallback to sending a new message if editing fails for other reasons
                await _send_new_complaint_message(message, case, text, reply_markup)
    else:
        # If it's not a callback, send a new message
        await _send_new_complaint_message(message, case, text, reply_markup)


@catch_async
async def listing_complaint_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle listing complaint navigation and actions."""
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    data = query.data

    index = context.user_data.get("listing_index", 0)
    complaints = context.user_data.get("listing_complaints", [])
    total = len(complaints)
    # Handle navigation
    if data.startswith("complaint_next_") and index + 1 < total:
        context.user_data["listing_index"] += 1
        await show_complaint(user_id, update, context)
        return State.LISTING.VIEW_COMPLAINTS
    elif data.startswith("complaint_back_") and index > 0:
        context.user_data["listing_index"] -= 1
        await show_complaint(user_id, update, context)
        return State.LISTING.VIEW_COMPLAINTS
    # Handle actions
    elif data.startswith("edit_"):
        return await _handle_edit_action(update, context, user_id, data, complaints)
    elif data.startswith("delete_"):
        return await _handle_delete_action(update, context, user_id, data, complaints)
    elif data.startswith("view_finder_"):
        context.user_data["selected_complaint"] = complaints[index]
        print("Viewing the finders for the first case")
        return await _handle_view_finders(update, context, user_id, data, complaints)
    else:
        await MessageHandler.send_error_message(update, user_id, "invalid_action")
        return State.END


@catch_async
async def show_finders_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Display paginated list of finders for a case (similar to listing_command)."""
    user_id = update.effective_user.id
    lang = await get_user_lang(user_id) or "en"
    context.user_data["lang"] = lang

    try:
        # Get case ID from context or callback data
        case_id = context.user_data.get("selected_case_id")
        if not case_id:
            # Try to get from callback data if coming from case view
            if update.callback_query:
                data = update.callback_query.data
                if data.startswith("reward_"):
                    index = int(data.split("_")[1])
                    complaints = context.user_data.get("listing_complaints", [])
                    if index < len(complaints):
                        case_id = complaints[index].id
                        context.user_data["selected_case_id"] = case_id

        if not case_id:
            await MessageHandler.send_error_message(update, user_id, "case_not_found")
            return State.END

        # Fetch all finders for the case
        all_finders = (
            await Finder.find(
                {
                    "case.$id": PydanticObjectId(case_id),
                    "status": FinderStatus.FIND.value,
                },
            )
            .sort(-Finder.timestamp)
            .to_list()
        )

        for finder in all_finders:
            await finder.fetch_all_links()

        if not all_finders:
            await MessageHandler.send_error_message(
                update, user_id, "no_finders_for_case"
            )
            return State.END

        # Fetch case details
        case = await Case.find_one({"_id": PydanticObjectId(case_id)}, fetch_links=True)
        if not case:
            await MessageHandler.send_error_message(update, user_id, "case_not_found")
            return State.END

        # Initialize pagination (same as cases)
        context.user_data["listing_finders"] = all_finders
        context.user_data["finder_index"] = 0
        context.user_data["current_case"] = case

        await show_finder(user_id, update, context)
        return State.LISTING.VIEW_FINDERS

    except Exception as e:
        logger.error(f"Error in show_finders_command: {e}")
        await MessageHandler.send_error_message(
            update, user_id, "error_fetching_finders"
        )
        return State.END


async def show_finder(
    user_id: int, update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Display a single finder with navigation and action buttons (similar to show_complaint)."""
    finders = context.user_data.get("listing_finders", [])
    index = context.user_data.get("finder_index", 0)
    case = context.user_data.get("finder_current_case")

    if not finders or index >= len(finders) or not case:
        await MessageHandler.send_error_message(update, user_id, "finder_not_found")
        return
    finder = finders[index]
    context.user_data["finder_current_finder"] = finder
    total = len(finders)

    # Get chat info in parallel (same as cases)
    chat_task = context.bot.get_chat(finder.user_id)
    chat = await chat_task

    # Build finder display components (same pattern as cases)
    text = FinderDisplayBuilder.build_finder_detail_text(case, finder, user_id)
    keyboard = await FinderDisplayBuilder.build_finder_detail_keyboard(
        finder, case, user_id, index, total
    )
    reply_markup = InlineKeyboardMarkup(keyboard)

    print("Text are", text)
    print("User id are", user_id)
    print("Case are", case)
    print("Finder are", finder)
    print("Index are", index)
    print("Total are", total)
    print("Keyboard are", keyboard)
    print("Reply markup are", reply_markup)

    # Determine the message to act upon (same logic as cases)
    message = update.callback_query.message if update.callback_query else update.message

    # If it's a callback, edit the message (same logic as cases)
    if update.callback_query:
        # Check if finder has proof images
        has_photo = finder.proof_url and len(finder.proof_url) > 0
        first_photo = finder.proof_url[0] if has_photo else None
        if first_photo:
            # If the new message has a photo
            if message.photo:
                # If the old message also had a photo, edit the media and caption
                media = InputMediaPhoto(
                    media=first_photo, caption=text, parse_mode="HTML"
                )
                await message.edit_media(media=media, reply_markup=reply_markup)
            else:
                # If the old message was text, delete it and send a new photo message
                await message.delete()
                await message.reply_photo(
                    first_photo,
                    caption=text,
                    reply_markup=reply_markup,
                    parse_mode="HTML",
                )
        else:
            # If the new message is text-only
            if message.photo:
                # If the old message had a photo, delete it and send a new text message
                await message.delete()
                await message.reply_text(
                    text, reply_markup=reply_markup, parse_mode="HTML"
                )
            else:
                # If the old message was also text, edit it
                await message.edit_text(
                    text, reply_markup=reply_markup, parse_mode="HTML"
                )

    else:
        # If it's not a callback, send a new message
        await _send_new_finder_message(message, finder, text, reply_markup, case)


async def _send_new_finder_message(
    message, finder: Finder, text: str, reply_markup: InlineKeyboardMarkup, case: Case
):
    """Helper function to send a new finder message (similar to cases)."""
    has_photo = finder.proof_url and len(finder.proof_url) > 0
    first_photo = finder.proof_url[0] if has_photo else None

    if first_photo:
        await message.reply_photo(
            first_photo,
            caption=text,
            reply_markup=reply_markup,
            parse_mode="HTML",
        )
    else:
        await message.reply_text(
            text,
            reply_markup=reply_markup,
            parse_mode="HTML",
        )


@catch_async
async def finder_navigation_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle finder navigation and actions (similar to listing_complaint_callback)."""
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    data = query.data

    case = context.user_data.get("finder_current_case")
    index = context.user_data.get("finder_index", 0)
    finders = context.user_data.get("listing_finders", [])

    total = len(finders)
    # Handle navigation (same pattern as cases)
    if data.startswith("finder_next_") and index + 1 < total:
        context.user_data["finder_index"] += 1
        await show_finder(user_id, update, context)
        return State.LISTING.VIEW_FINDERS
    elif data.startswith("finder_prev_") and index > 0:
        print("Previous finder", context.user_data["finder_index"], "finder index are")
        context.user_data["finder_index"] -= 1
        await show_finder(user_id, update, context)
        return State.LISTING.VIEW_FINDERS
    elif data.startswith("send_reward_"):

        await query.message.reply_text(
            get_text(user_id, "enter_reward_amount", "listing").format(
                max_amount=case.reward
            ),
            parse_mode="Markdown",
        )
        return State.REWARD_TRANSFER_PROCESS
        # return await _handle_send_reward_action(update, context, user_id, data, finders)

    # Handle actions (similar to cases but for finders)
    elif data.startswith("extend_reward_"):
        return await _handle_extend_reward_action(
            update, context, user_id, data, finders
        )
    # elif data.startswith("view_proof_"):
    #     return await _handle_view_proof_action(update, context, user_id, data, finders)
    # elif data.startswith("back_to_case_"):
    #     return await _handle_back_to_case_action(update, context, user_id, data)
    else:
        await MessageHandler.send_error_message(update, user_id, "invalid_action")
        return State.END


# ======================================================================================================================
# Helper Functions for Case Display and Actions (Optimized)
# ======================================================================================================================


async def _send_case_message(
    update: Update, case: Case, text: str, keyboard: List[List[InlineKeyboardButton]]
) -> None:
    """Send case message with photo or text."""
    reply_markup = InlineKeyboardMarkup(keyboard)

    if case.case_photo:
        message = update.message or update.callback_query.message
        await message.reply_photo(
            case.case_photo,
            caption=text,
            reply_markup=reply_markup,
            parse_mode="HTML",
        )
    else:
        await MessageHandler.send_or_edit_message(update, text, reply_markup)


# Removed - functionality moved to MessageHandler class


async def _handle_edit_action(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    user_id: int,
    data: str,
    complaints: List[Case],
) -> int:
    """Handle edit action for a case."""
    try:
        selected_index = int(data.split("_")[1])
        if selected_index >= len(complaints):
            await MessageHandler.send_error_message(update, user_id, "case_not_found")
            return State.END

        selected_complaint = complaints[selected_index]
        if not selected_complaint:
            await MessageHandler.send_error_message(update, user_id, "case_not_found")
            return State.END

        # Store editing context
        context.user_data["editing_complaint"] = selected_complaint
        context.user_data["editing_index"] = selected_index

        # Build edit fields keyboard
        editable_fields = get_text(user_id, "editable_fields", "listing")
        keyboard = _build_edit_fields_keyboard(editable_fields)

        new_text = get_text(user_id, "edit_field_prompt", "listing")
        reply_markup = InlineKeyboardMarkup(keyboard)

        await MessageHandler.send_or_edit_message(update, new_text, reply_markup)
        return State.LISTING.EDIT_FIELD_SELECTION

    except (ValueError, IndexError) as e:
        logger.error(f"Error in edit action: {e}")
        await MessageHandler.send_error_message(update, user_id, "invalid_case_index")
        return State.END


async def _handle_delete_action(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    user_id: int,
    data: str,
    complaints: List[Case],
) -> int:
    """Handle delete action for a case."""
    query = update.callback_query
    try:
        selected_index = int(data.split("_")[1])
        if selected_index >= len(complaints):
            await query.answer("❌ Complaint not found", show_alert=True)
            return State.LISTING.VIEW_COMPLAINTS

        selected_complaint = complaints[selected_index]
        context.user_data["deleting_complaint"] = selected_complaint
        context.user_data["deleting_index"] = selected_index

        # Build confirmation keyboard
        keyboard = [
            [
                InlineKeyboardButton(
                    "✅ Confirm Delete", callback_data="confirm_delete"
                ),
                InlineKeyboardButton("❌ Cancel", callback_data="cancel_delete"),
            ]
        ]

        new_text = DELETE_CONFIRMATION_TEMPLATE.format(
            person_name=selected_complaint.person_name,
            last_seen_location=selected_complaint.last_seen_location,
        )

        await MessageHandler.send_or_edit_message(
            update, new_text, InlineKeyboardMarkup(keyboard)
        )
        return State.CASE_DETAILS

    except (ValueError, IndexError) as e:
        logger.error(f"Error in delete action: {e}")
        await query.answer("❌ Invalid case index", show_alert=True)
        return State.LISTING.VIEW_COMPLAINTS


async def _handle_view_finders(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    user_id: int,
    data: str,
    complaints: List[Case],
) -> int:
    """Handle view finders action for a case."""
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    print("Viewing the finders for the first case", "data are", data)

    selected_index = int(data.split("_")[2])
    print("selected index of complaint", selected_index)
    if selected_index >= len(complaints):
        await query.answer("❌ Complaint not found", show_alert=True)
        return State.LISTING.VIEW_FINDERS
    selected_complaint = complaints[selected_index]

    #  Storing to  use it later.
    context.user_data["finder_current_case"] = selected_complaint
    context.user_data["finder_curent_index"] = selected_index

    all_finders = (
        await Finder.find(
            {
                "case.$id": PydanticObjectId(selected_complaint.id),
                "status": FinderStatus.FIND.value,
            },
        )
        .sort(-Finder.timestamp)
        .to_list()
    )

    for finder in all_finders:
        await finder.fetch_all_links()

    if not all_finders:
        await MessageHandler.send_error_message(update, user_id, "no_finders_for_case")
        return State.END

    context.user_data["listing_finders"] = all_finders
    context.user_data["finder_index"] = 0
    context.user_data["current_case"] = selected_complaint

    await show_finder(user_id, update, context)
    return State.LISTING.VIEW_FINDERS


def _build_edit_fields_keyboard(
    editable_fields: Dict[str, str],
) -> List[List[InlineKeyboardButton]]:
    """Build keyboard for editable fields."""
    keyboard = []
    field_items = list(editable_fields.items())

    # Create pairs of buttons
    for i in range(0, len(field_items), 2):
        row = []
        # First button
        k1, v1 = field_items[i]
        row.append(InlineKeyboardButton(f"{k1}", callback_data=f"edit_field_{v1}"))

        # Second button if available
        if i + 1 < len(field_items):
            k2, v2 = field_items[i + 1]
            row.append(InlineKeyboardButton(f"{k2}", callback_data=f"edit_field_{v2}"))

        keyboard.append(row)

    # Add cancel button
    keyboard.append([InlineKeyboardButton("Cancel", callback_data="cancel_edit")])

    return keyboard


@catch_async
async def edit_field_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Ask the user to enter a new value for the selected field."""
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    field_name = query.data.removeprefix("edit_field_")
    context.user_data["editing_field"] = field_name

    # Field-specific prompts
    field_prompts = {
        "country": ("🌍 Please enter your country:", State.ENTER_COUNTRY),
        "province": ("📍 Please enter your province/state:", State.ENTER_PROVINCE),
        "city": ("🏙️ Please enter your city:", State.ENTER_CITY),
        "mobile": ("📱 Please enter your mobile number:", State.ENTER_MOBILE_NUMBER),
    }

    if field_name in field_prompts:
        prompt, state = field_prompts[field_name]

        # Set context data for location fields
        case = context.user_data.get("editing_complaint")
        if case and field_name in ["province", "city"] and case.country:
            context.user_data["country"] = case.country
        if case and field_name == "city" and case.province:
            context.user_data["province"] = case.province

        await MessageHandler.send_or_edit_message(update, prompt)
        return state

    # Handle other fields
    text = get_text(user_id, "enter_new_value", "listing").format(
        field_name=field_name.replace("_", " ").title()
    )
    await MessageHandler.send_or_edit_message(update, text, parse_mode="Markdown")
    return State.EDIT_FIELD


async def _validate_and_process_field_value(field_name: str, value: str, context):
    """Validate and process field values depending on the field type."""
    fname = field_name.lower().strip()

    # ✅ Name / Person Name / Relationship / Reason
    if fname in ["name", "person_name", "relationship", "reason"]:
        if len(value) < 2:
            raise ValueError("Value must be at least 2 characters long.")
        return value.strip().title()

    # ✅ Location fields
    elif fname in ["last_seen_location", "country", "province", "city"]:
        if len(value) < 2:
            raise ValueError(f"{field_name.replace('_', ' ').title()} cannot be empty.")
        return value.strip().title()

    # ✅ Gender
    elif fname == "gender":
        allowed = ["MALE", "FEMALE", "OTHER"]
        if value.upper() not in allowed:
            raise ValueError(f"Invalid gender. Allowed: {', '.join(allowed)}")
        return value.upper()

    # ✅ Numeric: Age, Height, Weight
    elif fname in ["age", "height", "weight"]:
        try:
            num_value = int(value)
            if num_value <= 0:
                raise ValueError(
                    f"{field_name.replace('_', ' ').title()} must be greater than 0."
                )
            return num_value
        except ValueError:
            raise ValueError(
                f"{field_name.replace('_', ' ').title()} must be a valid number."
            )

    # ✅ Hair / Eye Color / Distinctive Features
    elif fname in ["hair_color", "eye_color", "distinctive_features"]:
        if not value.strip():
            raise ValueError(f"{field_name.replace('_', ' ').title()} cannot be empty.")
        return value.strip().title()

    # ✅ Mobile Number (11 digits, starts with country code 92)
    elif fname in ["mobile", "mobile_number", "contact_number"]:
        if not value.isdigit():
            raise ValueError("Mobile number must contain only digits.")
        if len(value) != 11:
            raise ValueError("Mobile number must be exactly 11 digits.")
        if not value.startswith("92"):
            raise ValueError(
                "Mobile number must start with the country code (e.g., 92...)."
            )
        return value.strip()

    # 🔄 Default
    else:
        return value.strip()


@catch_async
async def update_case_field(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Update the specified field in the case document."""
    case = context.user_data.get("editing_complaint")
    field_name = context.user_data.get("editing_field")
    user_id = update.effective_user.id
    new_value = update.message.text.strip()

    # Validate case exists
    if not case:
        await MessageHandler.send_error_message(update, user_id, "case_not_found")
        return State.END

    # Validate and process field value
    processed_value = await _validate_and_process_field_value(
        field_name, new_value, context
    )
    # Update the case document
    print("Field name ", field_name, "New Value", new_value)

    setattr(case, field_name, processed_value)
    case.updated_at = datetime.utcnow()
    await case.save()
    # Update the complaint in the listing
    editing_index = context.user_data.get("editing_index", 0)
    complaints = context.user_data.get("listing_complaints", [])
    if editing_index < len(complaints):
        complaints[editing_index] = case
    # Send success message and return to complaint view
    success_text = get_text(user_id, "field_updated_successfully", "listing").format(
        field_name=field_name.replace("_", " ").title(),
        new_value=processed_value,
    )
    await update.message.reply_text(success_text, parse_mode="HTML")
    # Clear edit context
    _clear_edit_context(context)
    # Return to complaint view
    await show_complaint(user_id, update, context)
    return State.LISTING.VIEW_COMPLAINTS


@catch_async
async def _handle_extend_reward_action(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    user_id: int,
    data: str,
    finders: List[Finder],
) -> int:
    """Handle extend reward action for a specific finder."""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    finder = context.user_data.get("finder_current_finder")
    case = context.user_data.get("selected_complaint")

    # Get all extend rewards for this case
    extend_rewards = await ExtendReward.find(
        {"case.$id": PydanticObjectId(case.id)}
    ).to_list()

    if not extend_rewards:
        await query.message.edit_text(
            get_text(user_id, "extend_reward_not_found", "listing")
        )
        return State.END

    # Build buttons from DB values
    kb = [
        [
            InlineKeyboardButton(
                f"💰 Extend Reward ({er.extend_reward_amount})",
                callback_data=f"extend_amount_{er.id}",
            )
        ]
        for er in extend_rewards
        if er.extend_reward_amount
    ]

    # Replace old button with new ones
    await query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(kb))

    return State.EXTEND_REWARD_CHOICE

    # return await handle_extend_reward_flow(update, context, case_id)


def _clear_edit_context(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Clear edit-related context data."""
    context.user_data.pop("editing_complaint", None)
    context.user_data.pop("editing_field", None)
    context.user_data.pop("editing_index", None)
    context.user_data.pop("country", None)
    context.user_data.pop("province", None)
    context.user_data.pop("otp_id", None)
    context.user_data.pop("mobile_number", None)


async def _validate_and_process_field_value(
    field_name: str, new_value: str, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Validate and process field value based on field type."""
    validation_rules = {
        "country": lambda v: get_country_matches(v)
        or (None, "Invalid country. Please provide a valid country."),
        "city": lambda v: get_city_matches(context.user_data.get("country"), v)
        or (None, f"Invalid city for country {context.user_data.get('country')}."),
        "mobile": lambda v: (
            (v, None)
            if len(v) >= MIN_MOBILE_LENGTH
            else (None, f"Mobile number must be at least {MIN_MOBILE_LENGTH} digits.")
        ),
    }

    if field_name in validation_rules:
        result, error_msg = validation_rules[field_name](new_value)
        if error_msg:
            raise ValueError(error_msg)
        return result[0] if isinstance(result, list) else result

    return new_value


@catch_async
async def delete_case_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handler for confirming and soft deleting a case."""
    query = update.callback_query
    await query.answer()

    case = context.user_data.get("deleting_complaint", None)
    user_id = update.effective_user.id

    if not case:
        await MessageHandler.send_error_message(update, user_id, "case_not_found")
        return State.HANDLER_END

    # Authorization check
    if case.user_id != user_id:
        await MessageHandler.send_error_message(
            update, user_id, "not_authorized_delete"
        )
        return State.HANDLER_END

    try:
        # Soft delete
        await update_case(case_id=PydanticObjectId(case.id), deleted=True)

        # Send success message
        success_text = get_text(user_id, "case_deleted_successfully", "listing")
        await MessageHandler.send_or_edit_message(update, success_text)

        # Show updated listing
        return await listing_command(update, context)

    except Exception as e:
        logger.error(f"Error deleting case: {e}")
        await MessageHandler.send_error_message(update, user_id, "error_deleting_case")
        return State.END


# ------------------------
# 🎯 REWARD FINDER FLOW
# ------------------------
@catch_async
async def view_finder_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    query = update.callback_query
    await query.answer()

    case = context.user_data.get("selected_complaint")
    user_id = query.from_user.id

    if not case:
        await MessageHandler.send_error_message(update, user_id, "case_not_found")
        return State.END

    print("Case are", case.id)
    print("Case are", PydanticObjectId(case.id))

    # ✅ fetch_links=True here will automatically populate case + wallet
    finders = await Finder.find(
        {
            "case.$id": PydanticObjectId(case.id),
            "status": FinderStatus.FIND.value,
        },
    ).to_list()

    for finder in finders:
        await finder.fetch_all_links()

    if not finders:
        await MessageHandler.send_error_message(update, user_id, "no_finders_for_case")
        return State.END

    # Store finders in context
    context.user_data["case_finders"] = finders
    context.user_data["current_finder_index"] = 0
    context.user_data["current_case_id"] = str(case.id)

    # Show first finder
    first_finder = finders[0]
    detail_card = FinderDisplayBuilder.build_finder_detail_text(
        case, first_finder, user_id
    )
    keyboard = await FinderDisplayBuilder.build_finder_detail_keyboard(
        first_finder, case, user_id, 0, len(finders)
    )
    reply_markup = InlineKeyboardMarkup(keyboard)

    await MessageHandler.send_or_edit_message(update, detail_card, reply_markup, "HTML")
    return State.CASE_DETAILS


# @catch_async
# async def view_finder_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Show individual finder details with navigation."""
#     query = update.callback_query
#     await query.answer()

#     case = context.user_data.get("selected_complaint")
#     user_id = query.from_user.id

#     try:

#         # Fetch case and finder in parallel
#         finder_task = Finder.find_one({"_id": finder_id}, fetch_links=True)

#         case, finder = await asyncio.gather(case_task, finder_task)

#         if not case or not finder:
#             await MessageHandler.send_error_message(
#                 update, user_id, "case_or_finder_not_found"
#             )
#             return State.END

#         # Get all finders for navigation
#         all_finders = context.user_data.get("case_finders", [])
#         total_finders = len(all_finders)

#         # Build detailed finder information
#         detail_card = FinderDisplayBuilder.build_finder_detail_text(case, finder, user_id)
#         keyboard = await FinderDisplayBuilder.build_finder_detail_keyboard(
#             finder, case, user_id, finder_index, total_finders
#         )
#         reply_markup = InlineKeyboardMarkup(keyboard)

#         # Store current finder index in context
#         context.user_data["current_finder_index"] = finder_index

#         await MessageHandler.send_or_edit_message(
#             update, detail_card, reply_markup, "HTML"
#         )
#         return State.CASE_DETAILS

#     except Exception as e:
#         logger.error(f"Error in view_finder_callback: {e}")
#         await MessageHandler.send_error_message(
#             update, user_id, "error_fetching_finder"
#         )
#         return State.END


# @catch_async
# async def finder_details_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Show detailed finder info with conditional action buttons."""
#     query = update.callback_query
#     await query.answer()

#     data = query.data.removeprefix("finder_details_")
#     finder_id_str, case_id_str = data.split("_", 1)
#     user_id = query.from_user.id

#     case_id = PydanticObjectId(case_id_str)
#     finder_id = PydanticObjectId(finder_id_str)
#     # Fetch case and finder in parallel
#     case_task = Case.find_one({"_id": case_id, "deleted": False}, fetch_links=True)
#     finder_task = Finder.find_one({"_id": finder_id}, fetch_links=True)

#     case, finder = await asyncio.gather(case_task, finder_task)
#     if not case or not finder:
#         await MessageHandler.send_error_message(
#             update, user_id, "case_or_finder_not_found"
#         )
#         return State.END
#     # Build detailed finder information
#     detail_card = FinderDisplayBuilder.build_finder_detail_text(case, finder, user_id)
#     keyboard = await FinderDisplayBuilder.build_finder_detail_keyboard(finder, case, user_id)
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     await MessageHandler.send_or_edit_message(
#         update, detail_card, reply_markup, "HTML"
#     )
#     return State.CASE_DETAILS


# ------------------------
# 🔄 EXTEND REWARD FLOW
# ------------------------


@catch_async
async def extend_reward_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle extend reward request for a specific finder."""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = query.data.removeprefix("extend_reward_")
    finder_id, case_id = data.split("_")

    try:
        case = await Case.find_one(
            {"_id": PydanticObjectId(case_id), "deleted": False}, fetch_links=True
        )
        finder = await Finder.find_one(
            {"_id": PydanticObjectId(finder_id)}, fetch_links=True
        )

        if not case or not finder:
            await query.message.edit_text(
                get_text(user_id, "case_or_finder_not_found", "listing"),
                parse_mode="HTML",
            )
            return State.END

        # Check if finder already has an extend reward request
        existing_extend = await ExtendReward.find_one(
            {
                "case.$id": PydanticObjectId(case_id),
                "user_id": finder.user_id,
                "status": {"$ne": ExtendRewardStatus.COMPLETED},
            }
        )

        if existing_extend:
            await query.message.edit_text(
                "⚠️ This finder already has a pending extend reward request.",
                parse_mode="HTML",
            )
            return State.END

        # Create extend reward request
        extend_reward = ExtendReward(
            case=case,
            user_id=finder.user_id,
            extend_reward_amount=case.reward * 0.5,  # 50% of original reward
            status=ExtendRewardStatus.PENDING,
        )
        await extend_reward.save()

        # Update finder with extend reward info
        finder.extended_reward_requested = extend_reward.extend_reward_amount
        finder.extended_reward_status = RewardExtensionStatus.PENDING
        finder.extended_reward_timestamp = datetime.utcnow()
        await finder.save()

        await query.message.edit_text(
            f"✅ Extend reward request created successfully!\n"
            f"💰 Amount: {extend_reward.extend_reward_amount} {case.wallet.wallet_type}\n"
            f"⏳ Status: Pending approval",
            parse_mode="HTML",
        )
        return State.END

    except Exception as e:
        logger.error(f"Extend reward callback error: {e}")
        await query.message.edit_text(
            get_text(user_id, "error_approving_extend", "listing"), parse_mode="HTML"
        )
        return State.END


# ------------------------
# UTILITY FUNCTIONS (OPTIMIZED)
# ------------------------

# Removed old utility functions - functionality moved to utility classes above


def _format_finder_list_card(
    case: Case, finders: List[Finder], user_id: int, lang: str
) -> str:
    """Format finder list card display text."""
    return (
        f"🔍 **Case Details:**\n"
        f"👤 Name: {case.person_name}\n"
        f"📍 Location: {case.last_seen_location}\n"
        f"💰 Reward: {case.reward} {case.wallet.wallet_type if case.wallet else 'N/A'}\n\n"
        f"👥 **Finders ({len(finders)}):**\n"
        f"Select a finder to view details and send reward."
    )


def _format_finder_detail_card(
    case: Case, finder: Finder, user_id: int, lang: str
) -> str:
    """Format finder detail card display text."""
    return FINDER_DETAIL_TEMPLATE.format(
        person_name=case.person_name,
        last_seen_location=case.last_seen_location,
        reward=case.reward,
        reward_type=case.wallet.wallet_type if case.wallet else "N/A",
        finder_id=finder.user_id,
        status=finder.status.value,
        found_date=(
            finder.created_at.strftime("%d %B %Y") if finder.created_at else "N/A"
        ),
    )


def _format_case_card(case: Case, user_id: int, lang: str) -> str:
    """Format case card display text."""
    return (
        f"🔍 <b>Case Details:</b>\n"
        f"👤 Name: {case.person_name}\n"
        f"📍 Location: {case.last_seen_location}\n"
        f"🎂 Age: {case.age or 'Unknown'}\n"
        f"💰 Reward: {case.reward} {case.wallet.wallet_type if case.wallet else 'N/A'}\n"
        f"📅 Posted: {case.created_at.strftime('%d %B %Y') if case.created_at else 'Unknown'}"
    )


async def create_pagination_keyboard(
    cases: list,
    page: int,
    total_pages: int,
    user_id: int,
    show_edit_delete: bool = True,
    show_reward_button: bool = False,
) -> InlineKeyboardMarkup:
    """Create a standardized pagination keyboard"""
    keyboard = []

    # Case buttons
    paginated_cases, _ = paginate_list(cases, page)
    for case in paginated_cases:
        row = [
            InlineKeyboardButton(
                f"{case.person_name} ({case.id})", callback_data=f"case_{str(case.id)}"
            )
        ]

        # Check if finder exists
        finder_exist = await Finder.find(
            {"case.$id": PydanticObjectId(case.id), "status": FinderStatus.FIND}
        ).to_list()

        # Edit/Delete buttons (only for owner and no finder)
        if show_edit_delete and case.user_id == user_id and len(finder_exist) == 0:
            row.append(
                InlineKeyboardButton(
                    get_text(user_id, "edit_button", "listing"),
                    callback_data=f"edit_{str(case.id)}",
                )
            )
            row.append(
                InlineKeyboardButton(
                    get_text(user_id, "delete_button", "listing"),
                    callback_data=f"delete_{str(case.id)}",
                )
            )

        # Reward button (only for owner and finder exists)
        if (
            show_reward_button
            and str(user_id) == str(OWNER_TELEGRAM_ID)
            and finder_exist
        ):
            row.append(
                InlineKeyboardButton(
                    "Reward Finder", callback_data=f"reward_{str(case.id)}"
                )
            )

        # Extend reward button (only for owner and pending extend reward)
        extend_reward = await ExtendReward.find_one(
            {
                "case.$id": PydanticObjectId(case.id),
                "status": {"$ne": ExtendRewardStatus.COMPLETED},
            }
        )
        if (
            case.status == CaseStatus.ADVERTISE
            and extend_reward
            and case.user_id == user_id
        ):
            row.append(
                InlineKeyboardButton(
                    get_text(user_id, "extend_reward_button", "listing"),
                    callback_data=f"extend_reward_{str(case.id)}",
                )
            )

        keyboard.append(row)

    # Navigation buttons
    navigation_buttons = []
    if page > 1:
        navigation_buttons.append(
            InlineKeyboardButton(
                get_text(user_id, "prev", "globals"), callback_data="page_previous"
            )
        )
    if page < total_pages:
        navigation_buttons.append(
            InlineKeyboardButton(
                get_text(user_id, "next", "globals"), callback_data="page_next"
            )
        )

    if navigation_buttons:
        keyboard.append(navigation_buttons)

    return InlineKeyboardMarkup(keyboard)


async def send_case_details(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    case: Case,
    show_edit_delete: bool = True,
) -> None:
    """Unified case details display"""
    user_id = update.effective_user.id
    lang = context.user_data.get("lang", "en")

    # Build proof text
    proof_text = (
        f"[Proof]({case.case_photo})"
        if case.case_photo and case.case_photo.startswith("http")
        else get_text(user_id, "no_proof_available", "listing")
    )

    # Format case message
    case_message = get_text(lang, "case_details_template", "listing").format(
        person_name=case.person_name,
        last_seen_location=case.last_seen_location,
        age=case.age or "Unknown",
        reward=case.reward or "0",
        reward_type=case.wallet.wallet_type if case.wallet else "None",
        last_seen_date=(
            case.created_at.strftime("%d %B %Y") if case.created_at else "Unknown"
        ),
        height=case.height or "Unknown",
    )
    case_message += f"\n<b>Proof:</b> {proof_text}"

    # Prepare buttons
    keyboard = []
    if show_edit_delete and case.user_id == user_id:
        row = [
            InlineKeyboardButton(
                get_text(user_id, "edit_button", "listing"),
                callback_data=f"edit_{str(case.id)}",
            ),
            InlineKeyboardButton(
                get_text(user_id, "delete_button", "listing"),
                callback_data=f"delete_{str(case.id)}",
            ),
        ]
        keyboard.append(row)

    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send message
    if isinstance(update, Update) and update.callback_query:
        await update.callback_query.message.edit_text(
            case_message.strip(),
            reply_markup=reply_markup,
            parse_mode="HTML",
        )
    elif isinstance(update, Update) and update.message:
        await update.message.reply_text(
            case_message.strip(),
            reply_markup=reply_markup,
            parse_mode="HTML",
        )


async def handle_wallet_selection(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    user_id: int,
    wallet_type: str,
    action: str = "create_case",
) -> int:
    """Unified handler for wallet selection flow with refresh capability"""
    existing_wallets = await WalletService.get_wallet_by_type(user_id, wallet_type)

    if existing_wallets:
        kb = []
        for wallet in existing_wallets:
            # Get current balance for display
            balance = await WalletManager.get_wallet_balance(
                wallet.public_key, wallet_type
            )
            kb.append(
                [
                    InlineKeyboardButton(
                        f"{wallet.name} ({balance:.4f} {wallet_type})",
                        callback_data=f"wallet_{str(wallet.id)}",
                    )
                ]
            )

        # Add refresh and create new wallet buttons
        kb.extend(
            [
                [
                    InlineKeyboardButton(
                        "🔄 Refresh Balances", callback_data="refresh_wallet_balances"
                    )
                ],
                [
                    InlineKeyboardButton(
                        get_text(user_id, "create_new_wallet"),
                        callback_data="create_new_wallet",
                    )
                ],
            ]
        )

        message = get_text(user_id, "choose_existing_or_new_wallet")
    else:
        kb = []
        message = get_text(user_id, "wallet_name_prompt")

    reply_markup = InlineKeyboardMarkup(kb)

    if update.callback_query:
        await update.callback_query.message.edit_text(
            message, reply_markup=reply_markup, parse_mode="HTML"
        )
    else:
        await update.message.reply_text(
            message, reply_markup=reply_markup, parse_mode="HTML"
        )

    context.user_data["wallet_type"] = wallet_type
    context.user_data["action"] = action
    return State.CHOOSE_WALLET_TYPE


@catch_async
async def refresh_wallet_balances_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle refresh wallet balances callback"""
    query = update.callback_query
    await query.answer("🔄 Refreshing balances...")

    user_id = update.effective_user.id
    wallet_type = context.user_data.get("wallet_type")

    if not wallet_type:
        await query.message.edit_text(
            get_text(user_id, "no_wallet_type_selected", "listing")
        )
        return State.END

    try:
        # Get all wallets of the selected type
        existing_wallets = await WalletService.get_wallet_by_type(user_id, wallet_type)

        if not existing_wallets:
            await query.message.edit_text(
                get_text(user_id, "no_wallets_found", "listing")
            )
            return State.END

        # Refresh balances for all wallets
        refreshed_wallets = []
        for wallet in existing_wallets:
            balance, success = await WalletManager.refresh_wallet_balance(
                wallet.public_key, wallet_type
            )
            if success:
                refreshed_wallets.append((wallet, balance))

        # Rebuild keyboard with refreshed balances
        kb = []
        for wallet, balance in refreshed_wallets:
            kb.append(
                [
                    InlineKeyboardButton(
                        f"{wallet.name} ({balance:.4f} {wallet_type})",
                        callback_data=f"wallet_{str(wallet.id)}",
                    )
                ]
            )

        # Add refresh and create new wallet buttons
        kb.extend(
            [
                [
                    InlineKeyboardButton(
                        "🔄 Refresh Balances", callback_data="refresh_wallet_balances"
                    )
                ],
                [
                    InlineKeyboardButton(
                        get_text(user_id, "create_new_wallet"),
                        callback_data="create_new_wallet",
                    )
                ],
            ]
        )

        message = get_text(user_id, "balances_refreshed", "listing")
        reply_markup = InlineKeyboardMarkup(kb)

        await query.message.edit_text(
            message, reply_markup=reply_markup, parse_mode="HTML"
        )
        return State.CHOOSE_WALLET_TYPE

    except Exception as e:
        logger.error(f"Error refreshing wallet balances: {e}")
        await query.message.edit_text(
            get_text(user_id, "error_refreshing_balances", "listing")
        )
        return State.END


async def process_wallet_selection(
    update: Update, context: ContextTypes.DEFAULT_TYPE, wallet_id: str
) -> int:
    """Process selected wallet and proceed to next step"""
    user_id = update.effective_user.id
    wallet_type = context.user_data.get("wallet_type")

    wallet_details = await WalletService.get_wallet_by_id(wallet_id)
    if not wallet_details:
        await update.callback_query.message.edit_text(
            get_text(user_id, "wallet_not_found"), parse_mode="HTML"
        )
        return State.END

    # Get balance
    total_balance = await WalletManager.get_wallet_balance(
        wallet_details["public_key"], wallet_type
    )

    # Store wallet info
    context.user_data["wallet"] = wallet_details

    # Create case if needed
    if context.user_data.get("action") == "create_case":
        await update_or_create_case(user_id, wallet=str(wallet_details["id"]))

    # Send confirmation message
    msg = get_text(user_id, "wallet_create_details_with_balance").format(
        name=wallet_details["name"],
        public_key=wallet_details["public_key"],
        network=get_network(wallet_details["wallet_type"]),
        balance=total_balance,
        wallet_type=wallet_type,
    )
    transfer_instructions = get_text(user_id, "transfer_instructions").format(
        wallet_type=wallet_type,
        public_key=wallet_details["public_key"],
    )
    msg += transfer_instructions

    await update.callback_query.message.edit_text(msg, parse_mode="HTML")

    # If creating case, proceed to case creation flow
    if context.user_data.get("action") == "create_case":
        await update.callback_query.message.reply_text(
            get_text(user_id, "create_case_title")
        )
        await update.callback_query.message.reply_text(get_text(user_id, "enter_name"))
        return State.CREATE_CASE_NAME

    return State.END


async def handle_extend_reward_flow(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    case_id: str,
    action: str = "view",
) -> int:
    """Unified handler for extend reward flows"""
    user_id = update.effective_user.id
    case = await Case.find_one({"_id": PydanticObjectId(case_id)}, fetch_links=True)
    if not case:
        await update.callback_query.message.edit_text(
            get_text(user_id, "case_not_found")
        )
        return State.END
    # Fetch all pending extend rewards
    extend_rewards = await ExtendReward.find(
        {
            "case.$id": PydanticObjectId(case_id),
            "status": {"$ne": ExtendRewardStatus.COMPLETED},
        }
    ).to_list()
    if not extend_rewards:
        await update.callback_query.message.edit_text(
            get_text(user_id, "extend_reward_not_found")
        )
        return State.END
    # Build case details
    proof_text = (
        f"[Proof]({case.case_photo})"
        if case.case_photo and case.case_photo.startswith("http")
        else get_text(user_id, "no_proof_available", "listing")
    )
    case_details = get_text(user_id, "case_details_template", "listing").format(
        person_name=case.person_name,
        last_seen_location=case.last_seen_location,
        age=case.age or "Unknown",
        reward=case.reward or "0",
        reward_type=case.wallet.wallet_type if case.wallet else "None",
        last_seen_date=(
            case.created_at.strftime("%d %B %Y") if case.created_at else "Unknown"
        ),
        height=case.height or "Unknown",
    )
    full_message = case_details + f"\n<b>Proof:</b> {proof_text}\n\n"
    full_message += get_text(user_id, "extend_reward_header", "listing") + "\n"
    keyboard = []
    for extend_reward in extend_rewards:
        full_message += (
            f"👤 <b>Requested By:</b> <code>{extend_reward.user_id}</code>\n"
        )
        full_message += f"   <b>Amount Requested:</b> {extend_reward.extend_reward_amount} {case.wallet.wallet_type}\n\n"
        if action == "approve":
            keyboard.append(
                [
                    InlineKeyboardButton(
                        f"Approve Extend by {extend_reward.user_id}",
                        callback_data=f"approve_extend_{extend_reward.id}_{case_id}",
                    )
                ]
            )
    # Add cancel button
    if action == "approve":
        keyboard.append(
            [
                InlineKeyboardButton(
                    get_text(user_id, "cancel_button", "listing"),
                    callback_data="cancel_extend",
                )
            ]
        )
    reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None
    await update.callback_query.message.edit_text(
        full_message.strip(),
        reply_markup=reply_markup,
        parse_mode="HTML",
    )
    return State.CONFIRM_EXTEND if action == "approve" else State.CASE_DETAILS


@catch_async
async def enter_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ask the user to enter the country."""
    await update.message.reply_text("🌍 Please enter your country:")
    return State.ENTER_COUNTRY


@catch_async
async def process_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process and validate the country. Update instantly if valid."""
    country = update.message.text.strip()
    country_matches = get_country_matches(country)

    if country_matches:
        selected_country = country_matches[0]
        context.user_data["country"] = selected_country

        # Update the case instantly
        case = context.user_data.get("editing_complaint")
        if case:
            setattr(case, "country", selected_country)
            case.updated_at = datetime.utcnow()
            await case.save()

            # Update the complaint in the listing
            editing_index = context.user_data.get("editing_index", 0)
            complaints = context.user_data.get("listing_complaints", [])
            if editing_index < len(complaints):
                complaints[editing_index] = case

        await update.message.reply_text(
            f"✅ Country updated to <b>{selected_country}</b> successfully!\n"
            "You can now edit other fields or return to the case view."
        )

        # Clear edit context and return to complaint view
        context.user_data.pop("editing_complaint", None)
        context.user_data.pop("editing_field", None)
        context.user_data.pop("editing_index", None)
        context.user_data.pop("country", None)

        # Return to complaint view
        await show_complaint(update.effective_user.id, update, context)
        return State.LISTING.VIEW_COMPLAINTS
    else:
        await update.message.reply_text(
            "❌ Invalid country. Please enter a valid country from the list:\n"
            "- United States\n- Pakistan\n- Canada\n- United Kingdom"
        )
        return State.ENTER_COUNTRY


@catch_async
async def process_province(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Validate the province based on the previously entered country."""
    province = update.message.text.strip()
    country = context.user_data.get("country")

    if not country:
        await update.message.reply_text(
            "❌ No country selected. Please select a country first."
        )
        return State.ENTER_COUNTRY

    provinces = get_province_matches(province, country)

    if provinces:
        case = context.user_data.get("editing_complaint")
        if case:
            setattr(case, "country", country)
            setattr(case, "province", provinces[0])
            case.updated_at = datetime.utcnow()
            await case.save()

            # Update the complaint in the listing
            editing_index = context.user_data.get("editing_index", 0)
            complaints = context.user_data.get("listing_complaints", [])
            if editing_index < len(complaints):
                complaints[editing_index] = case

        await update.message.reply_text(
            f"✅ Great! You've successfully updated:\n"
            f"🌍 Country: <b>{country}</b>\n"
            f"📍 Province: <b>{provinces[0]}</b>"
        )

        # Clear edit context and return to complaint view
        context.user_data.pop("editing_complaint", None)
        context.user_data.pop("editing_field", None)
        context.user_data.pop("editing_index", None)
        context.user_data.pop("country", None)
        context.user_data.pop("province", None)

        # Return to complaint view
        await show_complaint(update.effective_user.id, update, context)
        return State.LISTING.VIEW_COMPLAINTS
    else:
        await update.message.reply_text(
            f"❌ The province <b>{province}</b> is not valid for <b>{country}</b>.\n"
            "Please enter a valid province:"
        )
        return State.ENTER_PROVINCE


@catch_async
async def process_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Validate the city based on the previously entered country and province."""
    city = update.message.text.strip()
    country = context.user_data.get("country")
    province = context.user_data.get("province")

    if not country:
        await update.message.reply_text(
            "❌ No country selected. Please select a country first."
        )
        return State.ENTER_COUNTRY

    cities = get_city_matches(country, city)

    if cities:
        case = context.user_data.get("editing_complaint")
        if case:
            setattr(case, "country", country)
            if province:
                setattr(case, "province", province)
            setattr(case, "city", cities[0])
            case.updated_at = datetime.utcnow()
            await case.save()

            # Update the complaint in the listing
            editing_index = context.user_data.get("editing_index", 0)
            complaints = context.user_data.get("listing_complaints", [])
            if editing_index < len(complaints):
                complaints[editing_index] = case

        success_text = (
            f"✅ Great! You've successfully updated:\n🌍 Country: <b>{country}</b>\n"
        )
        if province:
            success_text += f"📍 Province: <b>{province}</b>\n"
        success_text += f"🏙️ City: <b>{cities[0]}</b>"

        await update.message.reply_text(success_text)

        # Clear edit context and return to complaint view
        context.user_data.pop("editing_complaint", None)
        context.user_data.pop("editing_field", None)
        context.user_data.pop("editing_index", None)
        context.user_data.pop("country", None)
        context.user_data.pop("province", None)

        # Return to complaint view
        await show_complaint(update.effective_user.id, update, context)
        return State.LISTING.VIEW_COMPLAINTS
    else:
        error_text = f"❌ The city <b>{city}</b> is not valid for <b>{country}</b>"
        if province:
            error_text += f" in <b>{province}</b>"
        error_text += ".\nPlease enter a valid city:"
        await update.message.reply_text(error_text)
        return State.ENTER_CITY


@catch_async
async def process_mobile_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process mobile number and send OTP for verification."""
    mobile_number = update.message.text.strip()
    user_id = update.effective_user.id

    # Basic mobile number validation
    if not mobile_number or len(mobile_number) < 10:
        await update.message.reply_text(
            "❌ Please enter a valid mobile number (at least 10 digits)."
        )
        return State.ENTER_MOBILE_NUMBER

    try:
        # Send OTP
        otp_result = await send_otp(mobile_number)

        if otp_result["success"]:
            # Store OTP ID and mobile number in context
            context.user_data["otp_id"] = otp_result["otp_id"]
            context.user_data["mobile_number"] = mobile_number

            # Create keyboard with cancel option
            keyboard = [
                [InlineKeyboardButton("❌ Cancel", callback_data="cancel_mobile_edit")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                f"📱 OTP sent to {mobile_number}.\n"
                "Please enter the OTP code to verify your mobile number:",
                reply_markup=reply_markup,
            )
            return State.VERIFY_MOBILE_OTP
        else:
            await update.message.reply_text(
                f"❌ Failed to send OTP: {otp_result['message']}\n"
                "Please try again with a different number:"
            )
            return State.ENTER_MOBILE_NUMBER

    except Exception as e:
        logger.error(f"Error sending OTP: {e}")
        await update.message.reply_text(
            "❌ An error occurred while sending OTP. Please try again:"
        )
        return State.ENTER_MOBILE_NUMBER


@catch_async
async def verify_mobile_otp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Verify OTP and update mobile number."""
    otp_code = update.message.text.strip()
    user_id = update.effective_user.id

    otp_id = context.user_data.get("otp_id")
    mobile_number = context.user_data.get("mobile_number")

    if not otp_id or not mobile_number:
        await update.message.reply_text("❌ OTP session expired. Please start over.")
        return State.END

    try:
        # Verify OTP
        verify_result = await verify_otp(otp_id, otp_code)

        if verify_result["success"]:
            # Update the case with verified mobile number
            case = context.user_data.get("editing_complaint")
            if case:
                setattr(case, "mobile", mobile_number)
                case.updated_at = datetime.utcnow()
                await case.save()

                # Update the complaint in the listing
                editing_index = context.user_data.get("editing_index", 0)
                complaints = context.user_data.get("listing_complaints", [])
                if editing_index < len(complaints):
                    complaints[editing_index] = case

            await update.message.reply_text(
                f"✅ Mobile number verified and updated successfully!\n"
                f"📱 New mobile number: <b>{mobile_number}</b>"
            )

            # Clear edit context and return to complaint view
            context.user_data.pop("editing_complaint", None)
            context.user_data.pop("editing_field", None)
            context.user_data.pop("editing_index", None)
            context.user_data.pop("otp_id", None)
            context.user_data.pop("mobile_number", None)

            # Return to complaint view
            await show_complaint(user_id, update, context)
            return State.LISTING.VIEW_COMPLAINTS
        else:
            await update.message.reply_text(
                f"❌ Invalid OTP: {verify_result['message']}\n"
                "Please enter the correct OTP code:"
            )
            return State.VERIFY_MOBILE_OTP

    except Exception as e:
        logger.error(f"Error verifying OTP: {e}")
        await update.message.reply_text(
            "❌ An error occurred while verifying OTP. Please try again:"
        )
        return State.VERIFY_MOBILE_OTP


@catch_async
async def cancel_mobile_edit_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Cancel mobile number edit process."""
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id

    # Clear mobile edit context
    context.user_data.pop("otp_id", None)
    context.user_data.pop("mobile_number", None)
    context.user_data.pop("editing_complaint", None)
    context.user_data.pop("editing_field", None)
    context.user_data.pop("editing_index", None)

    await query.message.edit_text("❌ Mobile number edit cancelled.")
    return State.END


@catch_async
async def cancel_delete_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handler to cancel delete request."""
    query = update.callback_query
    await query.answer()

    try:
        if query.message:
            await query.edit_message_text(
                get_text(update.effective_user.id, "delete_cancelled", "listing")
            )
        else:
            await context.bot.send_message(
                chat_id=update.effective_user.id,
                text=get_text(update.effective_user.id, "delete_cancelled", "listing"),
            )
    except Exception as e:
        logger.error(f"Error in cancel_delete_callback: {str(e)}")

    return State.END


@catch_async
async def cancel_edit_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handler for canceling the edit process."""
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id

    try:
        # Clear any edit-related data from context
        context.user_data.pop("editing_complaint", None)
        context.user_data.pop("editing_field", None)
        context.user_data.pop("editing_index", None)

        # Return to complaint view
        await show_complaint(user_id, update, context)
        return State.LISTING.VIEW_COMPLAINTS

    except Exception as e:
        logger.error(
            f"Error in cancel_edit_callback: {str(e)}\n{traceback.format_exc()}"
        )
        await query.message.edit_text(
            get_text(user_id, "error_canceling_edit", "listing")
        )
        return State.END


@catch_async
async def ask_reward_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Asks advertiser how much reward they want to send."""
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    callback_data = query.data.removeprefix("send_reward_")
    finder_id, case_id = callback_data.split("_")

    try:
        case = await Case.find_one({"_id": PydanticObjectId(case_id)}, fetch_links=True)
        finder = await Finder.find_one(
            {"_id": PydanticObjectId(finder_id)}, fetch_links=True
        )

        if not case or not finder:
            await query.message.edit_text(
                get_text(user_id, "case_or_finder_not_found", "listing")
            )
            return State.END

        context.user_data["reward_case_id"] = case.id
        context.user_data["reward_finder_id"] = finder.id

        await query.message.edit_text(
            get_text(user_id, "enter_reward_amount", "listing").format(
                max_amount=case.reward
            ),
            parse_mode="HTML",
        )
        return State.REWARD_TRANSFER_PROCESS

    except Exception as e:
        logger.error(f"Error in ask_reward_amount: {str(e)}\n{traceback.format_exc()}")
        await query.message.edit_text(
            get_text(user_id, "error_asking_reward_amount", "listing")
        )
        return State.END


@catch_async
async def process_reward_transfer(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Shows confirmation before processing reward transfer"""
    user_id = update.effective_user.id
    amount = update.message.text.strip()
    case = context.user_data.get("finder_current_case")
    finder = context.user_data.get("finder_current_finder")

    # Validate amount
    amount = float(amount)
    if amount <= 0 or amount > case.reward:
        raise ValueError("Invalid amount")
    # Store confirmation data
    context.user_data["reward_amount"] = amount
    # Show confirmation buttons
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    get_text(user_id, "confirm_button", "listing"),
                    callback_data="confirm_reward",
                ),
                InlineKeyboardButton(
                    get_text(user_id, "cancel_button", "listing"),
                    callback_data="cancel_reward",
                ),
            ]
        ]
    )
    await update.message.reply_text(
        get_text(user_id, "reward_confirmation", "listing").format(
            amount=amount, finder_id=finder.id, case_no=case.case_no
        ),
        reply_markup=keyboard,
        parse_mode="HTML",
    )
    return State.CONFIRM_REWARD


@catch_async
async def confirm_reward(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Executes the reward transfer after confirmation"""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    case = context.user_data.get("finder_current_case")
    finder = context.user_data.get("finder_current_finder")
    amount = context.user_data.get("reward_amount")

    # i want the consoel.log( like prettier evenly formated)
    print("--------------------------------")
    print("Finders", finder.model_dump_json(indent=4))
    print("--------------------------------")

    finder_wallet = finder.wallet
    wallet_type = finder_wallet.wallet_type
    # Transfer to finder
    is_transfer_to_finder_successful = await WalletManager.send_transfer(
        SOL_WALLET_PRIVATE_KEY if wallet_type == "SOL" else TRON_WALLET_PRIVATE_KEY,
        finder_wallet.public_key,
        amount,
        wallet_type,
    )
    # Transfer tax to collector (if applicable)
    tax_amount = float(case.reward - amount)
    is_tax_transfer_successful = True
    if tax_amount > 0:
        collect_public_key = (
            SOL_COLLECT_PUBLIC_KEY if wallet_type == "SOL" else TRON_COLLECT_PUBLIC_KEY
        )
        is_tax_transfer_successful = await WalletManager.send_transfer(
            (
                SOL_WALLET_PRIVATE_KEY
                if wallet_type == "SOL"
                else TRON_WALLET_PRIVATE_KEY
            ),
            collect_public_key,
            tax_amount,
            wallet_type,
        )
    # Update statuses
    finder.status = FinderStatus.COMPLETED
    case.status = CaseStatus.COMPLETED
    await finder.save()
    await case.save()
    # ✅ OWNER Message
    await query.message.edit_text(
        f"✅ <b>Reward transfer successful!</b>\n"
        f"You have successfully sent <b>{amount} {finder_wallet.wallet_type}</b> to the finder (ID: <code>{finder.user_id}</code>).",
        parse_mode="HTML",
    )
    # ✅ FINDER Message
    await context.bot.send_message(
        chat_id=finder.user_id,
        text=(
            f"🎉 <b>Congratulations!</b>\n"
            f"You’ve received a reward of <b>{amount} {finder_wallet.wallet_type}</b> for your successful contribution.\n"
            f"Thank you for your valuable help! 🙌"
        ),
        parse_mode="HTML",
    )
    # ✅ ADVERTISER Message
    await context.bot.send_message(
        chat_id=case.user_id,
        text=(
            f"📢 <b>Case Update</b>\n"
            f"A reward of <b>{amount} {finder_wallet.wallet_type}</b> has been transferred to the finder "
            f"(ID: <code>{finder.user_id}</code>) for Case No: <b>{case.case_no or 'N/A'}</b>.\n"
            f"The case is now marked as <b>COMPLETED</b> ✅"
        ),
        parse_mode="HTML",
    )
    return State.END


@catch_async
async def cancel_reward(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels the reward process"""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    case = context.user_data.get("finder_current_case")
    finder = context.user_data.get("finder_current_finder")
    amount = context.user_data.get("reward_amount")

    # Clear context data
    context.user_data.pop("finder_current_case", None)
    context.user_data.pop("finder_current_finder", None)
    context.user_data.pop("reward_amount", None)

    await query.message.edit_text(get_text(user_id, "reward_cancelled", "listing"))
    return State.END


# -------------------------- Extend Reward By Advertiser ---------------------------


@catch_async
async def approve_extend_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Approve and process the extend reward request."""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data.removeprefix("approve_extend_")
    extend_reward_id, case_id = data.split("_")

    context.user_data["extend_reward_id"] = extend_reward_id
    context.user_data["case_id"] = case_id

    try:
        # Fetch case and extend reward details
        case = await Case.find_one({"_id": PydanticObjectId(case_id)}, fetch_links=True)
        extend_reward = await ExtendReward.find_one(
            {"_id": PydanticObjectId(extend_reward_id)}
        )

        if not case or not extend_reward:
            await query.message.edit_text(
                get_text(user_id, "case_or_extend_not_found", "listing")
            )
            return State.END

        wallet_type = case.wallet.wallet_type

        # Get all user wallets of the given type
        wallets = await Wallet.find(
            {"user_id": user_id, "wallet_type": wallet_type, "deleted": False}
        ).to_list()

        if not wallets:
            await query.message.edit_text(
                get_text(user_id, "no_wallet_found", "listing")
            )
            return State.END

        # Select the wallet with the highest balance
        wallet_balances = []
        for wallet in wallets:
            balance = await WalletManager.get_wallet_balance(
                wallet.public_key, wallet_type
            )
            wallet_balances.append((wallet, balance))

        wallet_balances.sort(key=lambda x: x[1], reverse=True)
        best_wallet, best_balance = wallet_balances[0]

        # Revalidate the wallet balance
        if best_balance < extend_reward.extend_reward_amount:
            await query.message.edit_text(
                get_text(user_id, "insufficient_funds_after_selection", "listing")
            )
            return State.END

        # Prompt user to select a wallet
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        f"{wallet.name} ({balance:.2f} {wallet_type})",
                        callback_data=f"select_wallet_{wallet.id}",
                    )
                ]
                for wallet, balance in wallet_balances
            ]
            + [
                [
                    InlineKeyboardButton(
                        get_text(user_id, "cancel_button", "listing"),
                        callback_data="cancel_extend",
                    )
                ]
            ]
        )

        # Escape Markdown characters in dynamic content
        confirmation_message = get_text(
            user_id, "select_wallet_for_extend", "listing"
        ).format(
            amount=escape_markdown(str(extend_reward.extend_reward_amount), version=2),
            wallet_type=escape_markdown(wallet_type, version=2),
            from_wallet=escape_markdown(best_wallet.public_key, version=2),
            to_wallet=escape_markdown(SOL_WALLET_PUBLIC_KEY, version=2),
        )

        await query.message.edit_text(
            confirmation_message.strip(),
            reply_markup=keyboard,
            parse_mode="HTML",
        )
        return State.SELECT_WALLET_FOR_EXTEND

    except Exception as e:
        logger.error(f"Error in approve_extend_callback: {str(e)}")
        await query.message.edit_text(
            get_text(user_id, "error_approving_extend", "listing")
        )
        return State.END


@catch_async
async def select_wallet_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Process the selected wallet for extending the reward."""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data.removeprefix("select_wallet_")
    wallet_id = data.split("_")[0]

    extend_reward_id = context.user_data.get("extend_reward_id", None)
    case_id = context.user_data.get("case_id", None)

    # Fetch case and extend reward details
    case = await Case.find_one({"_id": PydanticObjectId(case_id)}, fetch_links=True)
    extend_reward = await ExtendReward.find_one(
        {"_id": PydanticObjectId(extend_reward_id)}
    )
    wallet = await Wallet.find_one({"_id": PydanticObjectId(wallet_id)})

    if not case or not extend_reward or not wallet:
        await query.message.edit_text(
            get_text(user_id, "case_or_extend_not_found", "listing")
        )
        return State.END

    wallet_type = case.wallet.wallet_type

    # Revalidate the wallet balance
    balance = await WalletManager.get_wallet_balance(wallet.public_key, wallet_type)
    if balance < extend_reward.extend_reward_amount:
        await query.message.edit_text(
            get_text(user_id, "insufficient_funds_after_selection", "listing")
        )
        return State.END

    # Store the selected wallet in context for later use
    context.user_data["selected_wallet"] = wallet

    # Show confirmation message
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    get_text(user_id, "confirm_button", "listing"),
                    callback_data=f"confirm_extend_{extend_reward_id}_{case_id}",
                )
            ],
            [
                InlineKeyboardButton(
                    get_text(user_id, "cancel_button", "listing"),
                    callback_data="cancel_extend",
                )
            ],
        ]
    )

    confirmation_message = get_text(
        user_id, "extend_reward_confirmation", "listing"
    ).format(
        amount=extend_reward.extend_reward_amount,
        wallet_type=wallet_type,
        from_wallet=wallet.public_key,
        to_wallet=SOL_WALLET_PUBLIC_KEY,
    )

    await query.message.edit_text(
        confirmation_message.strip(),
        reply_markup=keyboard,
        parse_mode="HTML",
    )

    return State.CONFIRM_EXTEND


@catch_async
async def confirm_extend_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Confirm and process the reward extension."""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    extend_reward_id, case_id = query.data.removeprefix("confirm_extend_").split("_")

    # Fetch case and extend reward details
    case = await Case.find_one({"_id": PydanticObjectId(case_id)}, fetch_links=True)
    extend_reward = await ExtendReward.find_one(
        {"_id": PydanticObjectId(extend_reward_id)}
    )

    if not case or not extend_reward:
        await query.message.edit_text(
            get_text(user_id, "case_or_extend_not_found", "listing")
        )
        return State.END

    # Retrieve the selected wallet from context.user_data
    selected_wallet = context.user_data.get("selected_wallet")
    if not selected_wallet:
        await query.message.edit_text(
            get_text(user_id, "no_wallet_selected", "listing")
        )
        return State.END

    wallet_type = case.wallet.wallet_type
    amount = extend_reward.extend_reward_amount

    # Recheck the wallet balance
    current_balance = await WalletManager.get_wallet_balance(
        selected_wallet.public_key, wallet_type
    )
    if current_balance < amount:
        await query.message.edit_text(
            get_text(user_id, "insufficient_funds_after_selection", "listing")
        )
        return State.END

    try:
        # Perform transfer
        if wallet_type == "SOL":
            success = await WalletService.send_sol(
                selected_wallet.private_key, SOL_WALLET_PUBLIC_KEY, amount
            )
        else:  # USDT
            success = await WalletService.send_usdt(
                selected_wallet.private_key,
                TRON_COLLECT_PUBLIC_KEY,  # Fixed: was SOL_WALLET_PUBLIC_KEY which is incorrect
                amount,
            )

        if not success:
            raise Exception("Transfer failed")

    except Exception as e:
        logger.error(f"Transfer failed: {e}")
        await query.message.edit_text(get_text(user_id, "transfer_failed", "listing"))
        return State.END

    # Update case and extend reward
    case.reward += amount
    await case.save()

    extend_reward.status = ExtendRewardStatus.COMPLETED
    await extend_reward.save()

    await query.message.edit_text(get_text(user_id, "extend_success", "listing"))
    return State.END


@catch_async
async def cancel_extend_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Cancel the extend reward process."""
    query = update.callback_query
    await query.answer()

    await query.message.edit_text(
        get_text(update.effective_user.id, "extend_cancelled")
    )
    return State.END


# ------------------------ Wallet Creation Flow ------------------------
@catch_async
async def advertiser_wallet_type_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle wallet type selection (SOL or USDT)"""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    wallet_type = query.data

    return await handle_wallet_selection(
        update, context, user_id, wallet_type, "create_case"
    )


@catch_async
async def advertiser_wallet_selection_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle wallet selection from list"""
    query = update.callback_query
    await query.answer()

    wallet_id = query.data.replace("wallet_", "")
    return await process_wallet_selection(update, context, wallet_id)


@catch_async
async def advertiser_wallet_name_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle wallet name input"""
    user_id = update.effective_user.id
    wallet_name = update.message.text.strip()

    if not wallet_name:
        await update.message.reply_text(
            get_text(user_id, "wallet_name_empty"), parse_mode="HTML"
        )
        return State.NAME_WALLET

    wallet_type = context.user_data.get("wallet_type")

    wallet = await WalletService.create_wallet(user_id, wallet_type, wallet_name)
    if wallet:
        total_balance = await WalletManager.get_wallet_balance(
            wallet.public_key, wallet_type
        )

        context.user_data["wallet"] = wallet

        msg = get_text(user_id, "wallet_create_details_with_balance").format(
            name=wallet.name,
            public_key=wallet.public_key,
            balance=total_balance,
            wallet_type=wallet_type,
            network=get_network(wallet_type),
        )

        transfer_instructions = get_text(user_id, "transfer_instructions").format(
            wallet_type=wallet_type,
            public_key=wallet.public_key,
        )
        msg += transfer_instructions

        await update.message.reply_text(msg, parse_mode="HTML")
        await update.message.reply_text(get_text(user_id, "create_case_title"))
        await update.message.reply_text(get_text(user_id, "enter_name"))

        return State.CREATE_CASE_NAME
    else:
        await update.message.reply_text(
            get_text(user_id, "wallet_create_err"), parse_mode="HTML"
        )
        return State.END


# ------------------------ Action Handler ------------------------
@catch_async
async def action_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle main action choices (advertise, find_people)"""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    choice = query.data

    if choice == "advertise":
        # From the original code, it goes to CHOOSE_WALLET_TYPE
        kb = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        get_text(user_id, "usdt_wallet"), callback_data="USDT"
                    ),
                    InlineKeyboardButton(
                        get_text(user_id, "sol_wallet"), callback_data="SOL"
                    ),
                ]
            ]
        )
        await query.edit_message_text(
            get_text(user_id, "choose_wallet"), reply_markup=kb
        )
        return State.CHOOSE_WALLET_TYPE

    elif choice == "find_people":
        # Clearing the province
        await query.edit_message_text("Choose Province")
        return State.CHOOSE_PROVINCE

    else:
        await query.edit_message_text(
            get_text(user_id, "invalid_choice"), parse_mode="HTML"
        )
        return State.END


@catch_async
async def update_choose_country(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:

    user_id = update.effective_user.id
    txt = update.message.text.strip()
    matches = get_country_matches(txt)
    if not matches:
        await update.message.reply_text(
            get_text(user_id, "country_not_found"), parse_mode="HTML"
        )
        return State.CHOOSE_COUNTRY
    if len(matches) == 1:
        context.user_data["country"] = matches[0]
        # Choose the country
        await update.message.reply_text("Choose a city:")
        return State.CHOOSE_CITY
    else:

        context.user_data["country_matches"] = matches
        context.user_data["country_page"] = 1

        paginated, total = paginate_list(matches, 1)
        kb = []
        for c in paginated:
            kb.append([InlineKeyboardButton(c, callback_data=f"country_select_{c}")])
        # Pagination buttons
        if total > 1:
            kb.append(
                [
                    InlineKeyboardButton("⬅️", callback_data="country_page_0"),
                    InlineKeyboardButton("➡️", callback_data="country_page_2"),
                ]
            )
        markup = InlineKeyboardMarkup(kb)
        await update.message.reply_text(
            get_text(user_id, "country_multi", "start-complaints").format(
                page=1, total=total
            ),  ## TODO: Getting it from the start command
            reply_markup=markup,
            parse_mode="HTML",
        )
        return State.CHOOSE_COUNTRY


@catch_async
async def country_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id
    if data.startswith("country_select_"):

        country = data.replace("country_select_", "")
        context.user_data["country"] = country

        await query.edit_message_text(
            f"{get_text(user_id, 'country_selected', "start-complaints")} {country}.",  ## TODO: Getting it from the start command
            parse_mode="HTML",
        )
        # Choose the country
        await update.message.reply_text("Choose a city:")
        return State.CHOOSE_CITY
    elif data.startswith("country_page_"):
        page_str = data.replace("country_page_", "")
        try:
            page_num = int(page_str)
            if page_num < 1:
                page_num = 1
        except ValueError:
            page_num = 1
        matches = context.user_data.get("country_matches", [])
        paginated, total = paginate_list(matches, page_num)
        kb = []
        for c in paginated:
            kb.append([InlineKeyboardButton(c, callback_data=f"country_select_{c}")])
        nav_row = []
        if page_num > 1:
            nav_row.append(
                InlineKeyboardButton("⬅️", callback_data=f"country_page_{page_num-1}")
            )
        if page_num < total:
            nav_row.append(
                InlineKeyboardButton("➡️", callback_data=f"country_page_{page_num+1}")
            )
        if nav_row:
            kb.append(nav_row)
        markup = InlineKeyboardMarkup(kb)
        await query.edit_message_text(
            get_text(user_id, "country_multi", "start-complaints").format(
                page=page_num, total=total
            ),  ## TODO: Getting it from the start command
            reply_markup=markup,
            parse_mode="HTML",
        )

        context.user_data["country_page"] = page_num
        return State.CHOOSE_COUNTRY
    else:
        await query.edit_message_text(
            get_text(user_id, "invalid_choice", "start-complaints"),
            parse_mode="HTML",  ## TODO: Getting it from the start command
        )
        return State.END


@catch_async
async def choose_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    city_input = update.message.text.strip()
    country = context.user_data.get("country")
    if not country:
        await update.message.reply_text(
            get_text(user_id, "invalid_choice", "start-complaints"),
            parse_mode="HTML",  ## TODO: Getting it from the start command
        )
        return State.END
    matches = get_city_matches(country, city_input)
    if not matches:
        await update.message.reply_text(
            get_text(user_id, "city_not_found", "start-complaints"),
            parse_mode="HTML",  ## TODO: Getting it from the start command
        )
        return State.CHOOSE_CITY
    if len(matches) == 1:
        context.user_data["city"] = matches[0]
        await update.message.reply_text(
            f"{get_text(user_id, 'city_selected', "start-complaints")} {matches[0]}",  ## TODO: Getting it from the start command
            parse_mode="HTML",
        )
        update.message.reply_text("Updated Successfully")
        return State.END
    else:
        context.user_data["city_matches"] = matches
        context.user_data["city_page"] = 1
        paginated, total = paginate_list(matches, 1)
        kb = []
        for c in paginated:
            kb.append([InlineKeyboardButton(c, callback_data=f"city_select_{c}")])
        # Pagination
        if total > 1:
            kb.append(
                [
                    InlineKeyboardButton("⬅️", callback_data="city_page_0"),
                    InlineKeyboardButton("➡️", callback_data="city_page_2"),
                ]
            )
        markup = InlineKeyboardMarkup(kb)
        await update.message.reply_text(
            get_text(user_id, "city_multi", "start-complaints").format(
                page=1, total=total
            ),  ## TODO: Getting it from the start command
            reply_markup=markup,
            parse_mode="HTML",
        )
        return State.CHOOSE_CITY


@catch_async
async def city_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data
    if data.startswith("city_select_"):
        city = data.replace("city_select_", "")
        context.user_data["city"] = city
        await update_or_create_case(user_id, city=city)

        await query.edit_message_text(
            f"{get_text(user_id, 'city_selected')} {city}",
            parse_mode="HTML",  ## TODO: Getting it from the start command
        )
        # Return to main menu or appropriate state
        return State.CHOOSE_ACTION
    elif data.startswith("city_page_"):
        page_str = data.replace("city_page_", "")
        try:
            page_num = int(page_str)
            if page_num < 1:
                page_num = 1
        except ValueError:
            page_num = 1
        matches = context.user_data.get("city_matches", [])
        paginated, total = paginate_list(matches, page_num)
        kb = []
        for c in paginated:
            kb.append([InlineKeyboardButton(c, callback_data=f"city_select_{c}")])
        nav_row = []
        if page_num > 1:
            nav_row.append(
                InlineKeyboardButton("⬅️", callback_data=f"city_page_{page_num-1}")
            )
        if page_num < total:
            nav_row.append(
                InlineKeyboardButton("➡️", callback_data=f"city_page_{page_num+1}")
            )
        if nav_row:
            kb.append(nav_row)
        markup = InlineKeyboardMarkup(kb)
        await query.edit_message_text(
            get_text(user_id, "city_multi", "start-complaints").format(
                page=page_num, total=total
            ),  ## TODO: Getting it from the start command
            reply_markup=markup,
            parse_mode="HTML",
        )
        context.user_data["city_page"] = page_num
        return State.CHOOSE_CITY
    else:
        await query.edit_message_text(
            get_text(user_id, "invalid_choice", "start-complaints"), parse_mode="HTML"
        )
        return State.END


# ------------------------
# 🔍 FINDER NAVIGATION HANDLERS
# ------------------------


@catch_async
async def finder_detail_navigation_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle navigation between individual finder details."""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = query.data

    try:
        # Parse navigation data
        if data.startswith("finder_next_"):
            parts = data.removeprefix("finder_next_").split("_")
            finder_index = int(parts[0]) + 1
            case_id_str = parts[1]
        elif data.startswith("finder_prev_"):
            parts = data.removeprefix("finder_prev_").split("_")
            finder_index = max(0, int(parts[0]) - 1)
            case_id_str = parts[1]
        else:
            await MessageHandler.send_error_message(update, user_id, "invalid_action")
            return State.END

        # Get case and finders
        case_id = PydanticObjectId(case_id_str)
        case = await Case.find_one({"_id": case_id, "deleted": False}, fetch_links=True)
        finders = context.user_data.get("case_finders", [])

        if not case or not finders or finder_index >= len(finders):
            await MessageHandler.send_error_message(update, user_id, "case_not_found")
            return State.END

        # Get the finder at the new index
        finder = finders[finder_index]

        # Build detailed finder information
        detail_card = FinderDisplayBuilder.build_finder_detail_text(
            case, finder, user_id
        )
        keyboard = await FinderDisplayBuilder.build_finder_detail_keyboard(
            finder, case, user_id, finder_index, len(finders)
        )
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Update current finder index in context
        context.user_data["current_finder_index"] = finder_index

        await MessageHandler.send_or_edit_message(
            update, detail_card, reply_markup, "HTML"
        )
        return State.CASE_DETAILS

    except Exception as e:
        logger.error(f"Finder detail navigation error: {e}")
        await MessageHandler.send_error_message(
            update, user_id, "error_processing_request"
        )
        return State.END


@catch_async
async def view_finder_proof_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Show finder proof images/videos."""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = query.data.removeprefix("view_proof_")
    finder_id_str, case_id_str = data.split("_", 1)

    try:
        finder_id = PydanticObjectId(finder_id_str)
        finder = await Finder.find_one({"_id": finder_id}, fetch_links=True)

        if not finder or not finder.proof_url:
            await MessageHandler.send_error_message(
                update, user_id, "no_proof_available"
            )
            return State.END

        # Send proof images/videos
        proof_text = f"🖼️ <b>Proof provided by Finder ID: {finder.user_id}</b>\n\n"

        for i, proof_url in enumerate(finder.proof_url, 1):
            proof_text += f"📎 Proof {i}: <a href='{proof_url}'>View</a>\n"

        # Add back button
        keyboard = [
            [
                InlineKeyboardButton(
                    "◀️ Back to Finder Details",
                    callback_data=f"finder_details_{finder_id}_{case_id_str}",
                )
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await MessageHandler.send_or_edit_message(
            update, proof_text, reply_markup, "HTML"
        )
        return State.CASE_DETAILS

    except Exception as e:
        logger.error(f"View proof error: {e}")
        await MessageHandler.send_error_message(update, user_id, "error_viewing_proof")
        return State.END


@catch_async
async def back_to_case_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle going back to case view from finder details."""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = query.data.removeprefix("back_to_case_")
    case_id_str = data

    try:
        case_id = PydanticObjectId(case_id_str)
        case = await Case.find_one({"_id": case_id, "deleted": False}, fetch_links=True)

        if not case:
            await MessageHandler.send_error_message(update, user_id, "case_not_found")
            return State.END

        # Get chat info and finder count in parallel
        chat_task = context.bot.get_chat(case.user_id)
        finder_count_task = Finder.find(
            {"case.$id": case.id, "status": FinderStatus.FIND.value}
        ).count()
        chat, finder_count = await asyncio.gather(chat_task, finder_count_task)

        # Build case display components
        text = CaseDisplayBuilder.build_case_text(case, 1, 1, chat, finder_count)
        keyboard = CaseDisplayBuilder.build_case_keyboard(
            case, 0, 1, finder_count, user_id
        )
        reply_markup = InlineKeyboardMarkup(keyboard)

        await MessageHandler.send_or_edit_message(update, text, reply_markup, "HTML")
        return State.CASE_DETAILS

    except Exception as e:
        logger.error(f"Error in back_to_case_callback: {e}")
        await MessageHandler.send_error_message(
            update, user_id, "error_processing_request"
        )
        return State.END
