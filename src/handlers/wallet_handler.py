from handlers.start_handler import cancel
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, error
from constant.language_constant import get_text
from constants import State
from services.tron_wallet_service import TronWallet
from services.wallet_service import WalletService
from utils.error_wrapper import catch_async
from telegram.ext import ContextTypes
import re

def escape_markdown_v2(text: str) -> str:
    """Escapes special characters for Telegram MarkdownV2"""
    escape_chars = r"_*[]()~>#+-=|{}.!"
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)



# ====================== Wallet Implementation ======================
@catch_async
async def wallet_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Entry point for /wallet command."""
    user_id = update.effective_user.id

    await cancel(update, context)

    
    wallets = await WalletService.get_wallet_by_user(user_id, False)
    if wallets is None:
        wallets = []

    kb = [
        [
            InlineKeyboardButton(
                get_text(user_id, "refresh_btn"), callback_data="refresh_wallets"
            )
        ],
        [
            InlineKeyboardButton(
                get_text(user_id, "sol_btn"), callback_data="sol_wallets"
            ),
            InlineKeyboardButton(
                get_text(user_id, "usdt_btn"), callback_data="usdt_wallets"
            ),
        ],
        [
            InlineKeyboardButton(
                get_text(user_id, "address_btn"), callback_data="show_address"
            )
        ],
        [
            InlineKeyboardButton(
                get_text(user_id, "history_btn"), callback_data="view_history"
            )
        ],
        [
            InlineKeyboardButton(
                get_text(user_id, "create_wallet_btn"), callback_data="create_wallet"
            ),
            InlineKeyboardButton(
                get_text(user_id, "delete_wallet_btn"), callback_data="delete_wallet"
            ),
        ],
    ]

    if update.message:
        await update.message.reply_text(
            get_text(user_id, "welcome_text"), reply_markup=InlineKeyboardMarkup(kb)
        )
    elif update.callback_query:
        await update.callback_query.message.reply_text(
            get_text(user_id, "welcome_text"), reply_markup=InlineKeyboardMarkup(kb)
        )

    return State.WALLET_MENU


@catch_async
async def refresh_wallets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Refresh the wallet list."""
    user_id = update.effective_user.id
    wallets = await WalletService.get_wallet_by_user(user_id, False)
    if wallets is None:
        wallets = []

    # Rebuild the keyboard with updated wallet information
    kb = [
        [
            InlineKeyboardButton(
                get_text(user_id, "refresh_btn"), callback_data="refresh_wallets"
            )
        ],
        [
            InlineKeyboardButton(
                get_text(user_id, "sol_btn"), callback_data="sol_wallets"
            ),
            InlineKeyboardButton(
                get_text(user_id, "usdt_btn"), callback_data="usdt_wallets"
            ),
        ],
        [
            InlineKeyboardButton(
                get_text(user_id, "address_btn"), callback_data="show_address"
            )
        ],
        [
            InlineKeyboardButton(
                get_text(user_id, "history_btn"), callback_data="view_history"
            )
        ],
        [
            InlineKeyboardButton(
                get_text(user_id, "create_wallet_btn"), callback_data="create_wallet"
            ),
            InlineKeyboardButton(
                get_text(user_id, "delete_wallet_btn"), callback_data="delete_wallet"
            ),
        ],
    ]

    new_text = get_text(user_id, "refresh_wallet_text")

    try:
        if update.callback_query.message.text != new_text:
            await update.callback_query.message.edit_text(
                new_text, reply_markup=InlineKeyboardMarkup(kb)
            )
        else:
            await update.callback_query.answer(
                get_text(user_id, "wallets_already_updated"), show_alert=True
            )
    except error.BadRequest:
        await update.callback_query.answer(
            get_text(user_id, "wallets_already_updated"), show_alert=True
        )

    return State.WALLET_MENU

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
        message = get_text(user_id, "no_sol_wallets")
        await query.edit_message_text(message)
        return State.WALLET_MENU

    # Create buttons with balances for each SOL wallet
    kb = []
    for wallet in sol_wallets:
        try:
            balance = await WalletService.get_sol_balance(wallet.public_key)
            btn_text = f"{wallet.name} - {balance} SOL"
        except Exception:
            btn_text = f"{wallet.name} - Error fetching balance"
        
        kb.append([InlineKeyboardButton(btn_text, callback_data=f"sol_detail_{wallet.id}")])

    # Add navigation buttons
    kb.append([
        InlineKeyboardButton(get_text(user_id, "refresh_btn"), callback_data="sol_wallets"),
        InlineKeyboardButton(get_text(user_id, "back_button"), callback_data="back_to_wallet_menu")
    ])

    await query.edit_message_text(
        "📋 Your SOL Wallets:",
        reply_markup=InlineKeyboardMarkup(kb)
    )
    return State.SOL_WALLET_DETAIL

