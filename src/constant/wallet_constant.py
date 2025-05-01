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
    "ur": {
    "choose_wallet": "براہ کرم والیٹ کی قسم منتخب کریں:",
    "sol_wallet": "سولانا (SOL)",
    "usdt_wallet": "یو ایس ڈی ٹی (USDT)",
    "choose_existing_or_new_wallet": "موجودہ والیٹ منتخب کریں یا نیا بنائیں",
    "wallet_name_prompt": "آپ نے {wallet_type} والیٹ منتخب کیا ہے۔\nبراہ کرم اپنے والیٹ کے لیے ایک نام درج کریں:",
    "wallet_name_empty": "❌ والیٹ کا نام خالی نہیں ہو سکتا۔ دوبارہ کوشش کریں۔",
    "wallet_create_ok": "✅ والیٹ کامیابی سے بنایا گیا!\n\n",
    "wallet_create_details": (
        "📌 <b>والیٹ کی معلومات:</b>\n"
        "🧾 <b>نام:</b> <code>{name}</code>\n"
        "💰 <b>قسم:</b> <code>{wallet_type}</code>\n"
        "🔐 <b>پبلک کلید:</b> <code>{public_key}</code>\n"
    ),
    "wallet_create_err": "❌ والیٹ بنانے میں خرابی۔ براہ کرم بعد میں دوبارہ کوشش کریں۔",
    "cancel_msg": "عمل منسوخ کر دیا گیا۔ دوبارہ شروع کرنے کے لیے /start استعمال کریں۔",
    "account_wallet_type": "اکاؤنٹ والیٹ کی قسم (SOL | USDT)",
    "menu_wallet_title": "💳 والیٹ مینو",
    "btn_refresh": "🔄 تازہ کریں",
    "btn_sol": "💰 SOL",
    "btn_usdt": "💵 USDT",
    "btn_show_address": "🏠 پتہ دکھائیں",
    "btn_create_wallet": "➕ نیا والیٹ بنائیں",
    "btn_delete_wallet": "🗑️ والیٹ حذف کریں",
    "wallet_no_exists": "❌ کوئی والیٹ نہیں ملا۔ 'نیا والیٹ بنائیں' بٹن استعمال کریں۔",
    "wallet_exists": "📌 <b>موجودہ والیٹ:</b>\nنام: {name}\nپبلک کلید: {pub}\nبیلنس: {bal} SOL",
    "wallet_deleted": "✅ والیٹ کامیابی سے حذف کر دیا گیا۔",
    "wallet_not_deleted": "❌ حذف کرنے کے لیے کوئی والیٹ نہیں ملا۔",
    "wallet_refreshed": "🔄 بیلنس تازہ کر دیا گیا:\nنام: {name}\nپبلک کلید: {pub}\nبیلنس: {bal} SOL",
    "guide_create_wallet": (
        "📝 <b>والیٹ کیسے بنائیں:</b>\n"
        "1️⃣ والیٹ کی قسم منتخب کریں (SOL یا USDT).\n"
        "2️⃣ اپنے والیٹ کے لیے ایک منفرد نام درج کریں۔\n"
        "3️⃣ آپ کا والیٹ پبلک اور سیکرٹ کلید کے ساتھ بنایا جائے گا۔\n"
        "4️⃣ فنڈز وصول کرنے کے لیے پبلک کلید استعمال کریں۔\n\n"
        "💡 مشورہ: اپنی سیکرٹ کلید کو محفوظ رکھیں اور کسی کے ساتھ شیئر نہ کریں۔"
    ),
    "guide_delete_wallet": (
        "⚠️ <b>اہم معلومات:</b>\n"
        "والیٹ کو حذف کرنا ناقابل واپسی ہے۔ والیٹ میں موجود تمام فنڈز ضائع ہو جائیں گے۔\n"
        "آگے بڑھنے سے پہلے یقینی بنائیں کہ آپ نے تمام فنڈز منتقل کر دیے ہیں۔"
    ),
    "no_wallets": "آپ کے پاس ابھی کوئی والیٹ نہیں ہے۔",
    "select_wallet": "ٹرانزیکشن ہسٹری دیکھنے کے لیے ایک والیٹ منتخب کریں:",
    "wallet_details": "**والیٹ کا نام:** {name} \n\n **پبلک پتہ:** {public_key}",
    "wallet_not_found": "والیٹ نہیں ملا۔",
    "back_button": "⬅️ واپس",
    "sol_wallets_header": "<b>آپ کے SOL والیٹس:</b>\n",
    "wallet_balance": "<b>نام:</b> {name}, <b>بیلنس:</b> {balance} SOL\n",
    "wallet_error": "<b>نام:</b> {name}, <b>خرابی:</b> {error}\n",
    "no_sol_wallets": "آپ کے پاس ابھی کوئی SOL والیٹ نہیں ہے۔",
    "no_usdt_wallets": "آپ کے پاس ابھی کوئی USDT والیٹ نہیں ہے۔"
}
,
"ja": {
    "choose_wallet": "ウォレットの種類を選択してください：",
    "sol_wallet": "ソラナ (SOL)",
    "usdt_wallet": "USDテザー (USDT)",
    "choose_existing_or_new_wallet": "既存のウォレットを選択するか、新しいウォレットを作成してください",
    "wallet_name_prompt": "{wallet_type}ウォレットを選択しました。\nウォレットの名前を入力してください：",
    "wallet_name_empty": "❌ ウォレット名は空にできません。もう一度お試しください。",
    "wallet_create_ok": "✅ ウォレットが正常に作成されました！\n\n",
    "wallet_create_details": (
        "📌 <b>ウォレット情報：</b>\n"
        "🧾 <b>名前：</b> <code>{name}</code>\n"
        "💰 <b>種類：</b> <code>{wallet_type}</code>\n"
        "🔐 <b>公開鍵：</b> <code>{public_key}</code>\n"
    ),
    "wallet_create_err": "❌ ウォレットの作成中にエラーが発生しました。後でもう一度お試しください。",
    "cancel_msg": "操作がキャンセルされました。再開するには /start を使用してください。",
    "account_wallet_type": "アカウントウォレットの種類 (SOL | USDT)",
    "menu_wallet_title": "💳 ウォレットメニュー",
    "btn_refresh": "🔄 更新",
    "btn_sol": "💰 SOL",
    "btn_usdt": "💵 USDT",
    "btn_show_address": "🏠 アドレスを表示",
    "btn_create_wallet": "➕ ウォレットを作成",
    "btn_delete_wallet": "🗑️ ウォレットを削除",
    "wallet_no_exists": "❌ ウォレットが見つかりません。「ウォレットを作成」ボタンを使用してください。",
    "wallet_exists": "📌 <b>既存のウォレット：</b>\n名前: {name}\n公開鍵: {pub}\n残高: {bal} SOL",
    "wallet_deleted": "✅ ウォレットが正常に削除されました。",
    "wallet_not_deleted": "❌ 削除するウォレットがありません。",
    "wallet_refreshed": "🔄 残高が更新されました：\n名前: {name}\n公開鍵: {pub}\n残高: {bal} SOL",
    "guide_create_wallet": (
        "📝 <b>ウォレットの作成方法：</b>\n"
        "1️⃣ ウォレットの種類を選択します（SOL または USDT）。\n"
        "2️⃣ ウォレットの一意の名前を入力します。\n"
        "3️⃣ 公開鍵と秘密鍵が生成されます。\n"
        "4️⃣ 公開鍵を使用して資金を受け取ります。\n\n"
        "💡 ヒント：秘密鍵は安全に保管し、他人と共有しないでください。"
    ),
    "guide_delete_wallet": (
        "⚠️ <b>重要な情報：</b>\n"
        "ウォレットの削除は取り消せません。ウォレット内のすべての資金が失われます。\n"
        "続行する前に、すべての資金を移動したことを確認してください。"
    ),
    "no_wallets": "まだウォレットがありません。",
    "select_wallet": "取引履歴を表示するウォレットを選択してください：",
    "wallet_details": "**ウォレット名：** {name} \n\n **公開アドレス：** {public_key}",
    "wallet_not_found": "ウォレットが見つかりません。",
    "back_button": "⬅️ 戻る",
    "sol_wallets_header": "<b>あなたのSOLウォレット：</b>\n",
    "wallet_balance": "<b>名前：</b> {name}, <b>残高：</b> {balance} SOL\n",
    "wallet_error": "<b>名前：</b> {name}, <b>エラー：</b> {error}\n",
    "no_sol_wallets": "まだSOLウォレットがありません。",
    "no_usdt_wallets": "まだUSDTウォレットがありません。"
}
,
"ko": {
    "choose_wallet": "지갑 유형을 선택하세요:",
    "sol_wallet": "솔라나 (SOL)",
    "usdt_wallet": "테더 (USDT)",
    "choose_existing_or_new_wallet": "기존 지갑을 선택하거나 새로 생성하세요",
    "wallet_name_prompt": "{wallet_type} 지갑을 선택하셨습니다.\n지갑의 이름을 입력하세요:",
    "wallet_name_empty": "❌ 지갑 이름은 비워둘 수 없습니다. 다시 시도해주세요.",
    "wallet_create_ok": "✅ 지갑이 성공적으로 생성되었습니다!\n\n",
    "wallet_create_details": (
        "📌 <b>지갑 정보:</b>\n"
        "🧾 <b>이름:</b> <code>{name}</code>\n"
        "💰 <b>유형:</b> <code>{wallet_type}</code>\n"
        "🔐 <b>공개 키:</b> <code>{public_key}</code>\n"
    ),
    "wallet_create_err": "❌ 지갑 생성 중 오류가 발생했습니다. 나중에 다시 시도해주세요.",
    "cancel_msg": "작업이 취소되었습니다. 다시 시작하려면 /start 를 입력해주세요.",
    "account_wallet_type": "계정 지갑 유형 (SOL | USDT)",
    "menu_wallet_title": "💳 지갑 메뉴",
    "btn_refresh": "🔄 새로고침",
    "btn_sol": "💰 SOL",
    "btn_usdt": "💵 USDT",
    "btn_show_address": "🏠 주소 보기",
    "btn_create_wallet": "➕ 새 지갑 만들기",
    "btn_delete_wallet": "🗑️ 지갑 삭제",
    "wallet_no_exists": "❌ 사용 가능한 지갑이 없습니다. '새 지갑 만들기' 버튼을 사용하세요.",
    "wallet_exists": "📌 <b>현재 지갑:</b>\n이름: {name}\n공개 키: {pub}\n잔액: {bal} SOL",
    "wallet_deleted": "✅ 지갑이 성공적으로 삭제되었습니다.",
    "wallet_not_deleted": "❌ 삭제할 지갑이 없습니다.",
    "wallet_refreshed": "🔄 잔액이 새로고침되었습니다:\n이름: {name}\n공개 키: {pub}\n잔액: {bal} SOL",
    "guide_create_wallet": (
        "📝 <b>지갑 생성 방법:</b>\n"
        "1️⃣ 지갑 유형(SOL 또는 USDT)을 선택하세요.\n"
        "2️⃣ 고유한 지갑 이름을 입력하세요.\n"
        "3️⃣ 공개 키와 비공개 키가 생성됩니다.\n"
        "4️⃣ 공개 키를 통해 자금을 수신할 수 있습니다.\n\n"
        "💡 팁: 비공개 키는 안전하게 보관하고 절대 공유하지 마세요."
    ),
    "guide_delete_wallet": (
        "⚠️ <b>중요:</b>\n"
        "지갑 삭제는 되돌릴 수 없습니다. 잔액이 남아 있는 경우 복구할 수 없습니다.\n"
        "삭제 전 모든 자산을 전송했는지 확인하세요."
    ),
    "no_wallets": "아직 생성된 지갑이 없습니다.",
    "select_wallet": "트랜잭션 기록을 확인할 지갑을 선택하세요:",
    "wallet_details": "**지갑 이름:** {name} \n\n **공개 주소:** {public_key}",
    "wallet_not_found": "지갑을 찾을 수 없습니다.",
    "back_button": "⬅️ 뒤로가기",
    "sol_wallets_header": "<b>내 SOL 지갑 목록:</b>\n",
    "wallet_balance": "<b>이름:</b> {name}, <b>잔액:</b> {balance} SOL\n",
    "wallet_error": "<b>이름:</b> {name}, <b>오류:</b> {error}\n",
    "no_sol_wallets": "SOL 지갑이 아직 없습니다.",
    "no_usdt_wallets": "USDT 지갑이 아직 없습니다."
}
,
"km": {
    "choose_wallet": "សូមជ្រើសប្រភេទកាបូប៖",
    "sol_wallet": "សូឡាណា (SOL)",
    "usdt_wallet": "យូអេសឌីធី (USDT)",
    "choose_existing_or_new_wallet": "ជ្រើសរើសកាបូបដែលមានរួច ឬបង្កើតថ្មី",
    "wallet_name_prompt": "អ្នកបានជ្រើស {wallet_type}។\nសូមបញ្ចូលឈ្មោះសម្រាប់កាបូប៖",
    "wallet_name_empty": "❌ ឈ្មោះកាបូបមិនអាចទទេបានទេ។ សូមព្យាយាមម្តងទៀត។",
    "wallet_create_ok": "✅ កាបូបបានបង្កើតដោយជោគជ័យ!\n\n",
    "wallet_create_details": (
        "📌 <b>ព័ត៌មានកាបូប:</b>\n"
        "🧾 <b>ឈ្មោះ:</b> <code>{name}</code>\n"
        "💰 <b>ប្រភេទ:</b> <code>{wallet_type}</code>\n"
        "🔐 <b>សោសាធារណៈ:</b> <code>{public_key}</code>\n"
    ),
    "wallet_create_err": "❌ មានបញ្ហា ក្នុងការបង្កើតកាបូប។ សូមសាកល្បងម្តងទៀត។",
    "cancel_msg": "ដំណើរការត្រូវបានបោះបង់។ ចាប់ផ្ដើមឡើងវិញដោយប្រើ /start",
    "account_wallet_type": "ប្រភេទកាបូបគណនី (SOL | USDT)",
    "menu_wallet_title": "💳 ម៉ឺនុយកាបូប",
    "btn_refresh": "🔄 ធ្វើបច្ចុប្បន្នភាព",
    "btn_sol": "💰 SOL",
    "btn_usdt": "💵 USDT",
    "btn_show_address": "🏠 បង្ហាញអាសយដ្ឋាន",
    "btn_create_wallet": "➕ បង្កើតកាបូបថ្មី",
    "btn_delete_wallet": "🗑️ លុបកាបូប",
    "wallet_no_exists": "❌ រកមិនឃើញកាបូប។ សូមចុច ‘បង្កើតកាបូបថ្មី’។",
    "wallet_exists": "📌 <b>កាបូបបច្ចុប្បន្ន:</b>\nឈ្មោះ: {name}\nសោសាធារណៈ: {pub}\nសមតុល្យ: {bal} SOL",
    "wallet_deleted": "✅ កាបូបបានលុបដោយជោគជ័យ។",
    "wallet_not_deleted": "❌ មិនមានកាបូបណាដែលអាចលុបបាន។",
    "wallet_refreshed": "🔄 សមតុល្យត្រូវបានធ្វើបច្ចុប្បន្នភាព៖\nឈ្មោះ: {name}\nសោសាធារណៈ: {pub}\nសមតុល្យ: {bal} SOL",
    "guide_create_wallet": (
        "📝 <b>របៀបបង្កើតកាបូប:</b>\n"
        "1️⃣ ជ្រើសប្រភេទកាបូប (SOL ឬ USDT)\n"
        "2️⃣ បញ្ចូលឈ្មោះតែមួយសម្រាប់កាបូប\n"
        "3️⃣ នឹងបង្កើតសោសាធារណៈ និងសោឯកជន\n"
        "4️⃣ ប្រើសោសាធារណៈដើម្បីទទួលប្រាក់\n\n"
        "💡 គន្លឹះ៖ រក្សាសោឯកជនឲ្យមានសុវត្ថិភាព និងកុំចែករំលែក។"
    ),
    "guide_delete_wallet": (
        "⚠️ <b>សេចក្តីជូនដំណឹងសំខាន់៖</b>\n"
        "ការលុបកាបូបគឺមិនអាចត្រឡប់វិញបានទេ។ សូមធ្វើការផ្ទេរទុនចេញមុនពេលលុប។"
    ),
    "no_wallets": "អ្នកមិនទាន់មានកាបូបណាមួយទេ។",
    "select_wallet": "សូមជ្រើសកាបូបដើម្បីមើលប្រវត្តិប្រតិបត្តិការ៖",
    "wallet_details": "**ឈ្មោះកាបូប៖** {name} \n\n **អាសយដ្ឋានសាធារណៈ៖** {public_key}",
    "wallet_not_found": "រកមិនឃើញកាបូប។",
    "back_button": "⬅️ ថយក្រោយ",
    "sol_wallets_header": "<b>កាបូប SOL របស់អ្នក:</b>\n",
    "wallet_balance": "<b>ឈ្មោះ:</b> {name}, <b>សមតុល្យ:</b> {balance} SOL\n",
    "wallet_error": "<b>ឈ្មោះ:</b> {name}, <b>បញ្ហា:</b> {error}\n",
    "no_sol_wallets": "អ្នកមិនទាន់មានកាបូប SOL ទេ។",
    "no_usdt_wallets": "អ្នកមិនទាន់មានកាបូប USDT ទេ។"
}

}
