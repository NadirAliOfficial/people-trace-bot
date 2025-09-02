from handlers.start_handler import cancel
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, error
from constant.language_constant import get_text
from constants import State
from services.tron_wallet_service import TronWallet
from services.wallet_service import WalletService
from utils.get_network import get_network
from utils.error_wrapper import catch_async
from telegram.ext import ContextTypes
import re


def escape_markdown_v2(text: str) -> str:
    """Escapes special characters for Telegram MarkdownV2"""
    escape_chars = r"_*[]()~>#+-=|{}.!"
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)


def back_to_wallet_menu_keyboard(user_id: int) -> list:
    kb = [
        [
            InlineKeyboardButton(
                get_text(user_id, "refresh_btn", "wallets"),
                callback_data="refresh_wallets",
            )
        ],
        [
            InlineKeyboardButton(
                get_text(user_id, "sol_btn", "globals"), callback_data="sol_wallets"
            ),
            InlineKeyboardButton(
                get_text(user_id, "usdt_btn", "globals"), callback_data="usdt_wallets"
            ),
        ],
        [
            InlineKeyboardButton(
                get_text(user_id, "address_btn", "wallets"),
                callback_data="show_address",
            )
        ],
        [
            InlineKeyboardButton(
                get_text(user_id, "create_wallet_btn", "wallets"),
                callback_data="create_wallet",
            ),
            InlineKeyboardButton(
                get_text(user_id, "delete_wallet_btn", "wallets"),
                callback_data="delete_wallet",
            ),
        ],
    ]
    return kb


# ====================== Wallet Implementation ======================
@catch_async
async def wallet_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Entry point for /wallet command."""
    user_id = update.effective_user.id

    await cancel(update, context)

    wallets = await WalletService.get_wallet_by_user(user_id, False)
    if wallets is None:
        wallets = []

    kb = back_to_wallet_menu_keyboard(user_id)

    if update.message:
        await update.message.reply_text(
            get_text(user_id, "welcome_text", "wallets"),
            reply_markup=InlineKeyboardMarkup(kb),
        )
    elif update.callback_query:
        await update.callback_query.message.reply_text(
            get_text(user_id, "welcome_text", "wallets"),
            reply_markup=InlineKeyboardMarkup(kb),
        )

    return State.WALLETS.WALLET_MENU


@catch_async
async def refresh_wallets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Refresh the wallet list."""
    user_id = update.effective_user.id
    wallets = await WalletService.get_wallet_by_user(user_id, False)
    if wallets is None:
        wallets = []

    # Rebuild the keyboard with updated wallet information
    kb = back_to_wallet_menu_keyboard(user_id)

    new_text = get_text(user_id, "refresh_wallet_text", "wallets")

    try:
        if update.callback_query.message.text != new_text:
            await update.callback_query.message.edit_text(
                new_text, reply_markup=InlineKeyboardMarkup(kb)
            )
        else:
            await update.callback_query.answer(
                get_text(user_id, "wallets_already_updated", "wallets"), show_alert=True
            )
    except error.BadRequest:
        await update.callback_query.answer(
            get_text(user_id, "wallets_already_updated", "wallets"), show_alert=True
        )

    return State.WALLETS.WALLET_MENU


# ====================== SOL Wallets Implementation ======================