@catch_async
async def show_sol_wallet_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show detailed view of a SOL wallet with private key option"""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    wallet_id = query.data.split('_')[-1]

    wallet = await WalletService.get_wallet_by_id(wallet_id)
    if not wallet:
        await query.message.edit_text(get_text(user_id, "wallet_not_found"))
        return State.WALLET_MENU

    # Get balance
    try:
        balance = await WalletService.get_sol_balance(wallet['public_key'])
        balance_text = f"{balance} SOL"
    except Exception as e:
        balance_text = f"Error: {str(e)}"

    # Format and escape message
    message = escape_markdown_v2(
        f"🔷 {wallet['name']}\n\n"
        f"💰 Balance: {balance_text}\n"
        f"🔑 Public Key: {wallet['public_key']}\n\n"
        "Select an action:"
    )

    # Create action buttons
    kb = [
        [InlineKeyboardButton("🔐 Show Private Key", callback_data=f"req_pk_{wallet['id']}")],
        [InlineKeyboardButton("⬅️ Back to Wallets", callback_data="sol_wallets")]
    ]

    await query.message.edit_text(
        message,
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(kb)
    )
    return State.SOL_WALLET_ACTIONS



# ====================== USDT Wallets Implementation ======================
@catch_async
async def usdt_wallets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display USDT wallets as interactive buttons with balances"""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    wallets = await WalletService.get_wallet_by_user(user_id, False)
    usdt_wallets = [w for w in wallets if w['wallet_type'].upper() == "USDT"]

    if not usdt_wallets:
        message = get_text(user_id, "no_usdt_wallets")
        await query.edit_message_text(message)
        return State.WALLET_MENU

    # Create buttons with balances for each USDT wallet
    kb = []
    for wallet in usdt_wallets:
        try:
            balance = await TronWallet.get_usdt_balance(wallet['public_key'])
            btn_text = f"{wallet['name']} - {balance} USDT"
        except Exception:
            btn_text = f"{wallet['name']} - Error fetching balance"
        
        kb.append([InlineKeyboardButton(btn_text, callback_data=f"usdt_detail_{wallet['id']}")])

    # Add navigation buttons
    kb.append([
        InlineKeyboardButton(get_text(user_id, "refresh_btn"), callback_data="usdt_wallets"),
        InlineKeyboardButton(get_text(user_id, "back_button"), callback_data="back_to_wallet_menu")
    ])

    await query.edit_message_text(
        "📋 Your USDT Wallets:",
        reply_markup=InlineKeyboardMarkup(kb)
    )
    return State.USDT_WALLET_DETAIL



@catch_async
async def usdt_wallets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display USDT wallets as interactive buttons with balances"""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    wallets = await WalletService.get_wallet_by_user(user_id, False)
    usdt_wallets = [w for w in wallets if w.wallet_type.upper() == "USDT"]

    if not usdt_wallets:
        message = get_text(user_id, "no_usdt_wallets")
        await query.edit_message_text(message)
        return State.WALLET_MENU

    # Create buttons with balances for each USDT wallet
    kb = []
    for wallet in usdt_wallets:
        try:
            balance = await TronWallet.get_usdt_balance(wallet.public_key)
            btn_text = f"{wallet.name} - {balance} USDT"
        except Exception:
            btn_text = f"{wallet.name} - Error fetching balance"
        
        kb.append([InlineKeyboardButton(btn_text, callback_data=f"usdt_detail_{wallet.id}")])

    # Add navigation buttons
    kb.append([
        InlineKeyboardButton(get_text(user_id, "refresh_btn"), callback_data="usdt_wallets"),
        InlineKeyboardButton(get_text(user_id, "back_button"), callback_data="back_to_wallet_menu")
    ])

    await query.edit_message_text(
        "📋 Your USDT Wallets:",
        reply_markup=InlineKeyboardMarkup(kb)
    )
    return State.USDT_WALLET_DETAIL

@catch_async
async def show_usdt_wallet_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show detailed view of a USDT wallet with private key option"""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    wallet_id = query.data.split('_')[-1]

    wallet = await WalletService.get_wallet_by_id(wallet_id)
    if not wallet:
        await query.message.edit_text(get_text(user_id, "wallet_not_found"))
        return State.WALLET_MENU

    # Get balance
    try:
        balance = await TronWallet.get_usdt_balance(wallet['public_key'])
        balance_text = f"{balance} USDT"
    except Exception as e:
        balance_text = f"Error: {str(e)}"

    # Format and escape message
    message = escape_markdown_v2(
        f"🔷 {wallet['name']}\n\n"
        f"💰 Balance: {balance_text}\n"
        f"🔑 Public Key: {wallet['public_key']}\n\n"
        "Select an action:"
    )

    # Create action buttons
    kb = [
        [InlineKeyboardButton("🔐 Show Private Key", callback_data=f"req_pk_{wallet['id']}")],
        [InlineKeyboardButton("⬅️ Back to Wallets", callback_data="usdt_wallets")]
    ]

    await query.message.edit_text(
        message,
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(kb)
    )
    return State.USDT_WALLET_ACTIONS

