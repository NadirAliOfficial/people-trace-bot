START_WALLET_CONSTANT = {
    "english": {  # English
        "choose_wallet_header": "💼 Before posting your case, you’ll need a crypto wallet for the reward bounty.\n"
        "Please choose a wallet type to proceed:",
        "choose_existing_or_new_wallet": "Choose an existing wallet or create a new one:",
        "no_wallets_found": "No wallets  found. ",
        "choose_existing_wallet": "Choose a wallet type:",
        "wallet_create_details_with_balance": (
            "<b>✅ Wallet Created!</b>\n"
            "🧾 <b>Name:</b> {name}\n"
            "💰 <b>Type:</b> {wallet_type}\n"
            "🔐 <b>Public Key:</b> <code>{public_key}</code>\n"
            "🌐 <b>Network:</b> {network}\n"
            "💵 <b>Balance:</b> {balance} {wallet_type}\n"
        ),
        "transfer_instructions": (
            "\n\n<b>💡 How to Transfer {wallet_type} to Your Wallet:</b>\n\n"
            "1️⃣ Open your {wallet_type}-compatible wallet app.\n"
            "2️⃣ Tap <b>Send</b> or <b>Transfer</b>.\n"
            "3️⃣ Paste your <b>Public Key</b> as the recipient:\n<code>{public_key}</code>\n"
            "4️⃣ Select the correct network: <b>TRC20 (Tron Network)</b>\n"
            "5️⃣ Enter the amount and confirm the transfer.\n"
        ),
        "wallet_summary": (
            "\n\n<b>💰 Current Balance:</b> {total_sol} {wallet_type}"
            "\n<b>🔗 Wallet Address (TRC20):</b> <code>{public_key}</code>"
        ),
        "wallet_not_found": "❌ Wallet not found. Please try again.",
        "wallet_name_empty": "❌ Wallet name cannot be empty. Please try again.",
        "wallet_name_prompt": "Please enter a name for your {wallet_type} wallet:",
        "wallet_name_prompt": "Please enter a name for your {wallet_type} wallet:",
        "wallet_create_err": "An error occurred while creating the wallet. Please try again.",
    },
}
