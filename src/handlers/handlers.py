wallet_handler = ConversationHandler(
    entry_points=[CommandHandler("wallets", wallet_command)],
    states={
        State.WALLETS.WALLET_MENU: [
            CallbackQueryHandler(refresh_wallets, pattern="^refresh_wallets$"),
            CallbackQueryHandler(sol_wallets, pattern="^sol_wallets$"),
            CallbackQueryHandler(usdt_wallets, pattern="^usdt_wallets$"),
            CallbackQueryHandler(show_address, pattern="^show_address$"),
            CallbackQueryHandler(view_history, pattern="^view_history$"),
            CallbackQueryHandler(create_wallet, pattern="^create_wallet$"),
            CallbackQueryHandler(delete_wallet, pattern="^delete_wallet$"),
            CallbackQueryHandler(
                back_to_wallet_menu, pattern="^back_to_wallet_menu$"
            ),  # TESTED
        ],
        State.WALLETS.SOL_WALLET_DETAIL: [
            CallbackQueryHandler(show_sol_wallet_detail, pattern="^sol_detail_"),
            CallbackQueryHandler(back_to_wallet_menu, pattern="^back_to_wallet_menu$"),
        ],
        State.WALLETS.SOL_WALLET_ACTIONS: [
            CallbackQueryHandler(request_private_key, pattern="^req_pk_"),
            CallbackQueryHandler(back_to_wallet_menu, pattern="^back_to_wallet_menu$"),
        ],
        State.WALLETS.USDT_WALLET_DETAIL: [
            CallbackQueryHandler(show_usdt_wallet_detail, pattern="^usdt_detail_"),
            CallbackQueryHandler(back_to_wallet_menu, pattern="^back_to_wallet_menu$"),
        ],
        State.WALLETS.USDT_WALLET_ACTIONS: [
            CallbackQueryHandler(request_private_key, pattern="^req_pk_"),
            CallbackQueryHandler(back_to_wallet_menu, pattern="^back_to_wallet_menu$"),
        ],
        State.WALLETS.CONFIRM_PRIVATE_KEY: [
            CallbackQueryHandler(show_private_key, pattern="^(confirm_pk|cancel_pk)$"),
            CallbackQueryHandler(back_to_wallet_menu, pattern="^back_to_wallet_menu$"),
        ],
        State.WALLETS.SHOW_ADDRESS: [
            CallbackQueryHandler(show_specific_address, pattern="^show_address_"),
            CallbackQueryHandler(back_to_wallet_menu, pattern="^back_to_wallet_menu$"),
        ],
        State.WALLETS.VIEW_HISTORY: [
            CallbackQueryHandler(view_specific_history, pattern="^view_history_"),
            CallbackQueryHandler(back_to_wallet_menu, pattern="^back_to_wallet_menu$"),
        ],
        State.WALLETS.SELECT_WALLET_TYPE: [
            CallbackQueryHandler(
                select_wallet_type, pattern="^(USDT|SOL)$"
            ),  # Handle wallet type selection
        ],
        State.WALLETS.ENTER_WALLET_NAME: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, process_create_wallet
            ),  # Handle wallet name input
        ],
        State.WALLETS.CONFIRM_DELETE_WALLET: [
            CallbackQueryHandler(
                confirm_delete_wallet, pattern="^confirm_delete_wallet_"
            ),
        ],
        State.WALLETS.DELETE_WALLET: [
            CallbackQueryHandler(process_delete_wallet, pattern="^delete_wallet_"),
            CallbackQueryHandler(cancel_delete_wallet, pattern="^cancel_delete_wallet"),
        ],
        State.WALLETS.END: [CommandHandler("wallet", wallet_command)],
    },
    fallbacks=[
        CommandHandler("cancel", cancel),
    ],
    allow_reentry=True,
)