@catch_async
async def sol_wallets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display SOL wallets as interactive buttons with balances"""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    wallets = await WalletService.get_wallet_by_user(user_id, False)
    sol_wallets = [w for w in wallets if w.wallet_type.upper() == "SOL"]

    if not sol_wallets:
        message = get_text(user_id, "no_sol_wallets", "wallets")
        await query.edit_message_text(message)
        return State.WALLETS.WALLET_MENU

    # Create buttons with balances for each SOL wallet
    kb = []
    for wallet in sol_wallets:
        try:
            balance = await WalletService.get_sol_balance(wallet.public_key)
            btn_text = f"{wallet.name} - {balance} SOL"
        except Exception:
            btn_text = f"{wallet.name} - Error fetching balance"

        kb.append(
            [InlineKeyboardButton(btn_text, callback_data=f"sol_detail_{wallet.id}")]
        )

    # Add navigation buttons
    kb.append(
        [
            InlineKeyboardButton(
                get_text(user_id, "refresh_btn", "wallets"), callback_data="sol_wallets"
            ),
            InlineKeyboardButton(
                get_text(user_id, "back_to_wallet", "globals"),
                callback_data="back_to_wallet_menu",
            ),
        ]
    )

    await query.edit_message_text(
        get_text(user_id, "your_sol_wallet", "wallets"), 
        reply_markup=InlineKeyboardMarkup(kb)
    )
    return State.WALLETS.SOL_WALLET_DETAIL


@catch_async
async def show_sol_wallet_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show detailed view of a SOL wallet with private key option"""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    wallet_id = query.data.split("_")[-1]

    wallet = await WalletService.get_wallet_by_id(wallet_id)
    if not wallet:
        await query.message.edit_text(get_text(user_id, "wallet_not_found", "wallets"))
        return State.WALLETS.WALLET_MENU

    # Get balance
    try:
        balance = await WalletService.get_sol_balance(wallet["public_key"])
        balance_text = f"{balance} SOL"
    except Exception as e:
        balance_text = f"Error: {str(e)}"

    # Format and escape message
    message = escape_markdown_v2(
        get_text(user_id, "show_balance", "wallets").format(
            name=wallet["name"], balance=balance_text, public_key=wallet["public_key"]
        )
    )

    # Create action buttons
    kb = [
        [
            InlineKeyboardButton(
                get_text(user_id, "show_private_key", "wallets"),
                callback_data=f"req_pk_{wallet['id']}",
            )
        ],
        [
            InlineKeyboardButton(
                get_text(user_id, "back_to_wallet", "globals"),
                callback_data="sol_wallets",
            )
        ],
    ]

    await query.message.edit_text(
        message, parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(kb)
    )
    return State.WALLETS.SOL_WALLET_ACTIONS


# ====================== USDT Wallets Implementation ======================
@catch_async
async def usdt_wallets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display USDT wallets as interactive buttons with balances"""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    wallets = await WalletService.get_wallet_by_user(user_id, False)
    usdt_wallets = [w for w in wallets if w.wallet_type.upper() == "USDT"]

    if not usdt_wallets:
        message = get_text(user_id, "no_usdt_wallets", "wallets")
        await query.edit_message_text(message)
        return State.WALLETS.WALLET_MENU

    # Create buttons with balances for each USDT wallet
    kb = []
    for wallet in usdt_wallets:
        try:
            balance = await TronWallet.get_usdt_balance(wallet.public_key)
            btn_text = f"{wallet.name} - {balance} USDT"
        except Exception:
            btn_text = f"{wallet.name} - Error fetching balance"

        kb.append(
            [InlineKeyboardButton(btn_text, callback_data=f"usdt_detail_{wallet.id}")]
        )

    # Add navigation buttons
    kb.append(
        [
            InlineKeyboardButton(
                get_text(user_id, "refresh_btn", "wallets"),
                callback_data="usdt_wallets",
            ),
            InlineKeyboardButton(
                get_text(user_id, "back_to_wallet", "globals"),
                callback_data="back_to_wallet_menu",
            ),
        ]
    )

    await query.edit_message_text(
        get_text(user_id, "your_usdt_wallet", "wallets"),
        reply_markup=InlineKeyboardMarkup(kb),
    )
    return State.WALLETS.USDT_WALLET_DETAIL


@catch_async
async def show_usdt_wallet_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show detailed view of a USDT wallet with private key option"""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    wallet_id = query.data.split("_")[-1]

    wallet = await WalletService.get_wallet_by_id(wallet_id)
    if not wallet:
        await query.message.edit_text(get_text(user_id, "wallet_not_found", "wallets"))
        return State.WALLETS.WALLET_MENU

    # Get balance
    try:
        balance = await TronWallet.get_usdt_balance(wallet["public_key"])
        balance_text = f"{balance} USDT"
    except Exception as e:
        balance_text = f"Error: {str(e)}"

    # Format and escape message
    message = escape_markdown_v2(
        get_text(user_id, "show_balance", "wallets").format(
            name=wallet["name"], balance=balance_text, public_key=wallet["public_key"]
        )
    )

    # Create action buttons
    kb = [
        [
            InlineKeyboardButton(
                get_text(user_id, "show_private_key", "wallets"),
                callback_data=f"req_pk_{wallet['id']}",
            )
        ],
        [
            InlineKeyboardButton(
                get_text(user_id, "back_to_wallet", "globals"),
                callback_data="back_to_wallet_menu",
            )
        ],
    ]

    await query.message.edit_text(
        message, parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(kb)
    )
    return State.WALLETS.USDT_WALLET_ACTIONS


