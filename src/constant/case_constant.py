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
        "mobile_number_doesnt_exist": "The mobile number you entered does not exist. Please try again.",
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
        "enter_valid_height": "Please enter a valid height (cm).",
        "enter_valid_weight": "Please enter a valid weight (kg).",
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
        "transaction_failed": "❌ <b>Transfer Failed</b>\n\nSomething went wrong while processing the reward transfer. Please try again later.",
        "transfer_canceled": "❌ <b>Transfer Canceled</b>\n\nThe reward transfer has been canceled as per your request.",
        "invalid_choice": "⚠️ <b>Invalid Selection</b>\n\nPlease choose a valid option.",
        # Newly Added Constants
        "mobile_selected_with_tac": "The mobile number you entered has been verified. Please enter the verification code:",
        "choose_existing_mobile": "Please select an existing number or add a new one.",
        "enter_mobile": "Please enter your mobile number (with country code):",
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

    # Thai (ไทย)
    "th": {
        "create_case_title": "สร้างเคสใหม่",
        "enter_name": "กรุณากรอกชื่อของคุณ:",
        "disclaimer_2": (
            "ข้อปฏิเสธความรับผิดชอบ 2:\n\n"
            "1. จำนวนเงินรางวัลจะถูกกักไว้จนกว่าเคสจะได้รับการแก้ไข.\n"
            "2. ห้ามใช้งานบริการนี้ในทางที่ผิด.\n"
            "3. ข้อมูลทั้งหมดที่ให้มาจะสามารถมองเห็นได้โดยสาธารณะ.\n\n"
            "คุณยอมรับหรือไม่?"
        ),
        "enter_person_name": "กรุณากรอกชื่อบุคคลที่คุณกำลังตามหา:",
        "relationship": "คุณมีความสัมพันธ์อย่างไรกับบุคคลนี้? (เช่น เพื่อน, ครอบครัว, คู่สมรส เป็นต้น):",
        "upload_photo": "อัปโหลดรูปภาพที่ชัดเจน (สูงสุด 5 MB):",
        "last_seen_location": "สถานที่สุดท้ายที่พบบุคคลนี้อยู่ที่ใด?",
        "sex": "เพศของบุคคลนี้คืออะไร? (ชาย/หญิง):",
        "age": "อายุของบุคคลนี้คือเท่าไร?",
        "hair_color": "สีผมของบุคคลนี้คืออะไร? (เช่น สีบลอนด์, สีน้ำตาล เป็นต้น):",
        "eye_color": "สีตาของบุคคลนี้คืออะไร? (เช่น สีฟ้า, สีเขียว เป็นต้น):",
        "height": "ความสูงของบุคคลนี้ (ซม.):",
        "weight": "น้ำหนักของบุคคลนี้ (กก.):",
        "distinctive_features": "ลักษณะทางกายภาพที่เด่นชัดของบุคคลนี้คืออะไร? (เช่น ลายสักนกอินทรี เป็นต้น):",
        "reason_for_finding": "คุณกำลังตามหาคนนี้เพราะเหตุใด?",
        "enter_reward_amount_sol": "กรุณากรอกจำนวนเงินรางวัลเป็น SOL.",
        "enter_reward_amount_usdt": "กรุณากรอกจำนวนเงินรางวัลเป็น USDT.",
        "enter_reward_amount_unknown": "กรุณากรอกจำนวนเงินรางวัล (ประเภทกระเป๋าเงินไม่ทราบ):",
        "insufficient_balance": "ยอดคงเหลือไม่เพียงพอ คุณมียอดคงเหลือ {0}",
        "refresh_wallet_balance": "กรุณาอัปเดทยอดคงเหลือกระเป๋าเงินของคุณ",
        "reward_amount_confirmed": "จำนวนเงินรางวัลของคุณ {0} ได้รับการยืนยันแล้ว",
        "insufficient_balance_for_transfer": "ยอดคงเหลือไม่เพียงพอสำหรับการโอน เหลือยอดคงเหลือ {0}",
        "transfer_successful": "การทำรายการโอนสำเร็จ",
        "transfer_failed": "การทำรายการโอนล้มเหลว กรุณาลองอีกครั้ง",
        "transfer_error": "เกิดข้อผิดพลาดขณะดำเนินการโอน กรุณาลองอีกครั้ง",
        "transfer_canceled": "การทำรายการโอนถูกยกเลิก",
        "invalid_confirmation": "การตอบกลับไม่ถูกต้อง กรุณายืนยันด้วย 'yes' หรือ 'no'",
        "enter_reason_for_finding": "กรุณากรอกรายละเอียดเหตุผลในการตามหา",
        "case_submitted": "เคสของคุณได้ถูกส่งเรียบร้อยแล้ว",
        "case_completed": "เคสของคุณเสร็จสิ้นแล้ว",
        "reward_amount_negative": "จำนวนเงินรางวัลต้องไม่เป็นลบ",
        "male_option": "♂ ชาย",
        "female_option": "♀ หญิง",
        "other_option": "อื่น ๆ",
    },

    # Vietnamese (Tiếng Việt)
    "vi": {
        "create_case_title": "Tạo Hồ Sơ Mới",
        "enter_name": "Nhập tên của bạn:",
        "disclaimer_2": (
            "Tuyên bố từ chối trách nhiệm 2:\n\n"
            "1. Số tiền thưởng sẽ được giữ cho đến khi hồ sơ được giải quyết.\n"
            "2. Cấm sử dụng sai mục đích dịch vụ này.\n"
            "3. Tất cả thông tin cung cấp sẽ được công khai.\n\n"
            "Bạn có đồng ý không?"
        ),
        "enter_person_name": "Nhập tên người mà bạn đang tìm kiếm:",
        "relationship": "Mối quan hệ của bạn với người đó là gì? (Ví dụ: Bạn bè, Gia đình, Vợ/Chồng, v.v.):",
        "upload_photo": "Tải lên hình ảnh rõ ràng của người đó (tối đa 5MB):",
        "last_seen_location": "Địa điểm cuối cùng nhìn thấy người này ở đâu?",
        "sex": "Giới tính của người này? (Nam/Nữ):",
        "age": "Tuổi của người này?",
        "hair_color": "Màu tóc của người này? (Ví dụ: Vàng, Nâu, v.v.):",
        "eye_color": "Màu mắt của người này? (Ví dụ: Xanh dương, Xanh lá, v.v.):",
        "height": "Chiều cao của người này (cm):",
        "weight": "Cân nặng của người này (kg):",
        "distinctive_features": "Đặc điểm thể chất nổi bật của người này là gì? (Ví dụ: Hình xăm con đại bàng):",
        "reason_for_finding": "Lý do bạn đang tìm kiếm người này là gì?",
        "enter_reward_amount_sol": "Vui lòng nhập số tiền thưởng bằng SOL.",
        "enter_reward_amount_usdt": "Vui lòng nhập số tiền thưởng bằng USDT.",
        "enter_reward_amount_unknown": "Vui lòng nhập số tiền thưởng (loại ví chưa xác định).",
        "insufficient_balance": "Số dư của bạn không đủ. Bạn hiện có sẵn {0}.",
        "refresh_wallet_balance": "Vui lòng làm mới số dư ví của bạn.",
        "reward_amount_confirmed": "Số tiền thưởng {0} đã được xác nhận.",
        "insufficient_balance_for_transfer": "Bạn không có đủ số dư để chuyển. Số dư hiện tại là {0}.",
        "transfer_successful": "Giao dịch chuyển tiền thành công.",
        "transfer_failed": "Giao dịch chuyển tiền thất bại. Vui lòng thử lại.",
        "transfer_error": "Đã xảy ra lỗi trong quá trình xử lý giao dịch. Vui lòng thử lại.",
        "transfer_canceled": "Giao dịch chuyển tiền đã bị hủy.",
        "invalid_confirmation": "Phản hồi không hợp lệ. Vui lòng xác nhận bằng 'yes' hoặc 'no'.",
        "enter_reason_for_finding": "Vui lòng cung cấp lý do tìm kiếm.",
        "case_submitted": "Hồ sơ của bạn đã được gửi thành công.",
        "case_completed": "Hồ sơ của bạn đã hoàn tất.",
        "reward_amount_negative": "Số tiền thưởng không thể âm.",
        "male_option": "♂ Nam",
        "female_option": "♀ Nữ",
        "other_option": "Khác",
    },

    "ur": {
    "create_case_title": "نیا کیس بنائیں",
    "enter_name": "اپنا نام درج کریں:",
    "disclaimer_2": (
        "دستبرداری:\n\n"
        "1. انعامی رقم کیس کے حل ہونے تک محفوظ رہے گی۔\n"
        "2. اس سروس کا غلط استعمال ممنوع ہے۔\n"
        "3. فراہم کردہ تمام معلومات عوامی ہوں گی۔\n\n"
        "کیا آپ متفق ہیں؟"
    ),
    "enter_person_name": "اس شخص کا نام درج کریں جسے آپ تلاش کر رہے ہیں:",
    "relationship": "اس شخص سے آپ کا کیا رشتہ ہے؟ (مثلاً: دوست، خاندان، شریک حیات وغیرہ):",
    "upload_photo": "اس شخص کی واضح تصویر اپ لوڈ کریں (زیادہ سے زیادہ 5MB):",
    "last_seen_location": "اس شخص کو آخری بار کہاں دیکھا گیا تھا؟",
    "sex": "اس شخص کی جنس کیا ہے؟ (مرد/عورت):",
    "age": "اس شخص کی عمر کیا ہے؟",
    "hair_color": "اس شخص کے بالوں کا رنگ کیا ہے؟ (مثلاً: سنہری، بھورا وغیرہ):",
    "eye_color": "اس شخص کی آنکھوں کا رنگ کیا ہے؟ (مثلاً: نیلا، سبز وغیرہ):",
    "height": "اس شخص کا قد کیا ہے (سینٹی میٹر میں)؟",
    "weight": "اس شخص کا وزن کیا ہے (کلوگرام میں)؟",
    "distinctive_features": "اس شخص کی نمایاں جسمانی خصوصیات کیا ہیں؟ (مثلاً: عقاب کا ٹیٹو):",
    "reason_for_finding": "آپ اس شخص کو کیوں تلاش کر رہے ہیں؟",
    "enter_reward_amount_sol": "براہ کرم انعامی رقم SOL میں درج کریں۔",
    "enter_reward_amount_usdt": "براہ کرم انعامی رقم USDT میں درج کریں۔",
    "enter_reward_amount_unknown": "براہ کرم انعامی رقم درج کریں (والیٹ کی قسم نامعلوم ہے)۔",
    "insufficient_balance": "آپ کا بیلنس ناکافی ہے۔ آپ کے پاس فی الحال {0} دستیاب ہیں۔",
    "refresh_wallet_balance": "براہ کرم اپنے والیٹ کا بیلنس تازہ کریں۔",
    "reward_amount_confirmed": "انعامی رقم {0} کی تصدیق ہو گئی ہے۔",
    "insufficient_balance_for_transfer": "منتقلی کے لیے آپ کا بیلنس ناکافی ہے۔ موجودہ بیلنس: {0}۔",
    "transfer_successful": "رقم کی منتقلی کامیاب رہی۔",
    "transfer_failed": "رقم کی منتقلی ناکام ہوئی۔ براہ کرم دوبارہ کوشش کریں۔",
    "transfer_error": "منتقلی کے دوران ایک خرابی پیش آئی۔ براہ کرم دوبارہ کوشش کریں۔",
    "transfer_canceled": "رقم کی منتقلی منسوخ کر دی گئی ہے۔",
    "invalid_confirmation": "غلط ردعمل۔ براہ کرم 'ہاں' یا 'نہیں' سے تصدیق کریں۔",
    "enter_reason_for_finding": "براہ کرم تلاش کرنے کی وجہ فراہم کریں۔",
    "case_submitted": "آپ کا کیس کامیابی سے جمع کروا دیا گیا ہے۔",
    "case_completed": "آپ کا کیس مکمل ہو گیا ہے۔",
    "reward_amount_negative": "انعامی رقم منفی نہیں ہو سکتی۔",
    "male_option": "♂ مرد",
    "female_option": "♀ عورت",
    "other_option": "دیگر",
}
,"ja": {
    "create_case_title": "新しいケースを作成",
    "enter_name": "あなたの名前を入力してください：",
    "disclaimer_2": (
        "免責事項：\n\n"
        "1. 報奨金はケースが解決されるまで保留されます。\n"
        "2. このサービスの不正使用は禁止されています。\n"
        "3. 提供されたすべての情報は公開されます。\n\n"
        "同意しますか？"
    ),
    "enter_person_name": "探している人の名前を入力してください：",
    "relationship": "その人との関係は何ですか？（例：友人、家族、配偶者など）：",
    "upload_photo": "その人の明確な写真をアップロードしてください（最大5MB）：",
    "last_seen_location": "その人が最後に目撃された場所はどこですか？",
    "sex": "その人の性別は何ですか？（男性/女性）：",
    "age": "その人の年齢は？",
    "hair_color": "その人の髪の色は何ですか？（例：金、茶など）：",
    "eye_color": "その人の目の色は何ですか？（例：青、緑など）：",
    "height": "その人の身長は何cmですか？",
    "weight": "その人の体重は何kgですか？",
    "distinctive_features": "その人の際立った身体的特徴は何ですか？（例：鷲のタトゥー）：",
    "reason_for_finding": "その人を探している理由は何ですか？",
    "enter_reward_amount_sol": "報奨金の金額をSOLで入力してください。",
    "enter_reward_amount_usdt": "報奨金の金額をUSDTで入力してください。",
    "enter_reward_amount_unknown": "報奨金の金額を入力してください（ウォレットの種類が不明です）。",
    "insufficient_balance": "残高が不足しています。現在の残高は{0}です。",
    "refresh_wallet_balance": "ウォレットの残高を更新してください。",
    "reward_amount_confirmed": "報奨金{0}が確認されました。",
    "insufficient_balance_for_transfer": "送金するには残高が不足しています。現在の残高は{0}です。",
    "transfer_successful": "送金が成功しました。",
    "transfer_failed": "送金に失敗しました。再試行してください。",
    "transfer_error": "送金処理中にエラーが発生しました。再試行してください。",
    "transfer_canceled": "送金がキャンセルされました。",
    "invalid_confirmation": "無効な応答です。「はい」または「いいえ」で確認してください。",
    "enter_reason_for_finding": "探している理由を提供してください。",
    "case_submitted": "あなたのケースが正常に送信されました。",
    "case_completed": "あなたのケースは完了しました。",
    "reward_amount_negative": "報奨金は負の値にできません。",
    "male_option": "♂ 男性",
    "female_option": "♀ 女性",
    "other_option": "その他",
}
,"ko": {
    "create_case_title": "새 케이스 만들기",
    "enter_name": "이름을 입력하세요:",
    "disclaimer_2": (
        "면책 조항:\n\n"
        "1. 보상금은 케이스가 해결될 때까지 보류됩니다.\n"
        "2. 이 서비스를 악용하는 것은 금지되어 있습니다.\n"
        "3. 제공된 모든 정보는 공개됩니다.\n\n"
        "동의하십니까?"
    ),
    "enter_person_name": "찾고 있는 사람의 이름을 입력하세요:",
    "relationship": "그 사람과의 관계는 무엇인가요? (예: 친구, 가족, 배우자 등):",
    "upload_photo": "그 사람의 명확한 사진을 업로드하세요 (최대 5MB):",
    "last_seen_location": "그 사람을 마지막으로 본 위치는 어디인가요?",
    "sex": "그 사람의 성별은 무엇인가요? (남성/여성):",
    "age": "그 사람의 나이는 몇 살인가요?",
    "hair_color": "그 사람의 머리 색깔은 무엇인가요? (예: 금발, 갈색 등):",
    "eye_color": "그 사람의 눈 색깔은 무엇인가요? (예: 파랑, 초록 등):",
    "height": "그 사람의 키는 몇 cm인가요?",
    "weight": "그 사람의 몸무게는 몇 kg인가요?",
    "distinctive_features": "그 사람의 특징적인 외모나 신체 특징은 무엇인가요? (예: 독수리 타투):",
    "reason_for_finding": "그 사람을 찾는 이유는 무엇인가요?",
    "enter_reward_amount_sol": "보상금 액수를 SOL로 입력하세요.",
    "enter_reward_amount_usdt": "보상금 액수를 USDT로 입력하세요.",
    "enter_reward_amount_unknown": "보상금 액수를 입력하세요 (지갑 유형이 확인되지 않음).",
    "insufficient_balance": "잔액이 부족합니다. 현재 잔액: {0}",
    "refresh_wallet_balance": "지갑 잔액을 새로 고치세요.",
    "reward_amount_confirmed": "보상금 {0}이 확인되었습니다.",
    "insufficient_balance_for_transfer": "송금하기에 잔액이 부족합니다. 현재 잔액: {0}",
    "transfer_successful": "송금이 성공적으로 완료되었습니다.",
    "transfer_failed": "송금에 실패했습니다. 다시 시도하세요.",
    "transfer_error": "송금 중 오류가 발생했습니다. 다시 시도하세요.",
    "transfer_canceled": "송금이 취소되었습니다.",
    "invalid_confirmation": "잘못된 응답입니다. '예' 또는 '아니오'로 확인하세요.",
    "enter_reason_for_finding": "찾는 이유를 입력해주세요.",
    "case_submitted": "케이스가 성공적으로 제출되었습니다.",
    "case_completed": "케이스가 완료되었습니다.",
    "reward_amount_negative": "보상금은 음수일 수 없습니다.",
    "male_option": "♂ 남성",
    "female_option": "♀ 여성",
    "other_option": "기타",
}
,
"km": {
    "create_case_title": "បង្កើតករណីថ្មី",
    "enter_name": "សូមបញ្ចូលឈ្មោះរបស់អ្នក៖",
    "disclaimer_2": (
        "ការបដិសេធ:\n\n"
        "1. ប្រាក់រង្វាន់នឹងត្រូវរក្សាទុករហូតដល់ករណីត្រូវបានដោះស្រាយ។\n"
        "2. ការប្រើប្រាស់សេវានេះក្នុងបំណងអាក្រក់គឺជារឿងត្រូវហាម។\n"
        "3. ព័ត៌មានទាំងអស់ដែលបានផ្ដល់នឹងត្រូវបង្ហាញសាធារណៈ។\n\n"
        "តើអ្នកយល់ព្រមទេ?"
    ),
    "enter_person_name": "សូមបញ្ចូលឈ្មោះនៃបុគ្គលដែលអ្នកកំពុងស្វែងរក៖",
    "relationship": "អ្នកមានទំនាក់ទំនងយ៉ាងដូចម្ដេចជាមួយបុគ្គលនោះ? (ឧ. មិត្តភក្តិ, គ្រួសារ, ស្វាមីភរិយា):",
    "upload_photo": "សូមផ្ទុករូបថតច្បាស់ៗ (អតិបរមា 5MB) របស់បុគ្គលនោះឡើង៖",
    "last_seen_location": "ទីតាំងចុងក្រោយដែលអ្នកបានឃើញបុគ្គលនោះ៖",
    "sex": "ភេទរបស់បុគ្គលនោះ៖ (ប្រុស/ស្រី):",
    "age": "អាយុបុគ្គលនោះប៉ុន្មាន?",
    "hair_color": "ពណ៌សក់៖ (ឧ. ប្រផេះ ខ្មៅ ត្នោត):",
    "eye_color": "ពណ៌ភ្នែក៖ (ឧ. ខៀវ បៃតង):",
    "height": "កម្ពស់បុគ្គលនោះ (សង់ទីម៉ែត្រ):",
    "weight": "ទំងន់បុគ្គលនោះ (គីឡូក្រាម):",
    "distinctive_features": "លក្ខណៈពិសេសរបស់បុគ្គលនោះ (ឧ. ស្នាមសាក់):",
    "reason_for_finding": "មូលហេតុដែលអ្នកស្វែងរកបុគ្គលនោះ៖",
    "enter_reward_amount_sol": "សូមបញ្ចូលប្រាក់រង្វាន់ជា SOL:",
    "enter_reward_amount_usdt": "សូមបញ្ចូលប្រាក់រង្វាន់ជា USDT:",
    "enter_reward_amount_unknown": "សូមបញ្ចូលប្រាក់រង្វាន់ (ប្រភេទកាបូបមិនស្គាល់):",
    "insufficient_balance": "សមតុល្យមិនគ្រប់គ្រាន់។ សមតុល្យបច្ចុប្បន្ន: {0}",
    "refresh_wallet_balance": "សូមធ្វើបច្ចុប្បន្នភាពសមតុល្យកាបូបរបស់អ្នក។",
    "reward_amount_confirmed": "បានបញ្ជាក់ប្រាក់រង្វាន់ {0}។",
    "insufficient_balance_for_transfer": "សមតុល្យមិនគ្រប់គ្រាន់សម្រាប់ផ្ទេរ។ សមតុល្យបច្ចុប្បន្ន: {0}",
    "transfer_successful": "ការផ្ទេរប្រាក់បានជោគជ័យ។",
    "transfer_failed": "ការផ្ទេរបរាជ័យ។ សូមព្យាយាមម្តងទៀត។",
    "transfer_error": "មានបញ្ហាដេលការផ្ទេរប្រាក់។ សូមព្យាយាមឡើងវិញ។",
    "transfer_canceled": "ការផ្ទេរត្រូវបានបោះបង់។",
    "invalid_confirmation": "ការឆ្លើយតបមិនត្រឹមត្រូវ។ សូមឆ្លើយ 'បាទ' ឬ 'ទេ'។",
    "enter_reason_for_finding": "សូមបញ្ចូលមូលហេតុនៃការស្វែងរក។",
    "case_submitted": "ករណីរបស់អ្នកត្រូវបានដាក់ស្នើដោយជោគជ័យ។",
    "case_completed": "ករណីរបស់អ្នកបានបញ្ចប់។",
    "reward_amount_negative": "ប្រាក់រង្វាន់មិនអាចមានតម្លៃអវិជ្ជមានបានទេ។",
    "male_option": "♂ ប្រុស",
    "female_option": "♀ ស្រី",
    "other_option": "ផ្សេងទៀត",
}
,"km": {
    "create_case_title": "បង្កើតករណីថ្មី",
    "enter_name": "សូមបញ្ចូលឈ្មោះរបស់អ្នក៖",
    "disclaimer_2": (
        "ការបដិសេធ:\n\n"
        "1. ប្រាក់រង្វាន់នឹងត្រូវរក្សាទុករហូតដល់ករណីត្រូវបានដោះស្រាយ។\n"
        "2. ការប្រើប្រាស់សេវានេះក្នុងបំណងអាក្រក់គឺជារឿងត្រូវហាម។\n"
        "3. ព័ត៌មានទាំងអស់ដែលបានផ្ដល់នឹងត្រូវបង្ហាញសាធារណៈ។\n\n"
        "តើអ្នកយល់ព្រមទេ?"
    ),
    "enter_person_name": "សូមបញ្ចូលឈ្មោះនៃបុគ្គលដែលអ្នកកំពុងស្វែងរក៖",
    "relationship": "អ្នកមានទំនាក់ទំនងយ៉ាងដូចម្ដេចជាមួយបុគ្គលនោះ? (ឧ. មិត្តភក្តិ, គ្រួសារ, ស្វាមីភរិយា):",
    "upload_photo": "សូមផ្ទុករូបថតច្បាស់ៗ (អតិបរមា 5MB) របស់បុគ្គលនោះឡើង៖",
    "last_seen_location": "ទីតាំងចុងក្រោយដែលអ្នកបានឃើញបុគ្គលនោះ៖",
    "sex": "ភេទរបស់បុគ្គលនោះ៖ (ប្រុស/ស្រី):",
    "age": "អាយុបុគ្គលនោះប៉ុន្មាន?",
    "hair_color": "ពណ៌សក់៖ (ឧ. ប្រផេះ ខ្មៅ ត្នោត):",
    "eye_color": "ពណ៌ភ្នែក៖ (ឧ. ខៀវ បៃតង):",
    "height": "កម្ពស់បុគ្គលនោះ (សង់ទីម៉ែត្រ):",
    "weight": "ទំងន់បុគ្គលនោះ (គីឡូក្រាម):",
    "distinctive_features": "លក្ខណៈពិសេសរបស់បុគ្គលនោះ (ឧ. ស្នាមសាក់):",
    "reason_for_finding": "មូលហេតុដែលអ្នកស្វែងរកបុគ្គលនោះ៖",
    "enter_reward_amount_sol": "សូមបញ្ចូលប្រាក់រង្វាន់ជា SOL:",
    "enter_reward_amount_usdt": "សូមបញ្ចូលប្រាក់រង្វាន់ជា USDT:",
    "enter_reward_amount_unknown": "សូមបញ្ចូលប្រាក់រង្វាន់ (ប្រភេទកាបូបមិនស្គាល់):",
    "insufficient_balance": "សមតុល្យមិនគ្រប់គ្រាន់។ សមតុល្យបច្ចុប្បន្ន: {0}",
    "refresh_wallet_balance": "សូមធ្វើបច្ចុប្បន្នភាពសមតុល្យកាបូបរបស់អ្នក។",
    "reward_amount_confirmed": "បានបញ្ជាក់ប្រាក់រង្វាន់ {0}។",
    "insufficient_balance_for_transfer": "សមតុល្យមិនគ្រប់គ្រាន់សម្រាប់ផ្ទេរ។ សមតុល្យបច្ចុប្បន្ន: {0}",
    "transfer_successful": "ការផ្ទេរប្រាក់បានជោគជ័យ។",
    "transfer_failed": "ការផ្ទេរបរាជ័យ។ សូមព្យាយាមម្តងទៀត។",
    "transfer_error": "មានបញ្ហាដេលការផ្ទេរប្រាក់។ សូមព្យាយាមឡើងវិញ។",
    "transfer_canceled": "ការផ្ទេរត្រូវបានបោះបង់។",
    "invalid_confirmation": "ការឆ្លើយតបមិនត្រឹមត្រូវ។ សូមឆ្លើយ 'បាទ' ឬ 'ទេ'។",
    "enter_reason_for_finding": "សូមបញ្ចូលមូលហេតុនៃការស្វែងរក។",
    "case_submitted": "ករណីរបស់អ្នកត្រូវបានដាក់ស្នើដោយជោគជ័យ។",
    "case_completed": "ករណីរបស់អ្នកបានបញ្ចប់។",
    "reward_amount_negative": "ប្រាក់រង្វាន់មិនអាចមានតម្លៃអវិជ្ជមានបានទេ។",
    "male_option": "♂ ប្រុស",
    "female_option": "♀ ស្រី",
    "other_option": "ផ្សេងទៀត",
}
,"id": {
    "create_case_title": "Buat Kasus Baru",
    "enter_name": "Masukkan nama Anda:",
    "disclaimer_2": (
        "Penafian:\n\n"
        "1. Hadiah akan disimpan hingga kasus diselesaikan.\n"
        "2. Penyalahgunaan layanan ini dilarang.\n"
        "3. Semua informasi yang diberikan akan dipublikasikan.\n\n"
        "Apakah Anda setuju?"
    ),
    "enter_person_name": "Masukkan nama orang yang Anda cari:",
    "relationship": "Apa hubungan Anda dengan orang tersebut? (contoh: teman, keluarga, pasangan):",
    "upload_photo": "Unggah foto yang jelas dari orang tersebut (maksimal 5MB):",
    "last_seen_location": "Di mana terakhir kali orang tersebut terlihat?",
    "sex": "Jenis kelamin orang tersebut (pria/wanita):",
    "age": "Berapa usia orang tersebut?",
    "hair_color": "Apa warna rambutnya? (contoh: pirang, coklat):",
    "eye_color": "Apa warna matanya? (contoh: biru, hijau):",
    "height": "Tinggi badan (dalam cm):",
    "weight": "Berat badan (dalam kg):",
    "distinctive_features": "Ciri-ciri fisik yang mencolok? (contoh: tato elang):",
    "reason_for_finding": "Mengapa Anda mencari orang ini?",
    "enter_reward_amount_sol": "Masukkan jumlah hadiah dalam SOL.",
    "enter_reward_amount_usdt": "Masukkan jumlah hadiah dalam USDT.",
    "enter_reward_amount_unknown": "Masukkan jumlah hadiah (jenis dompet tidak diketahui).",
    "insufficient_balance": "Saldo Anda tidak mencukupi. Saldo saat ini: {0}",
    "refresh_wallet_balance": "Silakan segarkan saldo dompet Anda.",
    "reward_amount_confirmed": "Jumlah hadiah {0} telah dikonfirmasi.",
    "insufficient_balance_for_transfer": "Saldo tidak cukup untuk transfer. Saldo saat ini: {0}",
    "transfer_successful": "Transfer berhasil.",
    "transfer_failed": "Transfer gagal. Silakan coba lagi.",
    "transfer_error": "Terjadi kesalahan saat melakukan transfer. Silakan coba lagi.",
    "transfer_canceled": "Transfer telah dibatalkan.",
    "invalid_confirmation": "Respon tidak valid. Harap konfirmasi dengan 'ya' atau 'tidak'.",
    "enter_reason_for_finding": "Harap masukkan alasan pencarian.",
    "case_submitted": "Kasus Anda telah berhasil dikirim.",
    "case_completed": "Kasus Anda telah selesai.",
    "reward_amount_negative": "Jumlah hadiah tidak boleh negatif.",
    "male_option": "♂ Pria",
    "female_option": "♀ Wanita",
    "other_option": "Lainnya",
}

}