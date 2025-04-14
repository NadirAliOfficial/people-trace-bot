WALLET_LANG_DATA = {
    "en": {
        "choose_wallet": "Please choose the type of wallet:",
        "sol_wallet": "Solana (SOL)",
        "usdt_wallet": "USD Tether (USDT)",
        "choose_existing_or_new_wallet": "Choose Existing Wallet or Create New One",
        "wallet_name_prompt": "You've chosen a {wallet_type} wallet.\nPlease enter a name for your wallet:",
        "wallet_name_empty": "❌ Wallet name cannot be empty. Please try again.",
        "wallet_create_ok": "✅ Wallet Created Successfully!\n\n",
        "wallet_create_details": (
            "✅ <b>Wallet Created Successfully!</b> \n\n"
            "📌 <b>Wallet Information:</b>\n"
            "🧾 <b>Name:</b> <code>{name}</code>\n"
            "💰 <b>Type:</b> <code>{wallet_type}</code>\n"
            "🔐 <b>Public Key:</b> <code>{public_key}</code>\n"
            # "🗝️ <b>Secret Key:</b> <code>{secret_key}</code>\n"
            # "💵 <b>Balance:</b> <code>{balance} {wallet_type}</code>"
        ),
        "wallet_create_err": "❌ Error creating wallet. Please try again later.",
        "cancel_msg": "Operation cancelled. Use /start to begin again.",
        "account_wallet_type": "Account Wallet Type (SOL | USDT)",
        "menu_wallet_title": "💳 Wallet Menu",
        "btn_refresh": "🔄 Refresh",
        "btn_sol": "💰 SOL",
        "btn_usdt": "💵 USDT",
        "btn_show_address": "🏠 Show Address",
        "btn_create_wallet": "➕ Create Wallet",
        "btn_delete_wallet": "🗑️ Delete Wallet",
        "wallet_no_exists": "❌ No wallet found. Please create one using the 'Create Wallet' button.",
        "wallet_exists": "📌 <b>Existing Wallet:</b>\nName: {name}\nPublic Key: `{pub}`\nBalance: {bal} SOL",
        "wallet_deleted": "✅ Wallet deleted successfully.",
        "wallet_not_deleted": "❌ No wallet to delete.",
        "wallet_refreshed": "🔄 Balance updated:\nName: {name}\nPublic Key: `{pub}`\nBalance: {bal} SOL",
        "guide_create_wallet": (
            "📝 <b>How to Create a Wallet:</b>\n"
            "1️⃣ Choose the wallet type (SOL or USDT).\n"
            "2️⃣ Enter a unique name for your wallet.\n"
            "3️⃣ Your wallet will be created with a public key and secret key.\n"
            "4️⃣ Use the public key to receive funds.\n\n"
            "💡 Tip: Keep your secret key safe and never share it with anyone."
        ),
        "guide_delete_wallet": (
            "⚠️ <b>Important Information:</b>\n"
            "Deleting a wallet is irreversible. All funds in the wallet will be lost.\n"
            "Make sure you have transferred all funds before proceeding."
        ),
        "no_wallets": "You don't have any wallets yet.",
        "select_wallet": "Select a wallet to view its transaction history:",
        "wallet_details": "**Wallet Name:** {name} \n\n **Public Address:** `{public_key}`",
        "wallet_not_found": "Wallet not found.",
        "back_button": "Back",
        "sol_wallets_header": "<b>Your SOL Wallets:</b>\n",
        "wallet_balance": "<b>Name:</b> {name}, <b>Balance:</b> {balance} SOL\n",
        "wallet_error": "<b>Name:</b> {name}, <b>Error:</b> {error}\n",
          "no_sol_wallets": "You don't have any SOL wallets yet.",
        "no_usdt_wallets": "You don't have any USDT wallets yet.",
        "back_button": "⬅️ Back",
        "refresh_btn": "🔄 Refresh",
        "wallet_not_found": "Wallet not found."
    },
    "zh": {
        "choose_wallet": "请选择要创建的钱包类型：",
        "sol_wallet": "Solana (SOL)",
        "usdt_wallet": "比特币 (BTC)",
        "choose_existing_or_new_wallet": "选择现有钱包或创建新钱包：",
        "wallet_name_prompt": "您选择了 {wallet_type} 钱包。\n请输入钱包名称：",
        "wallet_name_empty": "❌ 钱包名称不能为空。请重试。",
        "wallet_create_ok": "✅ 成功创建钱包！\n\n",
        "wallet_create_details": (
            "📌 <b>钱包详情：</b>\n"
            "名称: {name}\n"
            "公钥: `{public_key}`\n"
            "私钥: `{secret_key}`\n"
            "余额: {balance} {wallet_type}"
        ),
        "wallet_create_err": "❌ 创建钱包时出错。请稍后重试。",
        "cancel_msg": "操作已取消。输入 /start 重新开始。",
        "account_wallet_type": "账户钱包类型 (SOL | BTC)",
        "menu_wallet_title": "💳 钱包菜单",
        "btn_refresh": "🔄 刷新",
        "btn_sol": "💰 SOL",
        "btn_usdt": "💵 USDT",
        "btn_show_address": "🏠 显示地址",
        "btn_create_wallet": "➕ 创建钱包",
        "btn_delete_wallet": "🗑️ 删除钱包",
        "wallet_no_exists": "❌ 当前没有可用钱包。请使用“创建钱包”按钮创建一个。",
        "wallet_exists": "📌 <b>现有钱包：</b>\n名称: {name}\n公钥: `{pub}`\n余额: {bal} SOL",
        "wallet_deleted": "✅ 钱包已成功删除。",
        "wallet_not_deleted": "❌ 没有可删除的钱包。",
        "wallet_refreshed": "🔄 余额已更新:\n名称: {name}\n公钥: `{pub}`\n余额: {bal} SOL",
        "guide_create_wallet": (
            "📝 <b>如何创建钱包：</b>\n"
            "1️⃣ 选择钱包类型（SOL 或 USDT）。\n"
            "2️⃣ 输入唯一的钱包名称。\n"
            "3️⃣ 钱包将生成公钥和私钥。\n"
            "4️⃣ 使用公钥接收资金。\n\n"
            "💡 提示：妥善保管您的私钥，切勿与他人分享。"
        ),
        "guide_delete_wallet": (
            "⚠️ <b>重要信息：</b>\n"
            "删除钱包是不可逆的。钱包中的所有资金将丢失。\n"
            "在继续之前，请确保已转移所有资金。"
        ),
        "no_wallets": "您还没有任何钱包。",
        "select_wallet": "选择一个钱包以查看其交易记录：",
        "wallet_details": "**钱包名称:** {name} \n\n **公共地址:** `{public_key}`",
        "wallet_not_found": "未找到钱包。",
        "back_button": "返回",
        "sol_wallets_header": "<b>您的 SOL 钱包：</b>\n",
        "wallet_balance": "<b>名称：</b> {name}, <b>余额：</b> {balance} SOL\n",
        "wallet_error": "<b>名称：</b> {name}, <b>错误：</b> {error}\n",
    },
    "ms": {
        "choose_wallet": "Sila pilih jenis dompet:",
        "sol_wallet": "Solana (SOL)",
        "usdt_wallet": "USD Tether (USDT)",
        "choose_existing_or_new_wallet": "Pilih Dompet Sedia Ada atau Buat Yang Baru",
        "wallet_name_prompt": "Anda telah memilih dompet {wallet_type}.\nSila masukkan nama untuk dompet anda:",
        "wallet_name_empty": "❌ Nama dompet tidak boleh kosong. Sila cuba lagi.",
        "wallet_create_ok": "✅ Dompet berjaya dicipta!\n\n",
        "wallet_create_details": (
            "📌 <b>Maklumat Dompet:</b>\n"
            "Nama: {name}\n"
            "Kunci Awam: `{public_key}`\n"
            "Kunci Rahsia: `{secret_key}`\n"
            "Baki: {balance} {wallet_type}"
        ),
        "wallet_create_err": "❌ Ralat semasa mencipta dompet. Sila cuba lagi kemudian.",
        "cancel_msg": "Operasi dibatalkan. Gunakan /start untuk memulakan semula.",
        "account_wallet_type": "Jenis Dompet Akaun (SOL | USDT)",
        "menu_wallet_title": "💳 Menu Dompet",
        "btn_refresh": "🔄 Segar Semula",
        "btn_sol": "💰 SOL",
        "btn_usdt": "💵 USDT",
        "btn_show_address": "🏠 Tunjukkan Alamat",
        "btn_create_wallet": "➕ Buat Dompet",
        "btn_delete_wallet": "🗑️ Padam Dompet",
        "wallet_no_exists": "❌ Tiada dompet ditemui. Sila buat satu menggunakan butang 'Buat Dompet'.",
        "wallet_exists": "📌 <b>Dompet Sedia Ada:</b>\nNama: {name}\nKunci Awam: `{pub}`\nBaki: {bal} SOL",
        "wallet_deleted": "✅ Dompet berjaya dipadamkan.",
        "wallet_not_deleted": "❌ Tiada dompet untuk dipadamkan.",
        "wallet_refreshed": "🔄 Baki dikemas kini:\nNama: {name}\nKunci Awam: `{pub}`\nBaki: {bal} SOL",
        "guide_create_wallet": (
            "📝 <b>Cara Membuat Dompet:</b>\n"
            "1️⃣ Pilih jenis dompet (SOL atau USDT).\n"
            "2️⃣ Masukkan nama unik untuk dompet anda.\n"
            "3️⃣ Dompet akan dicipta dengan kunci awam dan kunci rahsia.\n"
            "4️⃣ Gunakan kunci awam untuk menerima dana.\n\n"
            "💡 Petua: Simpan kunci rahsia anda dengan selamat dan jangan kongsikan dengan sesiapa."
        ),
        "guide_delete_wallet": (
            "⚠️ <b>Maklumat Penting:</b>\n"
            "Memadam dompet adalah tindakan yang tidak boleh dibatalkan. Semua dana dalam dompet akan hilang.\n"
            "Pastikan anda telah memindahkan semua dana sebelum meneruskan."
        ),
        "no_wallets": "Anda belum mempunyai dompet lagi.",
        "select_wallet": "Pilih dompet untuk melihat sejarah transaksi:",
        "wallet_details": "**Nama Dompet:** {name} \n\n **Alamat Awam:** `{public_key}`",
        "wallet_not_found": "Dompet tidak ditemui.",
        "back_button": "Kembali",
        "sol_wallets_header": "<b>Dompet SOL Anda:</b>\n",
        "wallet_balance": "<b>Nama:</b> {name}, <b>Baki:</b> {balance} SOL\n",
        "wallet_error": "<b>Nama:</b> {name}, <b>Ralat:</b> {error}\n",
    },
}