@catch_async
async def request_private_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show confirmation before revealing private key"""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    wallet_id = query.data.split("_")[-1]

    # Store wallet ID in context
    context.user_data["pk_wallet_id"] = wallet_id

    kb = [
        [
            InlineKeyboardButton(
                get_text(user_id, "show_it_btn", "wallets"), callback_data="confirm_pk"
            )
        ],
        [
            InlineKeyboardButton(
                get_text(user_id, "back_to_wallet", "globals"),
                callback_data="back_to_wallet_menu",
            )
        ],
    ]

    warning_text = escape_markdown_v2(
        get_text(user_id, "wallet_security_warning", "wallets")
    )

    await query.message.edit_text(
        warning_text, parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(kb)
    )
    return State.WALLETS.CONFIRM_PRIVATE_KEY


@catch_async
async def show_private_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display the private key after confirmation"""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "cancel_pk":
        await query.message.delete()
        return await wallet_command(update, context)

    wallet_id = context.user_data.get("pk_wallet_id")
    wallet = await WalletService.get_wallet_by_id(wallet_id)

    if not wallet:
        await query.message.edit_text(get_text(user_id, "wallet_not_found", "wallets"))
        return State.WALLETS.WALLET_MENU

    # Format and escape the private key message
    warning_message = escape_markdown_v2(
        get_text(user_id, "private_key_warning", "wallets").format(
            wallet=wallet["private_key"]
        )
    )

    # Create back button
    kb = [
        [
            InlineKeyboardButton(
                get_text(user_id, "back_to_wallet", "globals"),
                callback_data="back_to_wallet_menu",
            )
        ]
    ]

    await query.message.edit_text(
        warning_message, parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(kb)
    )
    return State.WALLETS.WALLET_MENU


@catch_async
async def show_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show the public address of a wallet."""
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    wallets = await WalletService.get_wallet_by_user(user_id)

    if not wallets:
        message = get_text(user_id, "dont_have_any_wallet", "wallets")
        kb = []
    else:
        kb = [
            [
                InlineKeyboardButton(
                    wallet.name, callback_data=f"show_address_{wallet.id}"
                )
            ]
            for wallet in wallets
        ]
        message = get_text(user_id, "select_wallet_header", "wallets")

    await update.callback_query.message.edit_text(
        message, reply_markup=InlineKeyboardMarkup(kb), parse_mode="HTML"
    )
    return State.WALLETS.SHOW_ADDRESS


@catch_async
async def show_specific_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show the specific wallet address."""
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id

    # Get the user's language preference (default to 'en' if not set)
    user_language = context.user_data.get("language", "en")

    # Extract wallet ID from callback data
    wallet_id = query.data.split("_")[-1]
    wallet = await WalletService.get_wallet_by_id(wallet_id)

    if wallet:
        # Format the wallet details using the language-specific template
        message = get_text(user_id, "wallet_details", "wallets").format(
            name=wallet["name"], public_key=wallet["public_key"]
        )

        # Add a back button for navigation
        kb = [
            [
                InlineKeyboardButton(
                    get_text(user_id, "back_to_wallet", "globals"),
                    callback_data="back_to_wallet_menu",
                )
            ]
        ]
    else:
        message = get_text(user_id, "wallet_not_found", "wallets")
        kb = []  # No keyboard if wallet is not found

    # Edit the message with the formatted text and keyboard
    await update.callback_query.message.edit_text(
        message, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb)
    )
    return State.WALLETS.WALLET_MENU


