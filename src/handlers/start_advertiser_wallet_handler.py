
# DEBUGGING FROM START
@catch_async
async def advertiser_wallet_type_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    # Determine wallet type (SOL or USDT) from callback data
    wallet_type = query.data

    context.user_data["wallet_type"] = wallet_type

    print(f"Wallet type: {wallet_type}")

    existing_wallets = await WalletService.get_wallet_by_type(user_id, wallet_type)

    if existing_wallets:
        kb = [
            [
                InlineKeyboardButton(
                    wallet.name, callback_data=f"wallet_{str(wallet.id)}"
                )
            ]
            for wallet in existing_wallets
        ]
        kb.append(
            [
                InlineKeyboardButton(
                    get_text(user_id, "create_new_wallet"),
                    callback_data="create_new_wallet",
                )
            ]
        )
        await query.edit_message_text(
            get_text(user_id, "choose_existing_or_new_wallet"),
            reply_markup=InlineKeyboardMarkup(kb),
            parse_mode="HTML",
        )
        return State.CHOOSE_WALLET_TYPE
    else:
        msg = get_text(user_id, "wallet_name_prompt")
        if update.message:
            await update.message.reply_text(msg, parse_mode="HTML")
        elif update.callback_query:
            await update.callback_query.message.reply_text(msg, parse_mode="HTML")

        return State.NAME_WALLET


@catch_async
async def advertiser_wallet_selection_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    # Extract wallet name and type from callback data
    wallet_id = query.data.replace("wallet_", "")
    wallet_type = context.user_data.get("wallet_type")  # 'sol' or 'usdt'

    # Fetch wallet details by name and type
    wallet_details = await WalletService.get_wallet_by_id(wallet_id)

    print(f"Wallet details: {wallet_details}")

    if wallet_details:
        # Fetch balance for the specific wallet type (SOL or USDT)
        print(f"This is the wallet type: {wallet_type}")

        total_sol = (
            await WalletService.get_sol_balance(wallet_details["public_key"])
            if wallet_type == "SOL"
            else await WalletService.get_usdt_balance(wallet_details["public_key"])
        )

        print(f"Total {wallet_type}: {total_sol}")

        context.user_data["wallet"] = wallet_details  # Store in memory
        await update_or_create_case(user_id, wallet=str(wallet_details["id"]))

        msg = get_text(user_id, "wallet_create_details_with_balance").format(
            name=wallet_details["name"],
            public_key=wallet_details["public_key"],
            network=get_network(wallet_details["wallet_type"]),
            balance=total_sol,  # For USDT, balance might be different
            wallet_type=wallet_type,
        )

        transfer_instructions = get_text(user_id, "transfer_instructions").format(
            wallet_type=wallet_type,
            public_key=wallet_details["public_key"],
        )
        msg += transfer_instructions

        await query.edit_message_text(msg, parse_mode="HTML")

        # Transition to the Create Case flow
        await query.message.reply_text(get_text(user_id, "create_case_title", "cases"))
        await query.message.reply_text(get_text(user_id, "enter_name", "cases"))
        return State.CREATE_CASE_NAME
    else:
        await query.edit_message_text(
            get_text(user_id, "wallet_not_found"), parse_mode="HTML"
        )
        return State.END


@catch_async
async def advertiser_wallet_name_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    user_id = update.effective_user.id
    if update.callback_query:
        # If it's a callback query, prompt the user to enter a wallet name
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            get_text(user_id, "wallet_name_prompt"), parse_mode="HTML"
        )
        return State.NAME_WALLET

    wallet_name = update.message.text.strip()

    print(f"Wallet name: {wallet_name}")

    if not wallet_name:
        await update.message.reply_text(
            get_text(user_id, "wallet_name_empty"), parse_mode="HTML"
        )
        return State.NAME_WALLET

    print("Hello there how are you doing", wallet_name)

    wallet_type = context.user_data.get("wallet_type")

    print(f"Wallet type: {wallet_type}")

    wallet = await WalletService.create_wallet(user_id, wallet_type, wallet_name)
    if wallet:

        if wallet_type == "SOL":
            total_sol = await WalletService.get_sol_balance(wallet.public_key)
        elif wallet_type == "USDT":
            total_sol = await WalletService.get_usdt_balance(wallet.public_key)

        print(f"Total SOL: {total_sol}")
        print(f"This is the wallet type: {wallet_type}")

        context.user_data["wallet"] = wallet
        msg = get_text(user_id, "wallet_create_details_with_balance").format(
            name=wallet.name,
            public_key=wallet.public_key,
            balance=total_sol,  # For USDT, the balance logic will vary
            wallet_type=wallet_type,
            network = get_network(wallet_type),
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