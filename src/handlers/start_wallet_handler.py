from services.case_service import update_or_create_case
from services.tron_wallet_service import TronWallet
from services.wallet_service import WalletService
from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import (
    ContextTypes,
)
from constants import (
    State,
)
from utils.error_wrapper import catch_async
from utils.get_network import get_network
from constant.language_constant import get_text


@catch_async
async def wallet_type_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Step 1: Ask user to create or use an existing wallet after choosing type."""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    wallet_type = query.data  # "USDT" or "SOL"
    context.user_data["wallet_type"] = wallet_type

    buttons = [
        [
            InlineKeyboardButton(
                get_text(user_id, "create_wallet", "globals"),
                callback_data="create_new_wallet",
            ),
            InlineKeyboardButton(
                get_text(user_id, "use_existing_wallet", "globals"),
                callback_data="use_existing_wallet",
            ),
        ]
    ]

    await query.edit_message_text(
        get_text(user_id, "choose_existing_or_new_wallet", "start-wallet"),
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="HTML",
    )
    return State.CHOOSE_OR_CREATE_WALLET


@catch_async
async def show_existing_wallets_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Show paginated list of user's existing wallets by type (with limit & offset)."""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    wallet_type = context.user_data.get("wallet_type")

    page = int(context.user_data.get("wallet_page", 0))
    page_size = 5
    offset = page * page_size

    # Fetch only the wallets for current page
    paginated_wallets = await WalletService.get_wallet_by_type(
        user_id=user_id, wallet_type=wallet_type, limit=page_size, offset=offset
    )

    # If no wallets on this page, and it's the first page, show fallback
    if not paginated_wallets and page == 0:
        await query.edit_message_text(
            get_text(user_id, "no_wallets_found", "start-wallet").format(
                wallet_type=wallet_type
            ),
            parse_mode="HTML",
        )
        return State.END

    # If no wallets on this page, but there were on previous ones (e.g. user hit "Next" too far)
    if not paginated_wallets:
        context.user_data["wallet_page"] = 0  # Reset to first page
        return await show_existing_wallets_handler(update, context)

    # Build inline keyboard for this page
    kb = [
        [InlineKeyboardButton(wallet.name, callback_data=f"wallet_{wallet.id}")]
        for wallet in paginated_wallets
    ]

    # Add pagination controls
    nav_buttons = []
    if page > 0:
        nav_buttons.append(
            InlineKeyboardButton(
                get_text(user_id, "prev", "globals"), callback_data="wallet_page_prev"
            )
        )
    if len(paginated_wallets) == page_size:  # Possibly more pages
        nav_buttons.append(
            InlineKeyboardButton(
                get_text(user_id, "next", "globals"), callback_data="wallet_page_next"
            )
        )
    if nav_buttons:
        kb.append(nav_buttons)

    await query.edit_message_text(
        get_text(user_id, "choose_existing_wallet", "start-wallet"),
        reply_markup=InlineKeyboardMarkup(kb),
        parse_mode="HTML",
    )
    return State.CHOOSE_OR_CREATE_WALLET


@catch_async
async def wallet_pagination_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    query = update.callback_query
    await query.answer()

    direction = query.data  # "wallet_page_next" or "wallet_page_prev"
    current_page = int(context.user_data.get("wallet_page", 0))

    if direction == "wallet_page_next":
        context.user_data["wallet_page"] = current_page + 1
    elif direction == "wallet_page_prev" and current_page > 0:
        context.user_data["wallet_page"] = current_page - 1

    return await show_existing_wallets_handler(update, context)


