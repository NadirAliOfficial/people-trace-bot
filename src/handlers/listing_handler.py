import logging
from datetime import datetime
from typing import List, Optional, Tuple, Dict, Any
from beanie import PydanticObjectId
from config.config_manager import (
    OWNER_TELEGRAM_ID,
    SOL_WALLET_PRIVATE_KEY,
    SOL_WALLET_PUBLIC_KEY,
    SOL_COLLECT_PUBLIC_KEY,
    TRON_COLLECT_PUBLIC_KEY,
    TRON_WALLET_PRIVATE_KEY,
)
from constant.language_constant import get_text, user_data_store
from constants import State
from models.case_model import Case, CaseStatus
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, error, CallbackQuery
from telegram.helpers import escape_markdown
from telegram.ext import ContextTypes
from bson import ObjectId, errors
import traceback
from models.extend_reward_model import ExtendReward, ExtendRewardStatus
from models.finder_model import Finder, FinderStatus
from models.wallet_model import Wallet
from services.case_service import update_case, update_or_create_case
from services.finder_service import FinderService
from services.tron_wallet_service import TronWallet
from services.user_service import get_user_lang
from services.wallet_service import WalletService
from utils.get_network import get_network
from utils.logger import logger
from utils.error_wrapper import catch_async
from utils.helper import get_city_matches, get_country_matches, get_username, paginate_list

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

# ------------------------
# 🚀 MAIN HANDLERS
# ------------------------

@catch_async
async def listing_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display paginated list of ADVERTISE cases."""
    user_id = update.effective_user.id
    lang = await get_user_lang(user_id) or "en"
    context.user_data["lang"] = lang

    # Fetch all advertise cases, newest first
    all_cases = await Case.find(
        {"status": CaseStatus.ADVERTISE, "deleted": False}
    ).sort(-Case.created_at).to_list()

    if not all_cases:
        msg = get_text(user_id, "no_advertise_cases", "listing")
        await _send_message_or_edit(update, msg)
        return State.END

    # Initialize pagination
    context.user_data["listing_complaints"] = all_cases
    context.user_data["listing_index"] = 0  # start at first case

    await show_complaint(user_id, update, context)
    return State.LISTING.VIEW_COMPLAINTS



async def show_complaint(user_id: int, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display a single complaint with navigation and action buttons."""
    complaints = context.user_data["listing_complaints"]
    index = context.user_data["listing_index"]
    total = len(complaints)
    case = complaints[index]

    try:
        chat = await context.bot.get_chat(case.user_id)
        finder_count = await Finder.find(
            {"case.$id": case.id, "status": FinderStatus.FIND.value}
        ).count()

        # Build case display text
        text = _build_case_display_text(case, index + 1, total, chat, finder_count)
        
        # Build keyboard with navigation and actions
        keyboard = _build_case_keyboard(case, index, total, finder_count, user_id)
        
        # Send message with photo or text
        await _send_case_message(update, case, text, keyboard)
        
    except Exception as e:
        logger.error(f"Error showing complaint: {e}")
        await _send_message_or_edit(update, get_text(user_id, "error_displaying_case", "listing"))


@catch_async
async def listing_complaint_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
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

    # Handle edit action
    elif data.startswith("edit_"):
        return await _handle_edit_action(query, context, user_id, data, complaints)

    # Handle delete action
    elif data.startswith("delete_"):
        return await _handle_delete_action(query, context, user_id, data, complaints)

    # Handle reward action
    elif data.startswith("reward_"):
        return await _handle_reward_action(query, context, user_id, data, complaints)

    else:
        await query.message.edit_text(get_text(user_id, "invalid_action", "listing"))
        return State.END


# ======================================================================================================================
# Helper Functions for Case Display and Actions
# ======================================================================================================================
def _build_case_display_text(case: Case, case_num: int, total: int, chat, finder_count: int) -> str:
    """Build the display text for a case."""
    return (
        f"🔍 Case {case_num}/{total}\n"
        f"👤 Name: {case.person_name}\n"
        f"📍 Last Seen: {case.last_seen_location}\n"
        f"📅 Date: {case.created_at.strftime('%d %B %Y')}\n"
        f"🎂 Age: {case.age}\n"
        f"💰 Reward: {case.reward} {case.reward_type or 'N/A'}\n"
        f"🧾 Posted by: @{get_username(chat)}\n"
        f"👥 Finders: {finder_count}"
    )


def _build_case_keyboard(case: Case, index: int, total: int, finder_count: int, user_id: int) -> List[List[InlineKeyboardButton]]:
    """Build the keyboard for case actions and navigation."""
    keyboard = []
    
    # Action buttons (only for case owner)
    if case.user_id == user_id:
        keyboard.extend([
            [InlineKeyboardButton("🧩 Edit", callback_data=f"edit_{index}")],
            [InlineKeyboardButton("🧩 DELETE", callback_data=f"delete_{index}")]
        ])

    # Navigation buttons
    nav_row = []
    if index > 0:
        nav_row.append(InlineKeyboardButton("◀️ Back", callback_data=f"complaint_back_{index}"))
    if index < total - 1:
        nav_row.append(InlineKeyboardButton("▶️ Next", callback_data=f"complaint_next_{index}"))
    if nav_row:
        keyboard.append(nav_row)

    # Finder button
    if finder_count > 0:
        keyboard.append([
            InlineKeyboardButton(f"📬 View Finder ({finder_count})", callback_data=f"reward_{index}")
        ])

    return keyboard


async def _send_case_message(update: Update, case: Case, text: str, keyboard: List[List[InlineKeyboardButton]]) -> None:
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
        await _send_message_or_edit(update, text, reply_markup)


