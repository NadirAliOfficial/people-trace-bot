CASE_CONSTANT = {
    "en": {
        # Existing Constants
        "create_case_title": "Create New Case",
        "enter_name": "Enter your name:",
        "disclaimer_2": (
            "Disclaimer 2:\n\n"
            "1. The reward amount will be held in escrow until the case is resolved.\n"
            "2. Misuse of this service is prohibited.\n"
            "3. All information provided will be publicly visible.\n\n"
            "Do you agree?"
        ),
        "enter_person_name": "Enter the name of the person you're looking for:",
        "relationship": "What is your relationship to the person? (e.g., Friend, Family, Partner, etc.):",
        "upload_photo": "Upload a clear photo of the person (max. 5 MB):",
        "last_seen_location": "Where was the last seen location of this person?",
        "sex": "What is the person's gender? (Male/Female):",
        "age": "What is the person's age?",
        "hair_color": "What is the person's hair color? (e.g., Blonde, Brown, etc.):",
        "eye_color": "What is the person's eye color? (e.g., Blue, Green, etc.):",
        "height": "What is the person's height (cm):",
        "weight": "What is the person's weight (kg):",
        "distinctive_features": "What are the person's distinctive physical features? (e.g., Tattoo of eagle):",
        "reason_for_finding": "Why are you looking for this person?",
        "enter_reward_amount_sol": "Please enter the reward amount in SOL.",
        "enter_reward_amount_usdt": "Please enter the reward amount in USDT.",
        "enter_reward_amount_unknown": "Please enter the reward amount (unknown wallet type).",
        "insufficient_balance": "Your balance is insufficient. You have {0} available.",
        "refresh_wallet_balance": "Please refresh your wallet balance.",
        "reward_amount_confirmed": "Your reward amount of {0} has been confirmed.",
        "insufficient_balance_for_transfer": "You don't have enough balance to transfer. Your balance is {0}.",
        "transfer_successful": "The transfer was successful.",
        "transfer_failed": "The transfer failed. Please try again.",
        "transfer_error": "An error occurred while processing the transfer. Please try again.",
        "transfer_canceled": "The transfer has been canceled.",
        "invalid_confirmation": "Invalid response. Please confirm with 'yes' or 'no'.",
        "enter_reason_for_finding": "Please provide the reason for finding.",
        "case_submitted": "Your case has been submitted successfully.",
        "case_completed": "Your case has been completed.",
        "reward_amount_negative": "The reward amount cannot be negative.",
        "male_option": "♂ Male",
        "female_option": "♀ Female",
        "other_option": "Other",

        # Newly Added Constants
        "choose_existing_mobile": "Please select an existing number or add a new one.",
        "enter_mobile": "Enter your mobile number (TAC will be sent here):",
        "enter_valid_mobile": "❌ Invalid mobile number. Please enter a valid 10-digit number.",
        "tac_verified": "✅ TAC verified successfully.",
        "tac_invalid": "❌ Invalid TAC. Please try again.",
        "no_photo_found": "No photo found. Please upload a valid image file.",
        "case_not_found": "Case not found. Please try again.",
        "wallet_create_err": "An error occurred while creating the wallet. Please try again.",
        "wallet_name_prompt": "Please enter a name for your {wallet_type} wallet:",
        "wallet_name_empty": "Wallet name cannot be empty. Please try again.",
        "wallet_name_exists": "A wallet with this name already exists. Please choose a different name.",
        "wallet_create_details": (
            "✅ Wallet Created!\n"
            "Name: {name}\n"
            "Public Key: <code>{public_key}</code>\n"
            "Balance: {balance} {wallet_type}\n\n"
        ),
        "transfer_instructions": (
            "\n\n<b>How to Transfer {wallet_type} to Your Wallet:</b>\n\n"
            "1️⃣ Open your {wallet_type} wallet app or any compatible wallet.\n"
            "2️⃣ Go to the <b>Send</b> or <b>Transfer</b> section of the wallet.\n"
            "3️⃣ Paste your <b>Public Key</b> into the recipient address field. Your public key is:\n"
            "<code>{public_key}</code>\n\n"
            "4️⃣ Enter the amount of {wallet_type} you want to transfer.\n"
            "5️⃣ Review the transaction details and confirm the transfer.\n\n"
            "Once the transfer is successful, the {wallet_type} will appear in your wallet balance."
        ),
    },
    "zh": {
        # Existing Constants
        "create_case_title": "创建新案件",
        "enter_name": "请输入您的姓名：",
        "disclaimer_2": (
            "免责声明 2:\n\n"
            "1. 赏金金额将托管至案件解决。\n"
            "2. 禁止滥用本服务。\n"
            "3. 提供的所有信息将公开可见。\n\n"
            "您是否同意？"
        ),
        "enter_person_name": "请输入您要寻找的人的姓名：",
        "relationship": "您与该人的关系：",
        "upload_photo": "上传清晰的人物照片：",
        "last_seen_location": "请输入最后出现的位置（省份）：",
        "sex": "性别（男/女）：",
        "age": "年龄：",
        "hair_color": "发色：",
        "eye_color": "眼睛颜色：",
        "height": "身高（厘米）：",
        "weight": "体重（公斤）：",
        "distinctive_features": "显著的身体特征（例如，鹰形纹身）：",
        "reason_for_finding": "寻找原因：",
        "enter_reward_amount_sol": "请输入以SOL为单位的奖励金额。",
        "enter_reward_amount_usdt": "请输入以USDT为单位的奖励金额。",
        "enter_reward_amount_unknown": "请输入奖励金额（未知钱包类型）。",
        "insufficient_balance": "您的余额不足。您当前余额为{0}。",
        "refresh_wallet_balance": "请刷新您的钱包余额。",
        "reward_amount_confirmed": "您的奖励金额{0}已确认。",
        "insufficient_balance_for_transfer": "您的余额不足以转账。您当前余额为{0}。",
        "transfer_successful": "转账成功。",
        "transfer_failed": "转账失败，请重试。",
        "transfer_error": "处理转账时发生错误，请重试。",
        "transfer_canceled": "转账已取消。",
        "invalid_confirmation": "无效的回复，请输入 'yes' 或 'no' 进行确认。",
        "enter_reason_for_finding": "请提供寻找的原因。",
        "case_submitted": "您的案件已成功提交。",
        "case_completed": "您的案件已完成。",
        "reward_amount_negative": "奖励金额不能为负。",
        "male_option": "♂ 男",
        "female_option": "♀ 女",
        "other_option": "其他",

        # Newly Added Constants
        "choose_existing_mobile": "请选择一个已有的号码或添加一个新的号码。",
        "enter_mobile": "请输入您的手机号码（验证码将发送至此号码）：",
        "enter_valid_mobile": "❌ 无效的手机号码。请输入有效的10位数字。",
        "tac_verified": "✅ 验证码验证成功。",
        "tac_invalid": "❌ 无效的验证码。请重试。",
        "no_photo_found": "未找到照片。请上传有效的图片文件。",
        "case_not_found": "未找到案件。请重试。",
        "wallet_create_err": "创建钱包时发生错误。请重试。",
        "wallet_name_prompt": "请为您的 {wallet_type} 钱包输入名称：",
        "wallet_name_empty": "钱包名称不能为空。请重试。",
        "wallet_name_exists": "该名称的钱包已存在，请选择其他名称。",
        "wallet_create_details": (
            "✅ 钱包已创建！\n"
            "名称: {name}\n"
            "公钥: <code>{public_key}</code>\n"
            "余额: {balance} {wallet_type}\n\n"
        ),
        "transfer_instructions": (
            "\n\n<b>如何将 {wallet_type} 转入您的钱包：</b>\n\n"
            "1️⃣ 打开您的 {wallet_type} 钱包应用或兼容的钱包。\n"
            "2️⃣ 进入钱包的 <b>发送</b> 或 <b>转账</b> 部分。\n"
            "3️⃣ 将您的 <b>公钥</b> 粘贴到收款地址栏。您的公钥是：\n"
            "<code>{public_key}</code>\n\n"
            "4️⃣ 输入您要转账的 {wallet_type} 数量。\n"
            "5️⃣ 检查交易详情并确认转账。\n\n"
            "转账成功后，{wallet_type} 将显示在您的钱包余额中。"
        ),
    },
    "ms": {
        # Existing Constants
        "create_case_title": "Buat Kes Baharu",
        "enter_name": "Masukkan nama anda:",
        "disclaimer_2": (
            "Penafian 2:\n\n"
            "1. Jumlah ganjaran akan ditahan dalam escrow sehingga kes diselesaikan.\n"
            "2. Penyalahgunaan perkhidmatan ini adalah dilarang.\n"
            "3. Semua maklumat yang diberikan akan dapat dilihat oleh umum.\n\n"
            "Adakah anda bersetuju?"
        ),
        "enter_person_name": "Masukkan nama orang yang anda cari:",
        "relationship": "Apakah hubungan anda dengan orang itu? (cth: Rakan, Keluarga, Pasangan, dsb.):",
        "upload_photo": "Muat naik gambar jelas orang itu (maks. 5 MB):",
        "last_seen_location": "Di manakah lokasi terakhir orang ini dilihat?",
        "sex": "Apakah jantina orang itu? (Lelaki/Perempuan):",
        "age": "Apakah umur orang itu?",
        "hair_color": "Apakah warna rambut orang itu? (cth: Blonde, Perang, dll.):",
        "eye_color": "Apakah warna mata orang itu? (cth: Biru, Hijau, dll.):",
        "height": "Apakah ketinggian orang itu (cm):",
        "weight": "Apakah berat orang itu (kg):",
        "distinctive_features": "Apakah ciri-ciri fizikal khas orang itu? (cth: Tatu burung helang):",
        "reason_for_finding": "Mengapa anda mencari orang ini?",
        "enter_reward_amount_sol": "Sila masukkan jumlah ganjaran dalam SOL.",
        "enter_reward_amount_usdt": "Sila masukkan jumlah ganjaran dalam USDT.",
        "enter_reward_amount_unknown": "Sila masukkan jumlah ganjaran (jenis dompet tidak diketahui).",
        "insufficient_balance": "Baki anda tidak mencukupi. Anda mempunyai {0} tersedia.",
        "refresh_wallet_balance": "Sila kemas kini bali dompet anda.",
        "reward_amount_confirmed": "Jumlah ganjaran anda sebanyak {0} telah disahkan.",
        "insufficient_balance_for_transfer": "Anda tidak mempunyai baki yang mencukupi untuk dipindahkan. Baki anda adalah {0}.",
        "transfer_successful": "Pemindahan berjaya.",
        "transfer_failed": "Pemindahan gagal. Sila cuba lagi.",
        "transfer_error": "Ralat berlaku semasa memproses pemindahan. Sila cuba lagi.",
        "transfer_canceled": "Pemindahan telah dibatalkan.",
        "invalid_confirmation": "Jawapan tidak sah. Sila sahkan dengan 'yes' atau 'no'.",
        "enter_reason_for_finding": "Sila berikan sebab mencari.",
        "case_submitted": "Kes anda telah berjaya dihantar.",
        "case_completed": "Kes anda telah selesai.",
        "reward_amount_negative": "Jumlah ganjaran tidak boleh negatif.",
        "male_option": "♂ Lelaki",
        "female_option": "♀ Perempuan",
        "other_option": "Lain-lain",

        # Newly Added Constants
        "choose_existing_mobile": "Sila pilih nombor sedia ada atau tambah nombor baru.",
        "enter_mobile": "Masukkan nombor telefon bimbit anda (TAC akan dihantar ke sini):",
        "enter_valid_mobile": "❌ Nombor telefon tidak sah. Sila masukkan nombor 10 digit yang sah.",
        "tac_verified": "✅ TAC disahkan dengan jayanya.",
        "tac_invalid": "❌ TAC tidak sah. Sila cuba lagi.",
        "no_photo_found": "Tiada gambar ditemui. Sila muat naik fail imej yang sah.",
        "case_not_found": "Kes tidak dijumpai. Sila cuba lagi.",
        "wallet_create_err": "Ralat berlaku semasa mencipta dompet. Sila cuba lagi.",
        "wallet_name_prompt": "Sila masukkan nama untuk dompet {wallet_type} anda:",
        "wallet_name_empty": "Nama dompet tidak boleh kosong. Sila cuba lagi.",
        "wallet_name_exists": "Dompet dengan nama ini sudah wujud. Sila pilih nama lain.",
        "wallet_create_details": (
            "✅ Dompet Dicipta!\n"
            "Nama: {name}\n"
            "Kunci Awam: <code>{public_key}</code>\n"
            "Baki: {balance} {wallet_type}\n\n"
        ),
        "transfer_instructions": (
            "\n\n<b>Cara Memindahkan {wallet_type} ke Dompet Anda:</b>\n\n"
            "1️⃣ Buka aplikasi dompet {wallet_type} anda atau mana-mana dompet serasi.\n"
            "2️⃣ Pergi ke bahagian <b>Hantar</b> atau <b>Pindah</b> dompet.\n"
            "3️⃣ Tampalkan <b>Kunci Awam</b> anda ke dalam medan alamat penerima. Kunci awam anda adalah:\n"
            "<code>{public_key}</code>\n\n"
            "4️⃣ Masukkan jumlah {wallet_type} yang ingin anda pindahkan.\n"
            "5️⃣ Semak butiran transaksi dan sahkan pemindahan.\n\n"
            "Setelah pemindahan berjaya, {wallet_type} akan muncul dalam baki dompet anda."
        ),
    },
}