@catch_async
async def wallet_selection_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    wallet_id = query.data.replace("wallet_", "")
    wallet_type = context.user_data.get("wallet_type")  # 'sol' or 'usdt'

    wallet_details = await WalletService.get_wallet_by_id(wallet_id)

    if wallet_details:
        total_sol = (
            await WalletService.get_sol_balance(wallet_details["public_key"])
            if wallet_type == "SOL"
            else await TronWallet.get_usdt_balance(wallet_details["public_key"])
        )

        print(f"Total {wallet_type}: {total_sol}")

        context.user_data["wallet"] = wallet_details  # Store in memory
        await update_or_create_case(user_id, wallet=str(wallet_details["id"]))

        msg = get_text(
            user_id, "wallet_create_details_with_balance", "start-wallet"
        ).format(
            name=wallet_details["name"],
            public_key=wallet_details["public_key"],
            balance=total_sol,
            wallet_type=wallet_type,
            network=get_network(wallet_type),
        )

        transfer_instructions = get_text(
            user_id, "transfer_instructions", "start-wallet"
        ).format(
            wallet_type=wallet_type,
            public_key=wallet_details["public_key"],
        )

        full_msg = (
            msg
            + transfer_instructions
            + get_text(user_id, "wallet_summary", "start-wallet").format(
                total_sol=total_sol,
                public_key=wallet_details["public_key"],
                wallet_type=wallet_type,
            )
        )

        buttons = [
            [
                InlineKeyboardButton(
                    get_text(user_id, "refresh_wallet", "globals"),
                    callback_data="refresh_wallet",
                ),
                InlineKeyboardButton(
                    get_text(user_id, "continue_case", "globals"),
                    callback_data="create_case",
                ),
            ]
        ]

        await query.message.reply_text(
            full_msg, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(buttons)
        )
        return State.HANDLE_REPLY  # Use a custom state if needed
    else:
        await query.edit_message_text(
            get_text(user_id, "wallet_not_found", "start-wallet"), parse_mode="HTML"
        )
        return State.END


@catch_async
async def wallet_name_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    query = update.callback_query
    wallet_type = context.user_data.get("wallet_type")  # 'sol' or 'usdt'
    user_id = update.effective_user.id
    if update.callback_query:
        # If it's a callback query, prompt the user to enter a wallet name
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            get_text(user_id, "wallet_name_prompt", "start-wallet").format(wallet_type=wallet_type),
            parse_mode="HTML",
        )
        return State.NAME_WALLET

    wallet_name = update.message.text.strip()

    print(f"Wallet name: {wallet_name}")

    if not wallet_name:
        await update.message.reply_text(
            get_text(user_id, "wallet_name_empty", "start-wallet"), parse_mode="HTML"
        )
        return State.NAME_WALLET

    wallet_type = context.user_data.get("wallet_type")

    if await WalletService.check_wallet_name_used_with_type(
        user_id, wallet_name, wallet_type
    ):

        await update.message.reply_text(get_text(user_id, "wallet_name_exists", "start-wallet"))
        return State.NAME_WALLET

    wallet = await WalletService.create_wallet(user_id, wallet_type, wallet_name)
    if wallet:
        if wallet_type == "SOL":
            total_sol = await WalletService.get_sol_balance(wallet.public_key)
        elif wallet_type == "USDT":
            total_sol = await TronWallet.get_usdt_balance(wallet.public_key)

        context.user_data["wallet"] = wallet
        await update_or_create_case(user_id, wallet=str(wallet.id))
        msg = get_text(user_id, "wallet_create_details_with_balance", "start-wallet").format(
            name=wallet.name,
            public_key=wallet.public_key,
            network=get_network(wallet_type),
            balance=total_sol,  # For USDT, the balance logic will vary
            wallet_type=wallet_type,
        )

        transfer_instructions = get_text(user_id, "transfer_instructions", "start-wallet").format(
            wallet_type=wallet_type,
            public_key=wallet.public_key,
        )

        full_msg = (
            msg
            + transfer_instructions
            + f"\n\n<b>💰 Current Balance:</b> {total_sol} {wallet_type}\n<b>🔗 Wallet Address (TRC20):</b> <code>{wallet.public_key}</code>"
        )

        buttons = [
            [
                InlineKeyboardButton(
                    get_text(user_id, "refresh_wallet", "globals"), callback_data="refresh_wallet"
                ),
                InlineKeyboardButton(
                    get_text(user_id, "continue_case", "globals"), callback_data="create_case"
                ),
            ]
        ]

        await update.message.reply_text(
            full_msg, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(buttons)
        )
        return State.HANDLE_REPLY  # Use a custom state if needed
    else:
        await update.message.reply_text(
            get_text(user_id, "wallet_create_err", "start-wallet"), parse_mode="HTML"
        )
        return State.END