@catch_async
async def view_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View transaction history."""
    query = update.callback_query
    await query.answer()

    # Get the user's language preference (default to 'en' if not set)
    user_language = context.user_data.get("language", "en")

    user_id = update.effective_user.id
    wallets = await WalletService.get_wallet_by_user(user_id, False)

    if not wallets or wallets == []:
        message = get_text(user_id, "no_wallets", "wallets")
        kb = []  # Define an empty keyboard if there are no wallets
    else:
        kb = [
            [
                InlineKeyboardButton(
                    wallet.name, callback_data=f"view_history_{wallet.id}"
                )
            ]
            for wallet in wallets
        ]
        message = get_text(
            user_id, "select_wallet", "wallets"
        )  # Use the translated message

    # Ensure `kb` is always defined before using it
    await update.callback_query.message.edit_text(
        message, reply_markup=InlineKeyboardMarkup(kb)
    )
    return State.WALLETS.VIEW_HISTORY


@catch_async
async def view_specific_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View the specific wallet's transaction history."""
    query = update.callback_query
    wallet_id = query.data.split("_")[-1]
    wallet = await WalletService.get_wallet_by_id(wallet_id)
    user_id = update.effective_user.id

    if wallet:
        history = (
            await WalletService.get_usdt_history(wallet["public_key"])
            if wallet["wallet_type"] == "USDT"
            else await WalletService.get_sol_history(wallet["public_key"])
        )
        message = f"Transaction History for {wallet["name"]}:\n"
        for tx in history:
            message += f"Signature: {tx['signature']}, Time: {tx['block_time']}\n"
    else:
        message = get_text(user_id, "wallet_not_found", "wallets")

    await update.callback_query.message.edit_text(message)
    return State.WALLETS.WALLET_MENU


@catch_async
async def create_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ask the user to select the wallet type."""
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id

    # Create buttons for wallet type selection
    keyboard = [
        [
            InlineKeyboardButton(
                get_text(user_id, "usdt_btn", "globals"), callback_data="USDT"
            ),
            InlineKeyboardButton(
                get_text(user_id, "sol_btn", "globals"), callback_data="SOL"
            ),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    message = get_text(user_id, "select_wallet_type_header", "wallets")
    await query.edit_message_text(text=message, reply_markup=reply_markup)
    return State.WALLETS.SELECT_WALLET_TYPE


@catch_async
async def select_wallet_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store the selected wallet type and ask for the wallet name."""
    query = update.callback_query
    user_id = update.effective_user.id
    await query.answer()

    # Store the selected wallet type in context
    context.user_data["wallet_type"] = query.data

    message = get_text(user_id, "enter_wallet_name", "wallets")
    await query.edit_message_text(text=message)
    return State.WALLETS.ENTER_WALLET_NAME