async def _send_message_or_edit(update: Update, text: str, reply_markup: Optional[InlineKeyboardMarkup] = None) -> None:
    """Send message or edit existing message based on update type."""
    try:
        if update.message:
            await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="HTML")
        elif update.callback_query:
            if update.callback_query.message.photo:
                await update.callback_query.edit_message_caption(
                    caption=text, reply_markup=reply_markup, parse_mode="HTML"
                )
            else:
                await update.callback_query.edit_message_text(
                    text, reply_markup=reply_markup, parse_mode="HTML"
                )
    except error.BadRequest as e:
        if "message is not modified" in str(e):
            # Ignore duplicate message errors
            logger.info("Message not modified - ignoring duplicate")
        else:
            raise


async def _handle_edit_action(query: CallbackQuery, context: ContextTypes.DEFAULT_TYPE, user_id: int, data: str, complaints: List[Case]) -> int:
    """Handle edit action for a case."""
    try:
        selected_index = int(data.split("_")[1])
        if selected_index >= len(complaints):
            await query.message.edit_text(get_text(user_id, "case_not_found", "listing"))
            return State.END

        selected_complaint = complaints[selected_index]
        if not selected_complaint:
            await query.message.edit_text(get_text(user_id, "case_not_found", "listing"))
            return State.END

        # Build edit fields keyboard
        editable_fields = get_text(user_id, "editable_fields", "listing")
        keyboard = _build_edit_fields_keyboard(editable_fields)
        
        new_text = get_text(user_id, "edit_field_prompt", "listing")
        reply_markup = InlineKeyboardMarkup(keyboard)

        await _send_message_or_edit(Update(callback_query=query), new_text, reply_markup)
        context.user_data["editing_complaint"] = selected_complaint
        return State.CASE_DETAILS

    except (ValueError, IndexError) as e:
        logger.error(f"Error in edit action: {e}")
        await query.message.edit_text(get_text(user_id, "invalid_case_index", "listing"))
        return State.END


async def _handle_delete_action(query: CallbackQuery, context: ContextTypes.DEFAULT_TYPE, user_id: int, data: str, complaints: List[Case]) -> int:
    """Handle delete action for a case."""
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
                InlineKeyboardButton("✅ Confirm Delete", callback_data="confirm_delete"),
                InlineKeyboardButton("❌ Cancel", callback_data="cancel_delete"),
            ]
        ]

        new_text = (
            f"⚠️ Are you sure you want to delete case:\n\n"
            f"👤 {selected_complaint.person_name}\n"
            f"📍 {selected_complaint.last_seen_location}"
        )

        await _send_message_or_edit(Update(callback_query=query), new_text, InlineKeyboardMarkup(keyboard))
        return State.CASE_DETAILS

    except (ValueError, IndexError) as e:
        logger.error(f"Error in delete action: {e}")
        await query.answer("❌ Invalid case index", show_alert=True)
        return State.LISTING.VIEW_COMPLAINTS


async def _handle_reward_action(query: CallbackQuery, context: ContextTypes.DEFAULT_TYPE, user_id: int, data: str, complaints: List[Case]) -> int:
    """Handle reward action for a case."""
    try:
        selected_index = int(data.split("_")[1])
        if selected_index >= len(complaints):
            await query.message.edit_text(get_text(user_id, "case_not_found", "listing"))
            return State.END

        selected_complaint = complaints[selected_index]
        context.user_data["selected_complaint"] = selected_complaint
        
        # Continue to reward flow
        return await reward_case_callback(Update(callback_query=query), context)

    except (ValueError, IndexError) as e:
        logger.error(f"Error in reward action: {e}")
        await query.message.edit_text(get_text(user_id, "invalid_case_index", "listing"))
        return State.END


def _build_edit_fields_keyboard(editable_fields: Dict[str, str]) -> List[List[InlineKeyboardButton]]:
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
    keyboard.append([
        InlineKeyboardButton("Cancel", callback_data="cancel_edit")
    ])
    
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

    # Handle special cases for country and city
    if field_name == "country":
        await _send_message_or_edit(Update(callback_query=query), "🌍 Please enter your country:")
        return State.ENTER_COUNTRY
    elif field_name == "city":
        if "country" not in context.user_data:
            await _send_message_or_edit(Update(callback_query=query), "🌍 Please enter your country first:")
            return State.ENTER_COUNTRY
        await _send_message_or_edit(Update(callback_query=query), "🏙️ Please enter your city:")
        return State.ENTER_CITY
    
    # Handle other fields
    text = get_text(user_id, "enter_new_value", "listing").format(
        field_name=field_name.replace("_", " ").title()
    )
    await _send_message_or_edit(Update(callback_query=query), text)
    return State.EDIT_FIELD