@catch_async
async def request_private_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show confirmation before revealing private key"""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    wallet_id = query.data.split('_')[-1]

    # Store wallet ID in context
    context.user_data["pk_wallet_id"] = wallet_id

    kb = [
        [InlineKeyboardButton("✅ Yes, show it", callback_data="confirm_pk")],
        [InlineKeyboardButton("❌ Cancel", callback_data="cancel_pk")]
    ]

    warning_text = escape_markdown_v2(
        "⚠️ Security Warning\n\n"
        "Private keys give full access to your wallet. "
        "Never share them with anyone!\n\n"
        "Are you sure you want to view the private key?"
    )

    await query.message.edit_text(
        warning_text,
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(kb)
    )
    return State.CONFIRM_PRIVATE_KEY

@catch_async
async def show_private_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display the private key after confirmation"""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "cancel_pk":
        await query.message.delete()
        return await usdt_wallets(update, context)

    wallet_id = context.user_data.get("pk_wallet_id")
    wallet = await WalletService.get_wallet_by_id(wallet_id)
    
    if not wallet:
        await query.message.edit_text(get_text(user_id, "wallet_not_found"))
        return State.WALLET_MENU

    # Format and escape the private key message
    warning_message = escape_markdown_v2(
        "🚨 PRIVATE KEY WARNING 🚨\n\n"
        "This key gives FULL ACCESS to your wallet and funds.\n\n"
        "🔐 Private Key:\n"
        f"{wallet['private_key']}\n\n"
        "❗ Never share this key with anyone\n"
        "❗ Never enter it on unverified websites\n"
        "❗ Store it securely offline if you must keep it"
    )

    # Create back button
    kb = [[InlineKeyboardButton("⬅️ Back to Wallet", callback_data=f"usdt_detail_{wallet['id']}")]]

    await query.message.edit_text(
        warning_message,
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(kb))
    return State.USDT_WALLET_ACTIONS

@catch_async
async def show_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show the public address of a wallet."""
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    wallets = await WalletService.get_wallet_by_user(user_id)

    if not wallets:
        message = "<b>You don't have any wallets yet. </b>"
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
        message = "<b>Select a wallet to view its address: </b>"

    await update.callback_query.message.edit_text(
        message, reply_markup=InlineKeyboardMarkup(kb), parse_mode="HTML"
    )
    return State.SHOW_ADDRESS


@catch_async
async def show_specific_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show the specific wallet address."""
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id

    # Get the user's language preference (default to 'en' if not set)
    user_language = context.user_data.get("language", "en")

    # Fetch the appropriate language data

    # Extract wallet ID from callback data
    wallet_id = query.data.split("_")[-1]
    wallet = await WalletService.get_wallet_by_id(wallet_id)

    if wallet:
        # Format the wallet details using the language-specific template
        message = get_text(user_id, "wallet_details").format(
            name=wallet["name"], public_key=wallet["public_key"]
        )

        # Add a back button for navigation
        kb = [
            [
                InlineKeyboardButton(
                    get_text(user_id, "back_button"),
                    callback_data="back_to_wallet_menu",
                )
            ]
        ]
    else:
        message = get_text(user_id, "wallet_not_found")
        kb = []  # No keyboard if wallet is not found

    # Edit the message with the formatted text and keyboard
    await update.callback_query.message.edit_text(
        message, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb)
    )
    return State.WALLET_MENU


@catch_async
async def view_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View transaction history."""
    query = update.callback_query
    await query.answer()

    # Get the user's language preference (default to 'en' if not set)
    user_language = context.user_data.get("language", "en")

    # Fetch the appropriate language data

    user_id = update.effective_user.id
    wallets = await WalletService.get_wallet_by_user(user_id, False)

    if not wallets or wallets == []:
        message = get_text(user_id, "no_wallets")
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
        message = get_text(user_id, "select_wallet")  # Use the translated message

    # Ensure `kb` is always defined before using it
    await update.callback_query.message.edit_text(
        message, reply_markup=InlineKeyboardMarkup(kb)
    )
    return State.VIEW_HISTORY


@catch_async
async def view_specific_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View the specific wallet's transaction history."""
    query = update.callback_query
    wallet_id = query.data.split("_")[-1]
    wallet = await WalletService.get_wallet_by_id(wallet_id)

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
        message = "Wallet not found."

    await update.callback_query.message.edit_text(message)
    return State.WALLET_MENU