@catch_async
async def process_create_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process the wallet creation with the provided name and type."""
    wallet_name = update.message.text.strip()
    wallet_type = context.user_data.get("wallet_type")
    user_id = update.effective_user.id

    # Check if the wallet name is already used
    if await WalletService.check_wallet_name_used(user_id, wallet_name):
        message = get_text(user_id, "wallet_address_already_in_use", "wallets")
        await update.message.reply_text(message)
        return State.WALLETS.ENTER_WALLET_NAME

    # Create the wallet
    wallet = await WalletService.create_wallet(user_id, wallet_type, wallet_name)

    message = get_text(user_id, "wallet_create_details", "wallets").format(
        name=wallet.name,
        wallet_type=wallet.wallet_type,
        public_key=wallet.public_key,
        network=get_network(wallet.wallet_type),
    )

    await update.message.reply_text(
        message,
        parse_mode="HTML",
    )
    return State.WALLETS.WALLET_MENU


@catch_async
async def delete_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Delete a wallet."""
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    wallets = await WalletService.get_wallet_by_user(user_id, False)

    if not wallets:
        message = get_text(user_id, "dont_have_wallet_to_delete", "wallets")
        await query.message.edit_text(message)
        return State.WALLETS.WALLET_MENU

    kb = [
        [
            InlineKeyboardButton(
                wallet.name, callback_data=f"confirm_delete_wallet_{wallet.id}"
            )
        ]
        for wallet in wallets
    ]

    message = get_text(user_id, "select_wallet_to_delete", "wallets")
    await query.message.edit_text(message, reply_markup=InlineKeyboardMarkup(kb))
    return State.WALLETS.CONFIRM_DELETE_WALLET


@catch_async
async def confirm_delete_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ask for confirmation before deleting the wallet."""
    query = update.callback_query
    wallet_id = query.data.split("_")[-1]
    user_id = update.effective_user.id

    # Get wallet details to show confirmation
    wallet = await WalletService.get_wallet_by_id(wallet_id)
    wallet_name = wallet["name"] if wallet else "Unknown"

    kb = [
        [
            InlineKeyboardButton(
                get_text(user_id, "yes_delete", "wallets"),
                callback_data=f"delete_wallet_{wallet_id}",
            ),
            InlineKeyboardButton(
                get_text(user_id, "cancel_btn", "globals"), 
                callback_data="cancel_delete_wallet"
            ),
        ]
    ]

    message = get_text(user_id, "confirm_delete_message", "wallets").format(
        wallet_name=wallet_name
    )
    await query.message.edit_text(message, reply_markup=InlineKeyboardMarkup(kb))
    return State.WALLETS.DELETE_WALLET


@catch_async
async def cancel_delete_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel wallet deletion and return to menu."""
    query = update.callback_query
    user_id = update.effective_user.id
    message = get_text(user_id, "delete_wallet_confirm_reject", "wallets")
    await query.message.edit_text(message)
    return await wallet_command(update, context)


@catch_async
async def process_delete_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process the deletion of a wallet."""
    query = update.callback_query

    print("Getting the query data", query.data)

    wallet_id = query.data.split("_")[2]

    if not wallet_id:
        user_id = update.effective_user.id
        message = get_text(user_id, "delete_wallet_confirm_reject", "wallets")
        await query.message.edit_text(message)
        return State.WALLETS.END
    
    user_id = update.effective_user.id

    success = await WalletService.soft_delete_wallet(wallet_id)
    message = (
        get_text(user_id, "wallet_deleted", "wallets")
        if success
        else get_text(user_id, "failed_to_delete_wallet", "wallets")
    )

    await query.message.edit_text(message)
    return State.WALLETS.WALLET_MENU


#  ----------------------- Back to the Wallet Menu ------------------------
@catch_async
async def back_to_wallet_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles going back to the wallet menu."""
    query = update.callback_query
    if query:
        await query.answer()

    user_id = update.effective_user.id
    welcome_text = get_text(user_id, "welcome_text", "wallets")
    keyboard = InlineKeyboardMarkup(back_to_wallet_menu_keyboard(user_id))

    # Determine whether to edit the existing message or send a new one
    if update.callback_query:
        # Update the existing message (callback query)
        await query.edit_message_text(text=welcome_text, reply_markup=keyboard)
    elif update.message:
        # Send a new message (regular message)
        await update.message.reply_text(text=welcome_text, reply_markup=keyboard)
    return State.WALLETS.WALLET_MENU