@catch_async
async def update_case_field(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Update the specified field in the case document."""
    case = context.user_data.get("editing_complaint")
    field_name = context.user_data.get("editing_field")
    user_id = update.effective_user.id
    new_value = update.message.text.strip()
    
    # Validate case exists
    if not case:
        await update.message.reply_text(get_text(user_id, "case_not_found", "listing"))
        return State.HANDLER_END
    
    try:
        # Validate and process field value
        processed_value = await _validate_and_process_field_value(field_name, new_value, context)
        
        # Update the case document
        setattr(case, field_name, processed_value)
        case.updated_at = datetime.utcnow()
        await case.save()
        
        # Send success message
        success_text = get_text(user_id, "field_updated_successfully", "listing").format(
            field_name=field_name.replace("_", " ").title(),
            new_value=processed_value,
        )
        await update.message.reply_text(success_text, parse_mode="Markdown")
        
    except ValueError as e:
        await update.message.reply_text(
            get_text(user_id, "invalid_value", "listing").format(error_message=str(e))
        )
        return State.EDIT_FIELD
    except Exception as e:
        logger.error(f"Error updating case field: {e}")
        await update.message.reply_text(get_text(user_id, "error_updating_field", "listing"))
        return State.HANDLER_END
    
    return State.HANDLER_END


async def _validate_and_process_field_value(field_name: str, new_value: str, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Validate and process field value based on field type."""
    if field_name == "country":
        country_matches = get_country_matches(new_value)
        if not country_matches:
            raise ValueError("Invalid country. Please provide a valid country.")
        return country_matches[0]
    elif field_name == "city":
        country = context.user_data.get("country")
        city_matches = get_city_matches(country, new_value)
        if not city_matches:
            raise ValueError(f"Invalid city for country {country}.")
        return city_matches[0]
    else:
        return new_value


@catch_async
async def delete_case_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handler for confirming and soft deleting a case."""
    query = update.callback_query
    print("calling from the delete case callback", query.data)
    await query.answer()

    case = context.user_data.get("deleting_complaint", None)
    user_id = update.effective_user.id

    if not case:
        await query.message.edit_text(get_text(user_id, "case_not_found", "listing"))
        return State.HANDLER_END

    # Authorization check
    if case.user_id != user_id:
        if query.message.photo:
            await query.edit_message_caption(get_text(user_id, "not_authorized_delete", "listing"))
        else:
            await query.edit_message_text(get_text(user_id, "not_authorized_delete", "listing"))
        return State.HANDLER_END

    # Soft delete
    await update_case(case_id=PydanticObjectId(case.id), deleted=True)

    # Send success message
    success_text = get_text(user_id, "case_deleted_successfully", "listing")
    if query.message.photo:
        await query.edit_message_caption(success_text)
    else:
        await query.edit_message_text(success_text)

    # Show updated listing
    return await listing_command(update, context)



# ------------------------
# 🎯 REWARD FINDER FLOW
# ------------------------

@catch_async
async def reward_case_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show list of finders for a case."""
    query = update.callback_query
    await query.answer()

    case_id_str = query.data.removeprefix("reward_")
    try:
        case_id = PydanticObjectId(case_id_str)
        case = await Case.find_one({"_id": case_id, "deleted": False}, fetch_links=True)
        if not case:
            await query.message.edit_text(get_text(query.from_user.id, "case_not_found", "listing"), parse_mode="MarkdownV2")
            return State.END

        finders = await Finder.find(
            {"case.$id": case_id, "status": FinderStatus.FIND}
        ).to_list()

        if not finders:
            await query.message.edit_text(get_text(query.from_user.id, "no_finders_for_case", "listing"), parse_mode="MarkdownV2")
            return State.END

        # Format finder list header
        header = _format_finder_list_card(case, finders, query.from_user.id, context.user_data.get("lang", "en"))

        # Create finder buttons
        keyboard = []
        for finder in finders:
            keyboard.append([
                InlineKeyboardButton(
                    f"👤 Finder ID: {finder.user_id}",
                    callback_data=f"finder_details_{finder.id}_{case_id}"
                )
            ])

        keyboard.append([InlineKeyboardButton("◀️ Back to Case", callback_data=f"case_{case_id}")])

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.edit_text(header, reply_markup=reply_markup, parse_mode="MarkdownV2")
        return State.CASE_DETAILS

    except Exception as e:
        logger.error(f"Reward callback error: {e}")
        await query.message.edit_text(get_text(query.from_user.id, "error_processing_reward", "listing"), parse_mode="MarkdownV2")
        return State.END


@catch_async
async def finder_details_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show detailed finder info and reward button."""
    query = update.callback_query
    await query.answer()

    data = query.data.removeprefix("finder_details_")
    finder_id_str, case_id_str = data.split("_", 1)

    try:
        case_id = PydanticObjectId(case_id_str)
        finder_id = PydanticObjectId(finder_id_str)

        case = await Case.find_one({"_id": case_id, "deleted": False}, fetch_links=True)
        finder = await Finder.find_one({"_id": finder_id, "status": FinderStatus.FIND}, fetch_links=True)

        if not case or not finder:
            await query.message.edit_text(get_text(query.from_user.id, "case_or_finder_not_found", "listing"), parse_mode="MarkdownV2")
            return State.END

        # Format finder detail card
        detail_card = _format_finder_detail_card(case, finder, query.from_user.id, context.user_data.get("lang", "en"))

        # Only show reward button if user is case owner or admin
        keyboard = []
        if str(query.from_user.id) == str(case.user_id) or str(query.from_user.id) == str(OWNER_TELEGRAM_ID):
            keyboard.append([
                InlineKeyboardButton(
                    "💸 Send Reward",
                    callback_data=f"send_reward_{finder_id}_{case_id}"
                )
            ])

        keyboard.append([InlineKeyboardButton("◀️ Back to Finders", callback_data=f"reward_{case_id}")])

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.edit_text(detail_card, reply_markup=reply_markup, parse_mode="MarkdownV2")
        return State.CASE_DETAILS

    except Exception as e:
        logger.error(f"Finder details error: {e}")
        await query.message.edit_text(get_text(query.from_user.id, "error_fetching_finder", "listing"), parse_mode="MarkdownV2")
        return State.END




# ------------------------
# 🔄 EXTEND REWARD FLOW
# ------------------------

@catch_async
async def extend_reward_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show pending extend reward requests for this case."""
    query = update.callback_query
    await query.answer()

    case_id_str = query.data.removeprefix("extend_reward_")
    try:
        case_id = PydanticObjectId(case_id_str)
        case = await Case.find_one({"_id": case_id, "deleted": False}, fetch_links=True)
        if not case:
            await query.message.edit_text(get_text(query.from_user.id, "case_not_found", "listing"), parse_mode="MarkdownV2")
            return State.END

        # Fetch all pending extend rewards
        extend_rewards = await ExtendReward.find(
            {"case.$id": case_id, "status": {"$ne": ExtendRewardStatus.COMPLETED}}
        ).to_list()

        if not extend_rewards:
            await query.message.edit_text(get_text(query.from_user.id, "extend_reward_not_found", "listing"), parse_mode="MarkdownV2")
            return State.END

        # Format case header
        header = _format_case_card(case, query.from_user.id, context.user_data.get("lang", "en"))
        header += "\n\n🔄 **Pending Extend Requests:**\n"

        keyboard = []
        for er in extend_rewards:
            header += f"👤 Requested by: `{er.user_id}` | Amount: {er.extend_reward_amount} {case.wallet.wallet_type}\n"
            keyboard.append([
                InlineKeyboardButton(
                    f"✅ Approve {er.extend_reward_amount} {case.wallet.wallet_type}",
                    callback_data=f"approve_extend_{er.id}_{case_id}"
                )
            ])

        keyboard.append([InlineKeyboardButton("◀️ Back to Case", callback_data=f"case_{case_id}")])

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.edit_text(header.strip(), reply_markup=reply_markup, parse_mode="MarkdownV2")
        return State.CONFIRM_EXTEND

    except Exception as e:
        logger.error(f"Extend reward callback error: {e}")
        await query.message.edit_text(get_text(query.from_user.id, "error_approving_extend", "listing"), parse_mode="MarkdownV2")
        return State.END




# ------------------------
# UTILITY FUNCTIONS (REFACTORED TO AVOID DUPLICATION)
# ------------------------

async def get_case_with_validation(case_id_str: str, user_id: int, context: ContextTypes.DEFAULT_TYPE) -> tuple[Case, bool]:
    """Helper to fetch case with validation and error handling"""
    try:
        case_id = PydanticObjectId(case_id_str)
        case = await Case.find_one(
            {"_id": case_id, "deleted": False}, 
            fetch_links=True
        )
        if not case:
            await context.bot.send_message(
                chat_id=user_id, 
                text=get_text(user_id, "case_not_found", "listing")
            )
            return None, False
        
        # Check authorization if needed
        if case.user_id != user_id:
            await context.bot.send_message(
                chat_id=user_id, 
                text=get_text(user_id, "not_authorized", "listing")
            )
            return None, False
            
        return case, True
    except (errors.InvalidId, Exception) as e:
        logger.error(f"Error validating case {case_id_str}: {e}")
        await context.bot.send_message(
            chat_id=user_id, 
            text=get_text(user_id, "invalid_case_id", "listing")
        )
        return None, False

async def send_wallet_transfer(
    private_key: str, 
    recipient_address: str, 
    amount: float, 
    wallet_type: str
) -> bool:
    """Unified wallet transfer function"""
    try:
        if wallet_type == "SOL":
            return await WalletService.send_sol(private_key, recipient_address, amount)
        elif wallet_type == "USDT":
            return await TronWallet.transfer_usdt(private_key, recipient_address, amount)
        else:
            logger.error(f"Unsupported wallet type: {wallet_type}")
            return False
    except Exception as e:
        logger.error(f"Transfer failed for {wallet_type}: {e}")
        return False

async def get_wallet_balance(wallet_public_key: str, wallet_type: str) -> float:
    """Unified wallet balance getter with refresh capability"""
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


async def refresh_wallet_balance(wallet_public_key: str, wallet_type: str) -> Tuple[float, bool]:
    """Refresh wallet balance and return updated balance with success status"""
    try:
        # Force refresh by making a new request
        if wallet_type == "SOL":
            balance = await WalletService.get_sol_balance(wallet_public_key, force_refresh=True)
        elif wallet_type == "USDT":
            balance = await TronWallet.get_usdt_balance(wallet_public_key, force_refresh=True)
        else:
            logger.error(f"Unsupported wallet type for refresh: {wallet_type}")
            return 0.0, False
        
        return balance, True
    except Exception as e:
        logger.error(f"Error refreshing balance for {wallet_type}: {e}")
        return 0.0, False


def _format_finder_list_card(case: Case, finders: List[Finder], user_id: int, lang: str) -> str:
    """Format finder list card display text."""
    return (
        f"🔍 **Case Details:**\n"
        f"👤 Name: {case.person_name}\n"
        f"📍 Location: {case.last_seen_location}\n"
        f"💰 Reward: {case.reward} {case.wallet.wallet_type if case.wallet else 'N/A'}\n\n"
        f"👥 **Finders ({len(finders)}):**\n"
        f"Select a finder to view details and send reward."
    )


def _format_finder_detail_card(case: Case, finder: Finder, user_id: int, lang: str) -> str:
    """Format finder detail card display text."""
    return (
        f"🔍 **Case:** {case.person_name}\n"
        f"📍 Location: {case.last_seen_location}\n"
        f"💰 Reward: {case.reward} {case.wallet.wallet_type if case.wallet else 'N/A'}\n\n"
        f"👤 **Finder Details:**\n"
        f"ID: `{finder.user_id}`\n"
        f"Status: {finder.status.value}\n"
        f"Found Date: {finder.created_at.strftime('%d %B %Y') if finder.created_at else 'N/A'}"
    )


def _format_case_card(case: Case, user_id: int, lang: str) -> str:
    """Format case card display text."""
    return (
        f"🔍 **Case Details:**\n"
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
    show_reward_button: bool = False
) -> InlineKeyboardMarkup:
    """Create a standardized pagination keyboard"""
    keyboard = []
    
    # Case buttons
    paginated_cases, _ = paginate_list(cases, page)
    for case in paginated_cases:
        row = [
            InlineKeyboardButton(
                f"{case.person_name} ({case.id})",
                callback_data=f"case_{str(case.id)}"
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
                    callback_data=f"edit_{str(case.id)}"
                )
            )
            row.append(
                InlineKeyboardButton(
                    get_text(user_id, "delete_button", "listing"),
                    callback_data=f"delete_{str(case.id)}"
                )
            )
        
        # Reward button (only for owner and finder exists)
        if show_reward_button and str(user_id) == str(OWNER_TELEGRAM_ID) and finder_exist:
            row.append(
                InlineKeyboardButton(
                    "Reward Finder",
                    callback_data=f"reward_{str(case.id)}"
                )
            )
        
        # Extend reward button (only for owner and pending extend reward)
        extend_reward = await ExtendReward.find_one(
            {"case.$id": PydanticObjectId(case.id), "status": {"$ne": ExtendRewardStatus.COMPLETED}}
        )
        if case.status == CaseStatus.ADVERTISE and extend_reward and case.user_id == user_id:
            row.append(
                InlineKeyboardButton(
                    get_text(user_id, "extend_reward_button", "listing"),
                    callback_data=f"extend_reward_{str(case.id)}"
                )
            )
            
        keyboard.append(row)
    
    # Navigation buttons
    navigation_buttons = []
    if page > 1:
        navigation_buttons.append(
            InlineKeyboardButton(
                get_text(user_id, "prev", "globals"), 
                callback_data="page_previous"
            )
        )
    if page < total_pages:
        navigation_buttons.append(
            InlineKeyboardButton(
                get_text(user_id, "next", "globals"), 
                callback_data="page_next"
            )
        )
    
    if navigation_buttons:
        keyboard.append(navigation_buttons)
        
    return InlineKeyboardMarkup(keyboard)

async def send_case_details(
    update: Update, 
    context: ContextTypes.DEFAULT_TYPE, 
    case: Case,
    show_edit_delete: bool = True
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
        last_seen_date=case.created_at.strftime("%d %B %Y") if case.created_at else "Unknown",
        height=case.height or "Unknown",
    )
    case_message += f"\n**Proof:** {proof_text}"
    
    # Prepare buttons
    keyboard = []
    if show_edit_delete and case.user_id == user_id:
        row = [
            InlineKeyboardButton(
                get_text(user_id, "edit_button", "listing"), 
                callback_data=f"edit_{str(case.id)}"
            ),
            InlineKeyboardButton(
                get_text(user_id, "delete_button", "listing"), 
                callback_data=f"delete_{str(case.id)}"
            ),
        ]
        keyboard.append(row)
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Send message
    if isinstance(update, Update) and update.callback_query:
        await update.callback_query.message.edit_text(
            case_message.strip(),
            reply_markup=reply_markup,
            parse_mode="Markdown",
        )
    elif isinstance(update, Update) and update.message:
        await update.message.reply_text(
            case_message.strip(),
            reply_markup=reply_markup,
            parse_mode="Markdown",
        )

async def handle_wallet_selection(
    update: Update, 
    context: ContextTypes.DEFAULT_TYPE,
    user_id: int,
    wallet_type: str,
    action: str = "create_case"
) -> int:
    """Unified handler for wallet selection flow with refresh capability"""
    existing_wallets = await WalletService.get_wallet_by_type(user_id, wallet_type)
    
    if existing_wallets:
        kb = []
        for wallet in existing_wallets:
            # Get current balance for display
            balance = await get_wallet_balance(wallet.public_key, wallet_type)
            kb.append([InlineKeyboardButton(
                f"{wallet.name} ({balance:.4f} {wallet_type})", 
                callback_data=f"wallet_{str(wallet.id)}"
            )])
        
        # Add refresh and create new wallet buttons
        kb.extend([
            [InlineKeyboardButton(
                "🔄 Refresh Balances", 
                callback_data="refresh_wallet_balances"
            )],
            [InlineKeyboardButton(
                get_text(user_id, "create_new_wallet"),
                callback_data="create_new_wallet"
            )]
        ])
        
        message = get_text(user_id, "choose_existing_or_new_wallet")
    else:
        kb = []
        message = get_text(user_id, "wallet_name_prompt")
    
    reply_markup = InlineKeyboardMarkup(kb)
    
    if update.callback_query:
        await update.callback_query.message.edit_text(message, reply_markup=reply_markup, parse_mode="HTML")
    else:
        await update.message.reply_text(message, reply_markup=reply_markup, parse_mode="HTML")
    
    context.user_data["wallet_type"] = wallet_type
    context.user_data["action"] = action
    return State.CHOOSE_WALLET_TYPE


@catch_async
async def refresh_wallet_balances_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle refresh wallet balances callback"""
    query = update.callback_query
    await query.answer("🔄 Refreshing balances...")
    
    user_id = update.effective_user.id
    wallet_type = context.user_data.get("wallet_type")
    
    if not wallet_type:
        await query.message.edit_text(get_text(user_id, "no_wallet_type_selected", "listing"))
        return State.END
    
    try:
        # Get all wallets of the selected type
        existing_wallets = await WalletService.get_wallet_by_type(user_id, wallet_type)
        
        if not existing_wallets:
            await query.message.edit_text(get_text(user_id, "no_wallets_found", "listing"))
            return State.END
        
        # Refresh balances for all wallets
        refreshed_wallets = []
        for wallet in existing_wallets:
            balance, success = await refresh_wallet_balance(wallet.public_key, wallet_type)
            if success:
                refreshed_wallets.append((wallet, balance))
        
        # Rebuild keyboard with refreshed balances
        kb = []
        for wallet, balance in refreshed_wallets:
            kb.append([InlineKeyboardButton(
                f"{wallet.name} ({balance:.4f} {wallet_type})", 
                callback_data=f"wallet_{str(wallet.id)}"
            )])
        
        # Add refresh and create new wallet buttons
        kb.extend([
            [InlineKeyboardButton(
                "🔄 Refresh Balances", 
                callback_data="refresh_wallet_balances"
            )],
            [InlineKeyboardButton(
                get_text(user_id, "create_new_wallet"),
                callback_data="create_new_wallet"
            )]
        ])
        
        message = get_text(user_id, "balances_refreshed", "listing")
        reply_markup = InlineKeyboardMarkup(kb)
        
        await query.message.edit_text(message, reply_markup=reply_markup, parse_mode="HTML")
        return State.CHOOSE_WALLET_TYPE
        
    except Exception as e:
        logger.error(f"Error refreshing wallet balances: {e}")
        await query.message.edit_text(get_text(user_id, "error_refreshing_balances", "listing"))
        return State.END

async def process_wallet_selection(
    update: Update, 
    context: ContextTypes.DEFAULT_TYPE,
    wallet_id: str
) -> int:
    """Process selected wallet and proceed to next step"""
    user_id = update.effective_user.id
    wallet_type = context.user_data.get("wallet_type")
    
    wallet_details = await WalletService.get_wallet_by_id(wallet_id)
    if not wallet_details:
        await update.callback_query.message.edit_text(get_text(user_id, "wallet_not_found"), parse_mode="HTML")
        return State.END
    
    # Get balance
    total_balance = await get_wallet_balance(wallet_details["public_key"], wallet_type)
    
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
        await update.callback_query.message.reply_text(get_text(user_id, "create_case_title"))
        await update.callback_query.message.reply_text(get_text(user_id, "enter_name"))
        return State.CREATE_CASE_NAME
    
    return State.END

async def handle_extend_reward_flow(
    update: Update, 
    context: ContextTypes.DEFAULT_TYPE,
    case_id: str,
    action: str = "view"
) -> int:
    """Unified handler for extend reward flows"""
    user_id = update.effective_user.id
    try:
        case = await Case.find_one({"_id": PydanticObjectId(case_id)}, fetch_links=True)
        if not case:
            await update.callback_query.message.edit_text(get_text(user_id, "case_not_found"))
            return State.END
        
        # Fetch all pending extend rewards
        extend_rewards = await ExtendReward.find(
            {"case.$id": PydanticObjectId(case_id), "status": {"$ne": ExtendRewardStatus.COMPLETED}}
        ).to_list()
        
        if not extend_rewards:
            await update.callback_query.message.edit_text(get_text(user_id, "extend_reward_not_found"))
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
            last_seen_date=case.created_at.strftime("%d %B %Y") if case.created_at else "Unknown",
            height=case.height or "Unknown",
        )
        
        full_message = case_details + f"\n**Proof:** {proof_text}\n\n"
        full_message += get_text(user_id, "extend_reward_header", "listing") + "\n"
        
        keyboard = []
        for extend_reward in extend_rewards:
            full_message += f"👤 **Requested By:** `{extend_reward.user_id}`\n"
            full_message += f"   **Amount Requested:** {extend_reward.extend_reward_amount} {case.wallet.wallet_type}\n\n"
            
            if action == "approve":
                keyboard.append([
                    InlineKeyboardButton(
                        f"Approve Extend by {extend_reward.user_id}",
                        callback_data=f"approve_extend_{extend_reward.id}_{case_id}"
                    )
                ])
        
        # Add cancel button
        if action == "approve":
            keyboard.append([
                InlineKeyboardButton(
                    get_text(user_id, "cancel_button", "listing"),
                    callback_data="cancel_extend"
                )
            ])
        
        reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None
        
        await update.callback_query.message.edit_text(
            full_message.strip(),
            reply_markup=reply_markup,
            parse_mode="Markdown",
        )
        
        return State.CONFIRM_EXTEND if action == "approve" else State.CASE_DETAILS
        
    except Exception as e:
        logger.error(f"Error in extend_reward_flow: {str(e)}")
        await update.callback_query.message.edit_text(get_text(user_id, "error_processing_extend", "listing"))
        return State.END




@catch_async
async def enter_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ask the user to enter the country."""
    await update.message.reply_text("🌍 Please enter your country:")
    return State.ENTER_COUNTRY

@catch_async
async def process_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process and validate the country. Prompt for city if valid."""
    country = update.message.text.strip()
    country_matches = get_country_matches(country)
    
    if country_matches:
        context.user_data["country"] = country_matches[0]
        await update.message.reply_text(
            f"✅ You've entered **{country_matches[0]}**. Now, please enter your city:"
        )
        return State.ENTER_CITY
    else:
        await update.message.reply_text(
            "❌ Invalid country. Please enter a valid country from the list:\n"
            "- United States\n- Pakistan\n- Canada\n- United Kingdom"
        )
        return State.ENTER_COUNTRY

@catch_async
async def process_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Validate the city based on the previously entered country."""
    city = update.message.text.strip()
    country = context.user_data.get("country")
    cities = get_city_matches(country, city)
    
    if cities:
        case_id = context.user_data.get("editing_case_id")
        case = await Case.find_one({"_id": PydanticObjectId(case_id)})
        if case:
            setattr(case, "country", country)
            setattr(case, "city", cities[0])
            case.updated_at = datetime.utcnow()
            await case.save()
        
        await update.message.reply_text(
            f"✅ Great! You've successfully added:\n"
            f"🌍 Country: **{country}**\n"
            f"🏙️ City: **{cities[0]}**"
        )
        return State.END
    else:
        await update.message.reply_text(
            f"❌ The city **{city}** is not valid for **{country}**.\n"
            "Please enter a valid city:"
        )
        return State.ENTER_CITY


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
        context.user_data.pop("editing_case_id", None)
        context.user_data.pop("editing_field", None)
        
        await query.message.edit_text(get_text(user_id, "edit_canceled", "listing"))
        return State.END
        
    except Exception as e:
        logger.error(
            f"Error in cancel_edit_callback: {str(e)}\n{traceback.format_exc()}"
        )
        await query.message.edit_text(get_text(user_id, "error_canceling_edit", "listing"))
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
        case = await Case.find_one({"_id": ObjectId(case_id)})
        finder = await Finder.find_one(
            {"user_id": int(finder_id), "case.$id": PydanticObjectId(case.id)}
        )
        
        if not case or not finder:
            await query.message.edit_text(get_text(user_id, "case_or_finder_not_found", "listing"))
            return State.END
        
        context.user_data["reward_case_id"] = case.id
        context.user_data["reward_finder_id"] = finder.id
        
        await query.message.edit_text(
            get_text(user_id, "enter_reward_amount", "listing").format(max_amount=case.reward), 
            parse_mode="Markdown",
        )
        return State.REWARD_TRANSFER_PROCESS
        
    except Exception as e:
        logger.error(f"Error in ask_reward_amount: {str(e)}\n{traceback.format_exc()}")
        await query.message.edit_text(get_text(user_id, "error_asking_reward_amount", "listing")) 
        return State.END

@catch_async
async def process_reward_transfer(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Shows confirmation before processing reward transfer"""
    user_id = update.effective_user.id
    amount = update.message.text.strip()
    case_id = context.user_data.get("reward_case_id")
    finder_id = context.user_data.get("reward_finder_id")
    
    try:
        case = await Case.find_one({"_id": ObjectId(case_id)})
        if not case:
            await update.message.reply_text(get_text(user_id, "case_not_found", "listing"))
            return State.END
        
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
                amount=amount, finder_id=finder_id, case_no=case.case_no
            ),
            reply_markup=keyboard,
            parse_mode="Markdown",
        )
        return State.CONFIRM_REWARD
        
    except ValueError:
        await update.message.reply_text(
            get_text(user_id, "invalid_reward_amount", "listing").format(max_amount=case.reward)
        )
        return State.REWARD_TRANSFER_PROCESS

@catch_async
async def confirm_reward(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Executes the reward transfer after confirmation"""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    try:
        case_id = context.user_data.get("reward_case_id")
        finder_id = context.user_data.get("reward_finder_id")
        amount = context.user_data.get("reward_amount")
        
        case = await Case.find_one({"_id": ObjectId(case_id)})
        finder = await Finder.find_one({"_id": PydanticObjectId(finder_id)}, fetch_links=True)
        
        if not case or not finder:
            await query.message.edit_text(get_text(user_id, "case_or_finder_not_found", "listing"))
            return State.END
        
        finder_wallet = finder.wallet
        wallet_type = finder_wallet.wallet_type
        
        # Transfer to finder
        is_transfer_to_finder_successful = await send_wallet_transfer(
            SOL_WALLET_PRIVATE_KEY if wallet_type == "SOL" else TRON_WALLET_PRIVATE_KEY,
            finder_wallet.public_key,
            amount,
            wallet_type
        )
        
        # Transfer tax to collector (if applicable)
        tax_amount = float(case.reward - amount)
        is_tax_transfer_successful = True
        if tax_amount > 0:
            collect_public_key = SOL_COLLECT_PUBLIC_KEY if wallet_type == "SOL" else TRON_COLLECT_PUBLIC_KEY
            is_tax_transfer_successful = await send_wallet_transfer(
                SOL_WALLET_PRIVATE_KEY if wallet_type == "SOL" else TRON_WALLET_PRIVATE_KEY,
                collect_public_key,
                tax_amount,
                wallet_type
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
        
    except Exception as e:
        logger.error(f"Reward confirmation error: {str(e)}")
        await query.message.edit_text(
            "⚠️ <b>Error:</b> Something went wrong during the reward transfer.",
            parse_mode="HTML"
        )
        return State.END

@catch_async
async def cancel_reward(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels the reward process"""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    # Clear context data
    context.user_data.pop("reward_case_id", None)
    context.user_data.pop("reward_finder_id", None)
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
        extend_reward = await ExtendReward.find_one({"_id": PydanticObjectId(extend_reward_id)})
        
        if not case or not extend_reward:
            await query.message.edit_text(get_text(user_id, "case_or_extend_not_found", "listing"))
            return State.END
        
        wallet_type = case.wallet.wallet_type
        
        # Get all user wallets of the given type
        wallets = await Wallet.find(
            {"user_id": user_id, "wallet_type": wallet_type, "deleted": False}
        ).to_list()
        
        if not wallets:
            await query.message.edit_text(get_text(user_id, "no_wallet_found", "listing"))
            return State.END
        
        # Select the wallet with the highest balance
        wallet_balances = []
        for wallet in wallets:
            balance = await get_wallet_balance(wallet.public_key, wallet_type)
            wallet_balances.append((wallet, balance))
        
        wallet_balances.sort(key=lambda x: x[1], reverse=True)
        best_wallet, best_balance = wallet_balances[0]
        
        # Revalidate the wallet balance
        if best_balance < extend_reward.extend_reward_amount:
            await query.message.edit_text(get_text(user_id, "insufficient_funds_after_selection", "listing"))
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
        confirmation_message = get_text(user_id, "select_wallet_for_extend", "listing").format(
            amount=escape_markdown(str(extend_reward.extend_reward_amount), version=2),
            wallet_type=escape_markdown(wallet_type, version=2),
            from_wallet=escape_markdown(best_wallet.public_key, version=2),
            to_wallet=escape_markdown(SOL_WALLET_PUBLIC_KEY, version=2),
        )
        
        await query.message.edit_text(
            confirmation_message.strip(),
            reply_markup=keyboard,
            parse_mode="MarkdownV2",
        )
        return State.SELECT_WALLET_FOR_EXTEND
        
    except Exception as e:
        logger.error(f"Error in approve_extend_callback: {str(e)}")
        await query.message.edit_text(get_text(user_id, "error_approving_extend", "listing"))
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
    extend_reward = await ExtendReward.find_one({"_id": PydanticObjectId(extend_reward_id)})
    wallet = await Wallet.find_one({"_id": PydanticObjectId(wallet_id)})
    
    if not case or not extend_reward or not wallet:
        await query.message.edit_text(get_text(user_id, "case_or_extend_not_found", "listing"))
        return State.END
    
    wallet_type = case.wallet.wallet_type
    
    # Revalidate the wallet balance
    balance = await get_wallet_balance(wallet.public_key, wallet_type)
    if balance < extend_reward.extend_reward_amount:
        await query.message.edit_text(get_text(user_id, "insufficient_funds_after_selection", "listing"))
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
                    callback_data="cancel_extend"
                )
            ],
        ]
    )
    
    confirmation_message = get_text(user_id, "extend_reward_confirmation", "listing").format(
        amount=extend_reward.extend_reward_amount,
        wallet_type=wallet_type,
        from_wallet=wallet.public_key,
        to_wallet=SOL_WALLET_PUBLIC_KEY,
    )
    
    await query.message.edit_text(
        confirmation_message.strip(),
        reply_markup=keyboard,
        parse_mode="Markdown",
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
    extend_reward = await ExtendReward.find_one({"_id": PydanticObjectId(extend_reward_id)})
    
    if not case or not extend_reward:
        await query.message.edit_text(get_text(user_id, "case_or_extend_not_found", "listing"))
        return State.END
    
    # Retrieve the selected wallet from context.user_data
    selected_wallet = context.user_data.get("selected_wallet")
    if not selected_wallet:
        await query.message.edit_text(get_text(user_id, "no_wallet_selected", "listing"))
        return State.END
    
    wallet_type = case.wallet.wallet_type
    amount = extend_reward.extend_reward_amount
    
    # Recheck the wallet balance
    current_balance = await get_wallet_balance(selected_wallet.public_key, wallet_type)
    if current_balance < amount:
        await query.message.edit_text(get_text(user_id, "insufficient_funds_after_selection", "listing"))
        return State.END
    
    try:
        # Perform transfer
        if wallet_type == "SOL":
            success = await WalletService.send_sol(
                selected_wallet.private_key, 
                SOL_WALLET_PUBLIC_KEY, 
                amount
            )
        else:  # USDT
            success = await WalletService.send_usdt(
                selected_wallet.private_key, 
                TRON_COLLECT_PUBLIC_KEY,  # Fixed: was SOL_WALLET_PUBLIC_KEY which is incorrect
                amount
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
    
    return await handle_wallet_selection(update, context, user_id, wallet_type, "create_case")

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
        await update.message.reply_text(get_text(user_id, "wallet_name_empty"), parse_mode="HTML")
        return State.NAME_WALLET
    
    wallet_type = context.user_data.get("wallet_type")
    
    wallet = await WalletService.create_wallet(user_id, wallet_type, wallet_name)
    if wallet:
        total_balance = await get_wallet_balance(wallet.public_key, wallet_type)
        
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
        await update.message.reply_text(get_text(user_id, "wallet_create_err"), parse_mode="HTML")
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
                        get_text(user_id, "usdt_wallet"), 
                        callback_data="USDT"
                    ),
                    InlineKeyboardButton(
                        get_text(user_id, "sol_wallet"), 
                        callback_data="SOL"
                    ),
                ]
            ]
        )
        await query.edit_message_text(
            get_text(user_id, "choose_wallet"), 
            reply_markup=kb
        )
        return State.CHOOSE_WALLET_TYPE
    
    elif choice == "find_people":
        # Clearing the province
        await query.edit_message_text("Choose Province")
        return State.CHOOSE_PROVINCE
    
    else:
        await query.edit_message_text(
            get_text(user_id, "invalid_choice"), 
            parse_mode="HTML"
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
            get_text(user_id, "country_multi", "start-complaints").format(page=1, total=total), ## TODO: Getting it from the start command
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
            get_text(user_id, "country_multi", "start-complaints").format(page=page_num, total=total), ## TODO: Getting it from the start command
            reply_markup=markup,
            parse_mode="HTML",
        )

        context.user_data["country_page"] = page_num
        return State.CHOOSE_COUNTRY
    else:
        await query.edit_message_text(
            get_text(user_id, "invalid_choice", "start-complaints"), parse_mode="HTML" ## TODO: Getting it from the start command
        )
        return State.END


@catch_async
async def choose_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    city_input = update.message.text.strip()
    country = context.user_data.get("country")
    if not country:
        await update.message.reply_text(
            get_text(user_id, "invalid_choice", "start-complaints"), parse_mode="HTML" ## TODO: Getting it from the start command
        )
        return State.END
    matches = get_city_matches(country, city_input)
    if not matches:
        await update.message.reply_text(
            get_text(user_id, "city_not_found", "start-complaints"), parse_mode="HTML" ## TODO: Getting it from the start command
        )
        return State.CHOOSE_CITY
    if len(matches) == 1:
        context.user_data["city"] = matches[0]
        await update.message.reply_text(
            f"{get_text(user_id, 'city_selected', "start-complaints")} {matches[0]}", ## TODO: Getting it from the start command
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
            get_text(user_id, "city_multi", "start-complaints").format(page=1, total=total), ## TODO: Getting it from the start command
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
            f"{get_text(user_id, 'city_selected')} {city}", parse_mode="HTML" ## TODO: Getting it from the start command
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
            get_text(user_id, "city_multi", "start-complaints").format(page=page_num, total=total), ## TODO: Getting it from the start command
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