@catch_async
async def create_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ask the user to select the wallet type."""
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id

    # Create buttons for wallet type selection
    keyboard = [
        [
            InlineKeyboardButton(get_text(user_id, "usdt_btn"), callback_data="USDT"),
            InlineKeyboardButton(get_text(user_id, "sol_btn"), callback_data="SOL"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    message = "Please select the wallet type:"
    await query.edit_message_text(text=message, reply_markup=reply_markup)
    return State.SELECT_WALLET_TYPE


@catch_async
async def select_wallet_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store the selected wallet type and ask for the wallet name."""
    query = update.callback_query
    await query.answer()

    # Store the selected wallet type in context
    context.user_data["wallet_type"] = query.data

    message = "Please enter the wallet name:"
    await query.edit_message_text(text=message)
    return State.ENTER_WALLET_NAME


@catch_async
async def process_create_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process the wallet creation with the provided name and type."""
    wallet_name = update.message.text.strip()
    wallet_type = context.user_data.get("wallet_type")
    user_id = update.effective_user.id

    # Check if the wallet name is already used
    if await WalletService.check_wallet_name_used(user_id, wallet_name):
        message = (
            "A wallet with this name already exists. Please choose a different name."
        )
        await update.message.reply_text(message)
        return State.ENTER_WALLET_NAME

    # Create the wallet
    wallet = await WalletService.create_wallet(user_id, wallet_type, wallet_name)

    

    message = get_text(user_id=user_id, key="wallet_create_details").format(
        name=wallet.name,
        wallet_type=wallet.wallet_type,
        public_key=wallet.public_key,
        secret_key=wallet.private_key,
    )

    await update.message.reply_text(
        message,
        parse_mode="HTML",
    )
    return State.WALLET_MENU


@catch_async
async def delete_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Delete a wallet."""
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    wallets = await WalletService.get_wallet_by_user(user_id, False)

    if not wallets:
        message = "You don't have any wallets to delete."
        await query.message.edit_text(message)
        return State.WALLET_MENU

    kb = [
        [
            InlineKeyboardButton(
                wallet.name, callback_data=f"confirm_delete_wallet_{wallet.id}"
            )
        ]
        for wallet in wallets
    ]

    message = "Select a wallet to delete:"
    await query.message.edit_text(message, reply_markup=InlineKeyboardMarkup(kb))
    return State.CONFIRM_DELETE_WALLET


@catch_async
async def confirm_delete_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ask for confirmation before deleting the wallet."""
    query = update.callback_query
    wallet_id = query.data.split("_")[-1]

    kb = [
        [
            InlineKeyboardButton(
                "Yes, delete", callback_data=f"delete_wallet_{wallet_id}"
            ),
            InlineKeyboardButton("Cancel", callback_data="wallet_menu"),
        ]
    ]

    message = (
        "Are you sure you want to delete this wallet? This action cannot be undone."
    )
    await query.message.edit_text(message, reply_markup=InlineKeyboardMarkup(kb))
    return State.DELETE_WALLET


@catch_async
async def process_delete_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process the deletion of a wallet."""
    query = update.callback_query
    wallet_id = query.data.split("_")[-1]

    success = await WalletService.soft_delete_wallet(wallet_id)
    message = "Wallet deleted successfully." if success else "Failed to delete wallet."

    await query.message.edit_text(message)
    return State.WALLET_MENU


#  ----------------------- Back to the Wallet Menu ------------------------
@catch_async
async def back_to_wallet_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles going back to the wallet menu."""
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    message = get_text(user_id, "wallet_menu_message")  # Load the wallet menu message

    kb = [
        [
            InlineKeyboardButton(
                get_text(user_id, "refresh_btn"), callback_data="refresh_wallets"
            )
        ],
        [
            InlineKeyboardButton(
                get_text(user_id, "sol_btn"), callback_data="sol_wallets"
            ),
            InlineKeyboardButton(
                get_text(user_id, "usdt_btn"), callback_data="usdt_wallets"
            ),
        ],
        [
            InlineKeyboardButton(
                get_text(user_id, "address_btn"), callback_data="show_address"
            )
        ],
        [
            InlineKeyboardButton(
                get_text(user_id, "history_btn"), callback_data="view_history"
            )
        ],
        [
            InlineKeyboardButton(
                get_text(user_id, "create_wallet_btn"), callback_data="create_wallet"
            ),
            InlineKeyboardButton(
                get_text(user_id, "delete_wallet_btn"), callback_data="delete_wallet"
            ),
        ],
    ]

    welcome_text = get_text(user_id, "welcome_text")

    if update.message:
        await update.message.reply_text(
            get_text(user_id, "welcome_text"), reply_markup=InlineKeyboardMarkup(kb)
        )
    elif update.callback_query:
        await update.callback_query.message.reply_text(
            get_text(user_id, "welcome_text"), reply_markup=InlineKeyboardMarkup(kb)
        )
    return State.WALLET_MENU
