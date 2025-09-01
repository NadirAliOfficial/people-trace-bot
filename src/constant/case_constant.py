CASE_CONSTANT = {
    "english": {
        "case_poster_disclaimer": (
            "📜 *Before You Continue – Please Read Carefully*\n\n"
            "By posting a case on PeopleTrace, you agree to the following:\n\n"
            "• 🧾 All information must be accurate and honest\n"
            "• 🚫 This platform must not be used to harass, stalk, or harm others\n"
            "• 🕵️‍♂️ Use is strictly for locating people lawfully\n"
            "• 📍 You must report the case to local authorities first\n"
            "• 🔍 All case details will be publicly visible\n"
            "• 💰 Rewards are held in escrow until verification\n"
            "• ⚠️ PeopleTrace is not liable for misuse or third-party consequences\n"
            "• ❗️False reports, offensive content, or illegal intent will lead to a permanent ban and legal action\n\n"
            "*Do you agree to these terms?*"
        ),
        "create_case_title": "Case Details",
        "enter_person_name": "👤 Enter the full name of the person you’re looking for:",
        "male_option": "♂ Male",
        "female_option": "♀ Female",
        "other_option": "Other",
        "gender": "⚧️ Gender:",
        "valid_age": "Please enter a valid number for age.",
        "age": "🎂 Age (or approximate):",
        "hair_color": "🧑 Hair color:",
        "eye_color": "👁️ Eye color:",
        "height": "📏 Height (in cm):",
        "weight": "⚖️ Weight (in kg)",
        "relationship": "🤝 What is your relationship to this person?",
        "upload_photo": "📸 Upload a clear, recent photo (Max 5MB):",
        "no_photo_found": "No photo found. Please upload a valid image file.",
        "enter_valid_height": "Please enter a valid height (cm).",
        "last_seen_location": "👕 What was this person last seen wearing? \n (Include clothing type, color, accessories, shoes, etc.)",
        "enter_valid_weight": "Please enter a valid weight (kg).",
        "distinctive_features": "🧷 Any distinctive physical features? (tattoos, scars, etc.)",
        "reason_for_finding": "❓ Why are you looking for this person?",
        "case_not_found": "Case not found. Please try again.",
        "enter_reward_amount": (
            "💰 <b>Reward Setup</b>\n\n"
            "What reward would you like to offer for verified leads? (in {type})"
        ),
        "reward_amount_negative": "❌ Reward amount must be greater than 0. You entered: {0}.",
        "insufficient_balance": "🚫 Insufficient Balance. You have only {0} available.",
        "refresh_wallet_balance": "🔄 Please refresh your wallet balance or lower the reward.",
        "reward_amount_confirmed": (
            "💸 Reward amount of {0} has been confirmed.\n\n"
            "🔒 Your wallet balance is being checked..."
        ),
        "insufficient_balance_for_transfer": (
            "🚫 <b>Insufficient Balance</b>\n\n"
            "Your wallet has only <b>{wallet_balance} {wallet_type}</b>.\n"
            "The reward amount is <b>{reward_amount} {wallet_type}</b>.\n"
            "Please ensure your wallet has enough balance to proceed."
        ),
        "congratulates_advertiser": (
            "🎉 <b>Congratulations!</b>\n\n"
            "Your reward of <b>{reward_amount} {wallet_type}</b> has been successfully transferred to our platform.\n\n"
            "📝 <b>Case Summary:</b>\n"
            "👤 <b>Case Name:</b> {case_name}\n"
            "📍 <b>Location:</b> {location}\n"
            "🎁 <b>Reward Offered:</b> {reward_amount} {wallet_type}\n"
            "💸 <b>Platform Fee (5%):</b> {platform_fee} {wallet_type}\n"
            "🔒 <b>Net Held in Escrow:</b> {net_amount} {wallet_type}\n\n"
            "🙌 We’ve lodged your case and the reward has been moved to the bot owner's wallet.\n"
            "🛡️ <b>Your reward is securely held in escrow</b> and will only be released upon verified, successful leads.\n\n"
            "🚀 Thank you for being part of our platform!"
        ),
        "owner_message": (
            "📢 <b>New Reward Transfer Completed</b>\n\n"
            "🆔 <b>User ID:</b> <code>{user_id}</code>\n"
            "📄 <b>Case ID:</b> <code>{case.id}</code>\n"
            "💰 <b>Amount:</b> {reward_amount} {wallet_type}\n"
            "🔐 <b>Wallet:</b> <code>{wallet.public_key}</code>\n"
            "🏷️ <b>Wallet Name:</b> {wallet.name}\n\n"
            "✅ <b>Status:</b> Reward transferred successfully.\n"
            "🔍 Use /listing to view all active cases."
        ),
        "transaction_failed": "❌ <b>Transfer Failed</b>\n\nSomething went wrong while processing the reward transfer. Please try again later.",
        "transfer_failed": "The transfer failed. Please try again.",
        "transfer_canceled": "The transfer has been canceled.",
        "enter_reward_amount_unknown": "Please enter the reward amount (unknown wallet type).",
        "reward_amount_invalid": "❌ Please enter a valid numeric reward amount.",
        "finder_disclaimer": (
            "📜 Before You Continue – Please Read Carefully\n\n"
            "By participating as a Finder on PeopleTrace, you agree to the following:\n\n"
            "• 🔍 You will only use this platform to help locate missing persons lawfully\n"
            "• 📹 Leads must include verifiable evidence (photo/video)\n"
            "• 💬 Communication with posters must remain respectful and ethical\n"
            "• 🧾 Do not use false, AI-generated, or misleading content\n"
            "• 📍 You may be asked for additional clarification or location proof\n"
            "• 💸 5% platform fee is deducted from successful reward claims\n"
            "• 🚫 Misuse, extortion, or suspicious behavior will lead to a permanent ban and legal action\n"
            "• ❗️ We reserve the right to reject false or unverified claims\n\n"
            "Do you agree to these terms?"
        ),
        "enter_name": "Enter your name:",
        "reward_too_low_tip": (
            "💸 <b>Reward set to {amount} {type}</b>\n\n"
            "💡 <b>Tip:</b> The higher the reward, the more eyes you attract!\n"
            "Offering a generous reward motivates more people to join the search — "
            "increasing your chances of finding the person faster. 🕵️‍♂️💬\n"
            "A little extra can go a long way in rallying a powerful crowd behind your case."
        ),
        "cancel_edit_button": "❌ Cancel / Edit",
        "increase_reward_button": "💰 Increase Reward",
        "back_button": "🔙 Back",
        "enter_reward_amount_usdt": "Please enter the reward amount in USDT.",
        "transfer_successful": "The transfer was successful.",
        "transfer_error": "An error occurred while processing the transfer. Please try again.",
        "invalid_confirmation": "Invalid response. Please confirm with 'yes' or 'no'.",
        "enter_reason_for_finding": "Please provide the reason for finding.",
        "case_submitted": "Your case has been submitted successfully.",
        "case_completed": "Your case has been completed.",
        "choose_existing_mobile": "Please select an existing number or add a new one.",
        "tac_invalid": "❌ Invalid TAC. Please try again.",
        "wallet_name_empty": "Wallet name cannot be empty. Please try again.",
        "wallet_name_exists": "❌ A wallet with this name already exists. Please choose a different name.",
        "wallet_create_details": (
            "✅ Wallet Created!\n"
            "🧾 Name: {name}\n"
            "💰 Type: {wallet_type}\n"
            "🔐 Public Key: <code>{public_key}</code>\n"
            "🌐 Network: {network}\n"
        ),
        "mobile_number_doesnt_exist": "The mobile number you entered does not exist. Please try again.",
        "invalid_choice": "⚠️ <b>Invalid Choice</b>\n\nPlease select a valid option.",
        "mobile_selected_with_tac": "The mobile number you entered has been verified. Please enter the verification code:",
        "enter_valid_mobile": "❌ Invalid mobile number. Please enter a valid 10-digit number.",
        "wallet_create_err": "An error occurred while creating the wallet. Please try again.",
        "wallet_name_prompt": "Please enter a name for your {wallet_type} wallet:",
        "wallet_create_details_with_balance": (
            "✅ Wallet Created!\n"
            "🧾 Name: {name}\n"
            "💰 Type: {wallet_type}\n"
            "🔐 Public Key: <code>{public_key}</code>\n"
            "🌐 Network: {network}\n"
            "💵 Balance: {balance} {wallet_type}\n"
        ),
        "understood_and_agree": "✅ I Understand and Agree",
    },
    "chinese": {
        "case_poster_disclaimer": (
            "📜 *在您继续之前–请仔细阅读*\n\n"
            "在 PeopleTrace 上发布案件，即表示您同意以下条款：\n\n"
            "• 🧾 所有信息必须准确真实\n"
            "• 🚫 不得利用本平台骚扰、跟踪或伤害他人\n"
            "• 🕵️‍♂️ 仅限合法寻找失踪人员\n"
            "• 📍 您必须先向地方当局报案\n"
            "• 🔍 所有案件详情将公开可见\n"
            "• 💰 奖励金将托管至验证通过后发放\n"
            "• ⚠️ PeopleTrace 对滥用或第三方行为不承担责任\n"
            "• ❗️虚假报案、冒犯性内容或非法意图将导致永久封禁和法律诉讼\n\n"
            "*您是否同意以上条款？*"
        ),
        "create_case_title": "案件详情",
        "enter_person_name": "👤 请输入您要寻找的人的全名：",
        "male_option": "♂ 男性",
        "female_option": "♀ 女性",
        "other_option": "其他",
        "gender": "⚧️ 性别：",
        "valid_age": "请输入有效的年龄数字。",
        "age": "🎂 年龄（或大致年龄）：",
        "hair_color": "🧑 发色：",
        "eye_color": "👁️ 眼色：",
        "height": "📏 身高（厘米）：",
        "weight": "⚖️ 体重（公斤）",
        "relationship": "🤝 您与此人的关系是什么？",
        "upload_photo": "📸 上传一张清晰、近期的照片（最大 5MB）：",
        "no_photo_found": "未找到照片。请上传有效的图像文件。",
        "enter_valid_height": "请输入有效的身高（厘米）。",
        "last_seen_location": "👕 此人最后一次出现时穿着什么？ \n （包括衣物类型、颜色、配饰、鞋子等）",
        "enter_valid_weight": "请输入有效的体重（公斤）。",
        "distinctive_features": "🧷 是否有明显身体特征？（纹身、疤痕等）",
        "reason_for_finding": "❓ 您为何要寻找此人？",
        "case_not_found": "未找到案件。请再试一次。",
        "enter_reward_amount": (
            "💰 <b>设置奖励</b>\n\n"
            "您希望为已验证的线索提供多少奖励？（以 {type} 计算）"
        ),
        "reward_amount_negative": "❌ 奖励金额必须大于 0。您输入的是：{0}。",
        "insufficient_balance": "🚫 余额不足。您当前可用余额为 {0}。",
        "refresh_wallet_balance": "🔄 请刷新您的钱包余额或降低奖励金额。",
        "reward_amount_confirmed": (
            "💸 奖励金额 {0} 已确认。\n\n"
            "🔒 正在检查您的钱包余额..."
        ),
        "insufficient_balance_for_transfer": (
            "🚫 <b>余额不足</b>\n\n"
            "您的钱包只有 <b>{wallet_balance} {wallet_type}</b>。\n"
            "奖励金额为 <b>{reward_amount} {wallet_type}</b>。\n"
            "请确保您的钱包有足够余额以继续。"
        ),
        "congratulates_advertiser": (
            "🎉 <b>恭喜！</b>\n\n"
            "您的 <b>{reward_amount} {wallet_type}</b> 奖励已成功转入我们的平台。\n\n"
            "📝 <b>案件摘要：</b>\n"
            "👤 <b>案件名称：</b> {case_name}\n"
            "📍 <b>地点：</b> {location}\n"
            "🎁 <b>提供奖励：</b> {reward_amount} {wallet_type}\n"
            "💸 <b>平台费用 (5%)：</b> {platform_fee} {wallet_type}\n"
            "🔒 <b>托管净额：</b> {net_amount} {wallet_type}\n\n"
            "🙌 我们已受理您的案件，奖励已转至机器人所有者的钱包。\n"
            "🛡️ <b>您的奖励已安全托管</b>，只有在提供经验证的成功线索后才会发放。\n\n"
            "🚀 感谢您成为我们平台的一员！"
        ),
        "owner_message": (
            "📢 <b>新的奖励转移已完成</b>\n\n"
            "🆔 <b>用户 ID：</b> <code>{user_id}</code>\n"
            "📄 <b>案件 ID：</b> <code>{case.id}</code>\n"
            "💰 <b>金额：</b> {reward_amount} {wallet_type}\n"
            "🔐 <b>钱包：</b> <code>{wallet.public_key}</code>\n"
            "🏷️ <b>钱包名称：</b> {wallet.name}\n\n"
            "✅ <b>状态：</b> 奖励转移成功。\n"
            "🔍 使用 /listing 查看所有活动案件。"
        ),
        "transaction_failed": "❌ <b>转账失败</b>\n\n处理奖励转账时出现问题，请稍后再试。",
        "transfer_failed": "转账失败，请重试。",
        "transfer_canceled": "转账已取消。",
        "enter_reward_amount_unknown": "请输入赏金金额（未知钱包类型）。",
        "reward_amount_invalid": "❌ 请输入有效的数字奖励金额。",
        "finder_disclaimer": (
            "📜 *在您继续之前–请仔细阅读*\n\n"
            "作为 PeopleTrace 上的*查找者*，您同意以下内容：\n\n"
            "• 🔍 您只能合法使用此平台帮助寻找失踪人员\n"
            "• 📹 线索必须包含可验证的证据（照片/视频）\n"
            "• 💬 与发布者沟通时需保持尊重和道德\n"
            "• 🧾 不得使用虚假、AI生成或误导性内容\n"
            "• 📍 您可能需要提供额外说明或位置证明\n"
            "• 💸 成功领取奖励时将扣除 5% 平台费用\n"
            "• 🚫 滥用、勒索或可疑行为将导致永久封禁及法律行动\n"
            "• ❗ 我们保留拒绝虚假或未经核实声明的权利\n\n"
            "*您是否同意以上条款？*"
        ),
        "enter_name": "请输入您的姓名：",
        "reward_too_low_tip": (
            "💸 <b>奖励设置为 {amount} {type}</b>\n\n"
            "💡 <b>提示：</b> 奖励越高，吸引的关注就越多！\n"
            "提供丰厚的奖励能激励更多人加入搜索 — "
            "增加您更快找到目标的机会。🕵️‍♂️💬\n"
            "一点额外的奖励就能为您的案件争取到强大的支持。"
        ),
        "cancel_edit_button": "❌ 取消 / 编辑",
        "increase_reward_button": "💰 增加奖励",
        "back_button": "🔙 返回",
        "enter_reward_amount_usdt": "请输入以 USDT 计算的赏金金额。",
        "transfer_successful": "转账成功。",
        "transfer_error": "处理转账时发生错误，请重试。",
        "invalid_confirmation": "无效响应。请用 '是' 或 '否' 回复。",
        "enter_reason_for_finding": "请输入寻找原因。",
        "case_submitted": "您的案件已成功提交。",
        "case_completed": "您的案件已完成。",
        "choose_existing_mobile": "请选择现有号码或添加新号码。",
        "tac_invalid": "❌ 验证码无效。请再试一次。",
        "wallet_name_empty": "钱包名称不能为空。请再试一次。",
        "wallet_name_exists": "❌ 同名钱包已存在。请选择其他名称。",
        "wallet_create_details": (
            "✅ 钱包已创建！\n"
            "🧾 名称: {name}\n"
            "💰 类型: {wallet_type}\n"
            "🔐 公钥: <code>{public_key}</code>\n"
            "🌐 网络: {network}\n"
        ),
        "mobile_number_doesnt_exist": "您输入的手机号码不存在。请再试一次。",
        "invalid_choice": "⚠️ <b>无效选择</b>\n\n请选择有效选项。",
        "mobile_selected_with_tac": "您输入的手机号码已验证。请输入验证码：",
        "enter_valid_mobile": "❌ 无效手机号码。请输入一个有效的10位数字。",
        "wallet_create_err": "创建钱包时出错。请再试一次。",
        "wallet_name_prompt": "请输入您的 {wallet_type} 钱包名称：",
        "wallet_create_details_with_balance": (
            "✅ 钱包已创建！\n"
            "🧾 名称: {name}\n"
            "💰 类型: {wallet_type}\n"
            "🔐 公钥: <code>{public_key}</code>\n"
            "🌐 网络: {network}\n"
            "💵 余额: {balance} {wallet_type}\n"
        ),
        "understood_and_agree": "✅ 我理解并同意",
    },
    "urdu": {
        "case_poster_disclaimer": (
            "📜 *جاری رکھنے سے پہلے – براہ کرم غور سے پڑھیں*\n\n"
            "PeopleTrace پر کیس پوسٹ کرکے، آپ مندرجہ ذیل پر متفق ہیں:\n\n"
            "• 🧾 تمام معلومات درست اور ایماندارانہ ہونی چاہئیں\n"
            "• 🚫 اس پلیٹ فارم کو کسی کو ہراساں کرنے، پیچھا کرنے، یا نقصان پہنچانے کے لیے استعمال نہیں کیا جانا چاہیے\n"
            "• 🕵️‍♂️ استعمال صرف قانونی طور پر لوگوں کو تلاش کرنے کے لیے ہے\n"
            "• 📍 آپ کو پہلے مقامی حکام کو کیس کی اطلاع دینی ہوگی\n"
            "• 🔍 کیس کی تمام تفصیلات عوامی طور پر نظر آئیں گی\n"
            "• 💰 انعامات تصدیق تک ایسکرو میں رکھے جاتے ہیں\n"

            "• ⚠️ PeopleTrace غلط استعمال یا تیسرے فریق کے نتائج کے لیے ذمہ دار نہیں ہے\n"
            "• ❗️جھوٹی رپورٹس، جارحانہ مواد، یا غیر قانونی ارادے کی صورت میں مستقل پابندی اور قانونی کارروائی کی جائے گی\n\n"
            "*کیا آپ ان شرائط سے متفق ہیں؟*"
        ),
        "create_case_title": "کیس کی تفصیلات",
        "enter_person_name": "👤 اس شخص کا پورا نام درج کریں جسے آپ تلاش کر رہے ہیں:",
        "male_option": "♂ مرد",
        "female_option": "♀ عورت",
        "other_option": "دیگر",
        "gender": "⚧️ جنس:",
        "valid_age": "براہ کرم عمر کے لیے ایک درست نمبر درج کریں۔",
        "age": "🎂 عمر (یا تخمینہ):",
        "hair_color": "🧑 بالوں کا رنگ:",
        "eye_color": "👁️ آنکھوں کا رنگ:",
        "height": "📏 قد (سینٹی میٹر میں):",
        "weight": "⚖️ وزن (کلوگرام میں)",
        "relationship": "🤝 آپ کا اس شخص سے کیا تعلق ہے؟",
        "upload_photo": "📸 ایک واضح، حالیہ تصویر اپ لوڈ کریں (زیادہ سے زیادہ 5MB):",
        "no_photo_found": "کوئی تصویر نہیں ملی۔ براہ کرم ایک درست تصویری فائل اپ لوڈ کریں۔",
        "enter_valid_height": "براہ کرم درست قد درج کریں (سینٹی میٹر میں)۔",
        "last_seen_location": "👕 اس شخص نے آخری بار کیا پہنا ہوا تھا؟ \n (لباس کی قسم، رنگ، لوازمات، جوتے وغیرہ شامل کریں)",
        "enter_valid_weight": "براہ کرم درست وزن درج کریں (کلوگرام میں)۔",
        "distinctive_features": "🧷 کوئی مخصوص جسمانی خصوصیات؟ (ٹیٹو، نشانات، وغیرہ)",
        "reason_for_finding": "❓ آپ اس شخص کو کیوں تلاش کر رہے ہیں؟",
        "case_not_found": "کیس نہیں ملا۔ براہ کرم دوبارہ کوشش کریں۔",
        "enter_reward_amount": (
            "💰 <b>انعام کا تعین</b>\n\n"
            "آپ تصدیق شدہ لیڈز کے لیے کیا انعام دینا چاہیں گے؟ ({type} میں)"
        ),
        "reward_amount_negative": "❌ انعام کی رقم 0 سے زیادہ ہونی چاہیے۔ آپ نے درج کیا: {0}۔",
        "insufficient_balance": "🚫 ناکافی بیلنس۔ آپ کے پاس صرف {0} دستیاب ہے۔",
        "refresh_wallet_balance": "🔄 براہ کرم اپنے والیٹ کا بیلنس تازہ کریں یا انعام کم کریں۔",
        "reward_amount_confirmed": (
            "💸 {0} کی انعامی رقم کی تصدیق ہو گئی ہے۔\n\n"
            "🔒 آپ کے والیٹ کا بیلنس چیک کیا جا رہا ہے..."
        ),
        "insufficient_balance_for_transfer": (
            "🚫 <b>ناکافی بیلنس</b>\n\n"
            "آپ کے والیٹ میں صرف <b>{wallet_balance} {wallet_type}</b> ہیں۔\n"
            "انعام کی رقم <b>{reward_amount} {wallet_type}</b> ہے۔\n"
            "براہ کرم یقینی بنائیں کہ آگے بڑھنے کے لیے آپ کے والیٹ میں کافی بیلنس ہے۔"
        ),
        "congratulates_advertiser": (
            "🎉 <b>مبارک ہو!</b>\n\n"
            "آپ کا <b>{reward_amount} {wallet_type}</b> کا انعام کامیابی کے ساتھ ہمارے پلیٹ فارم پر منتقل کر دیا گیا ہے۔\n\n"
            "📝 <b>کیس کا خلاصہ:</b>\n"
            "👤 <b>کیس کا نام:</b> {case_name}\n"
            "📍 <b>مقام:</b> {location}\n"
            "🎁 <b>پیش کردہ انعام:</b> {reward_amount} {wallet_type}\n"
            "💸 <b>پلیٹ فارم فیس (5%):</b> {platform_fee} {wallet_type}\n"
            "🔒 <b>ایسکرو میں رکھی گئی خالص رقم:</b> {net_amount} {wallet_type}\n\n"
            "🙌 ہم نے آپ کا کیس درج کر لیا ہے اور انعام بوٹ کے مالک کے والیٹ میں منتقل کر دیا گیا ہے۔\n"
            "🛡️ <b>آپ کا انعام محفوظ طریقے سے ایسکرو میں رکھا گیا ہے</b> اور صرف تصدیق شدہ، کامیاب لیڈز پر ہی جاری کیا جائے گا۔\n\n"
            "🚀 ہمارے پلیٹ فارم کا حصہ بننے کے لیے آپ کا شکریہ!"
        ),
        "owner_message": (
            "📢 <b>نیا انعام کی منتقلی مکمل ہو گئی</b>\n\n"
            "🆔 <b>صارف ID:</b> <code>{user_id}</code>\n"
            "📄 <b>کیس ID:</b> <code>{case.id}</code>\n"
            "💰 <b>رقم:</b> {reward_amount} {wallet_type}\n"
            "🔐 <b>والیٹ:</b> <code>{wallet.public_key}</code>\n"
            "🏷️ <b>والیٹ کا نام:</b> {wallet.name}\n\n"
            "✅ <b>حیثیت:</b> انعام کامیابی سے منتقل ہو گیا۔\n"
            "🔍 تمام فعال کیسز دیکھنے کے لیے /listing استعمال کریں۔"
        ),
        "transaction_failed": "❌ <b>منتقلی ناکام</b>\n\nانعام کی منتقلی پر کارروائی کے دوران کچھ غلط ہو گیا۔ براہ کرم بعد میں دوبارہ کوشش کریں۔",
        "transfer_failed": "منتقلی ناکام ہو گئی۔ براہ کرم دوبارہ کوشش کریں۔",
        "transfer_canceled": "منتقلی منسوخ کر دی گئی ہے۔",
        "enter_reward_amount_unknown": "براہ کرم انعامی رقم درج کریں (نامعلوم والیٹ قسم)۔",
        "reward_amount_invalid": "❌ براہ کرم ایک درست عددی انعامی رقم درج کریں۔",
        "finder_disclaimer": (
            "📜 جاری رکھنے سے پہلے – براہ کرم غور سے پڑھیں\n\n"
            "PeopleTrace پر ایک فائنڈر کے طور پر شرکت کرکے، آپ مندرجہ ذیل پر متفق ہیں:\n\n"
            "• 🔍 آپ اس پلیٹ فارم کو صرف قانونی طور پر لاپتہ افراد کو تلاش کرنے میں مدد کے لیے استعمال کریں گے\n"
            "• 📹 لیڈز میں قابل تصدیق ثبوت (تصویر/ویڈیو) شامل ہونا چاہیے\n"
            "• 💬 پوسٹرز کے ساتھ مواصلات احترام اور اخلاقیات پر مبنی ہونی چاہیے\n"
            "• 🧾 جھوٹے، AI سے تیار کردہ، یا گمراہ کن مواد کا استعمال نہ کریں\n"
            "• 📍 آپ سے اضافی وضاحت یا مقام کا ثبوت مانگا جا سکتا ہے\n"
            "• 💸 کامیاب انعامی دعووں سے 5% پلیٹ فارم فیس کاٹی جائے گی\n"
            "• 🚫 غلط استعمال، بھتہ خوری، یا مشکوک رویے کی صورت میں مستقل پابندی اور قانونی کارروائی کی جائے گی\n"
            "• ❗️ ہم جھوٹے یا غیر تصدیق شدہ دعووں کو مسترد کرنے کا حق محفوظ رکھتے ہیں\n\n"
            "کیا آپ ان شرائط سے متفق ہیں؟"
        ),
        "enter_name": "اپنا نام درج کریں:",
        "reward_too_low_tip": (
            "💸 <b>انعام {amount} {type} پر سیٹ کریں</b>\n\n"
            "💡 <b>مشورہ:</b> انعام جتنا زیادہ ہوگا، اتنی ہی زیادہ توجہ حاصل ہوگی!\n"
            "ایک فراخ انعام کی پیشکش زیادہ لوگوں کو تلاش میں شامل ہونے کی ترغیب دیتی ہے — "
            "شخص کو تیزی سے تلاش کرنے کے امکانات کو بڑھاتی ہے۔ 🕵️‍♂️💬\n"
            "تھوڑا سا اضافی آپ کے کیس کے پیچھے ایک طاقتور ہجوم کو جمع کرنے میں بہت مددگار ثابت ہوسکتا ہے۔"
        ),
        "cancel_edit_button": "❌ منسوخ / ترمیم کریں",
        "increase_reward_button": "💰 انعام میں اضافہ کریں",
        "back_button": "🔙 واپس",
        "enter_reward_amount_usdt": "براہ کرم USDT میں انعامی رقم درج کریں۔",
        "transfer_successful": "منتقلی کامیاب ہو گئی۔",
        "transfer_error": "منتقلی پر کارروائی کے دوران ایک خرابی پیش آئی۔ براہ کرم دوبارہ کوشش کریں۔",
        "invalid_confirmation": "غلط جواب۔ براہ کرم 'ہاں' یا 'نہیں' کے ساتھ تصدیق کریں۔",
        "enter_reason_for_finding": "براہ کرم تلاش کرنے کی وجہ فراہم کریں۔",
        "case_submitted": "آپ کا کیس کامیابی سے جمع کر دیا گیا ہے۔",
        "case_completed": "آپ کا کیس مکمل ہو گیا ہے۔",
        "choose_existing_mobile": "براہ کرم موجودہ نمبر کو منتخب کریں یا نیا نمبر شامل کریں۔",
        "tac_invalid": "❌ غلط TAC۔ براہ کرم دوبارہ کوشش کریں۔",
        "wallet_name_empty": "والیٹ کا نام خالی نہیں ہو سکتا۔ براہ کرم دوبارہ کوشش کریں۔",
        "wallet_name_exists": "❌ اس نام کا والیٹ پہلے سے موجود ہے۔ براہ کرم دوسرا نام منتخب کریں۔",
        "wallet_create_details": (
            "✅ والیٹ بنایا گیا!\n"
            "🧾 نام: {name}\n"
            "💰 قسم: {wallet_type}\n"
            "🔐 عوامی کلید: <code>{public_key}</code>\n"
            "🌐 نیٹ ورک: {network}\n"
        ),
        "mobile_number_doesnt_exist": "جو موبائل نمبر آپ نے درج کیا ہے وہ موجود نہیں ہے۔ براہ کرم دوبارہ کوشش کریں۔",
        "invalid_choice": "⚠️ <b>غلط انتخاب</b>\n\nبراہ کرم ایک درست آپشن منتخب کریں۔",
        "mobile_selected_with_tac": "موبائل نمبر جو آپ نے درج کیا ہے وہ تصدیق شدہ ہے۔ براہ کرم تصدیقی کوڈ درج کریں:",
        "enter_valid_mobile": "❌ غلط موبائل نمبر۔ براہ کرم درست 10 ہندسی نمبر درج کریں۔",
        "wallet_create_err": "والیٹ بنانے کے دوران کچھ خرابی۔ براہ کرم دوبارہ کوشش کریں۔",
        "wallet_name_prompt": "براہ کرم اپنے {wallet_type} والیٹ کے لیے نام درج کریں:",
        "wallet_create_details_with_balance": (
            "✅ والیٹ بنایا گیا!\n"
            "🧾 نام: {name}\n"
            "💰 قسم: {wallet_type}\n"
            "🔐 عوامی کلید: <code>{public_key}</code>\n"
            "🌐 نیٹ ورک: {network}\n"
            "💵 بیلنس: {balance} {wallet_type}\n"
        ),
        "understood_and_agree": "✅ میں سمجھتا ہوں اور متفق ہوں",
    },
    "japanese": {
        "case_poster_disclaimer": (
            "📜 *続行する前に – よくお読みください*\n\n"
            "PeopleTraceにケースを投稿することにより、以下のことに同意したことになります：\n\n"
            "• 🧾 すべての情報は正確かつ正直でなければなりません\n"
            "• 🚫 このプラットフォームを嫌がらせ、ストーカー行為、または他人に危害を加えるために使用してはなりません\n"
            "• 🕵️‍♂️ 合法的な人物捜索にのみ使用されます\n"
            "• 📍 まず地方当局に事件を報告しなければなりません\n"
            "• 🔍 すべてのケース詳細は公開されます\n"
            "• 💰 報酬は確認されるまでエスクローに保持されます\n"
            "• ⚠️ PeopleTraceは誤用または第三者の結果に対して責任を負いません\n"
            "• ❗️虚偽の報告、不快なコンテンツ、または違法な意図は、永久的な追放と法的措置につながります\n\n"
            "*これらの条件に同意しますか？*"
        ),
        "create_case_title": "ケース詳細",
        "enter_person_name": "👤 探している人のフルネームを入力してください：",
        "male_option": "♂ 男性",
        "female_option": "♀ 女性",
        "other_option": "その他",
        "gender": "⚧️ 性別：",
        "valid_age": "有効な年齢を数字で入力してください。",
        "age": "🎂 年齢（またはおおよその年齢）：",
        "hair_color": "🧑 髪の色：",
        "eye_color": "👁️ 目の色：",
        "height": "📏 身長（cm）：",
        "weight": "⚖️ 体重（kg）",
        "relationship": "🤝 あなたとこの人との関係は何ですか？",
        "upload_photo": "📸 鮮明で最近の写真をアップロードしてください（最大5MB）：",
        "no_photo_found": "写真が見つかりません。有効な画像ファイルをアップロードしてください。",
        "enter_valid_height": "有効な身長（cm）を入力してください。",
        "last_seen_location": "👕 この人が最後に見られたときに何を着ていましたか？ \n （服の種類、色、アクセサリー、靴などを含めてください）",
        "enter_valid_weight": "有効な体重（kg）を入力してください。",
        "distinctive_features": "🧷 何か特徴的な身体的特徴はありますか？（タトゥー、傷跡など）",
        "reason_for_finding": "❓ なぜこの人を探しているのですか？",
        "case_not_found": "ケースが見つかりません。もう一度お試しください。",
        "enter_reward_amount": (
            "💰 <b>報酬設定</b>\n\n"
            "確認済みのリードに対してどのくらいの報酬を提供しますか？（{type}で）"
        ),
        "reward_amount_negative": "❌ 報酬額は0より大きくなければなりません。入力したのは：{0}。",
        "insufficient_balance": "🚫 残高不足。利用可能なのは{0}のみです。",
        "refresh_wallet_balance": "🔄 ウォレットの残高を更新するか、報酬を下げてください。",
        "reward_amount_confirmed": (
            "💸 報酬額{0}が確認されました。\n\n"
            "🔒 ウォレットの残高を確認しています..."
        ),
        "insufficient_balance_for_transfer": (
            "🚫 <b>残高不足</b>\n\n"
            "あなたのウォレットには<b>{wallet_balance} {wallet_type}</b>しかありません。\n"
            "報酬額は<b>{reward_amount} {wallet_type}</b>です。\n"
            "続行するにはウォレットに十分な残高があることを確認してください。"
        ),
        "congratulates_advertiser": (
            "🎉 <b>おめでとうございます！</b>\n\n"
            "<b>{reward_amount} {wallet_type}</b>の報酬が当社のプラットフォームに正常に転送されました。\n\n"
            "📝 <b>ケース概要：</b>\n"
            "👤 <b>ケース名：</b> {case_name}\n"
            "📍 <b>場所：</b> {location}\n"
            "🎁 <b>提供報酬：</b> {reward_amount} {wallet_type}\n"
            "💸 <b>プラットフォーム手数料（5%）：</b> {platform_fee} {wallet_type}\n"
            "🔒 <b>エスクロー純額：</b> {net_amount} {wallet_type}\n\n"
            "🙌 ケースを提出し、報酬はボット所有者のウォレットに移動しました。\n"
            "🛡️ <b>報酬は安全にエスクローに保持され</b>、確認済みの成功したリードがあった場合にのみ解放されます。\n\n"
            "🚀 当社のプラットフォームにご参加いただきありがとうございます！"
        ),
        "owner_message": (
            "📢 <b>新しい報酬転送が完了しました</b>\n\n"
            "🆔 <b>ユーザーID：</b> <code>{user_id}</code>\n"
            "📄 <b>ケースID：</b> <code>{case.id}</code>\n"
            "💰 <b>金額：</b> {reward_amount} {wallet_type}\n"
            "🔐 <b>ウォレット：</b> <code>{wallet.public_key}</code>\n"
            "🏷️ <b>ウォレット名：</b> {wallet.name}\n\n"
            "✅ <b>ステータス：</b> 報酬は正常に転送されました。\n"
            "🔍 /listingを使用してすべてのアクティブなケースを表示します。"
        ),
        "transaction_failed": "❌ <b>転送失敗</b>\n\n報酬の転送処理中に問題が発生しました。後でもう一度お試しください。",
        "transfer_failed": "転送に失敗しました。もう一度お試しください。",
        "transfer_canceled": "転送はキャンセルされました。",
        "enter_reward_amount_unknown": "報酬額を入力してください（不明なウォレットタイプ）。",
        "reward_amount_invalid": "❌ 有効な数値の報酬額を入力してください。",
        "finder_disclaimer": (
            "📜 続行する前に – よくお読みください\n\n"
            "PeopleTraceのファインダーとして参加することにより、以下のことに同意したことになります：\n\n"
            "• 🔍 このプラットフォームを合法的な行方不明者の捜索にのみ使用します\n"
            "• 📹 リードには検証可能な証拠（写真/ビデオ）を含める必要があります\n"
            "• 💬 ポスターとのコミュニケーションは敬意を払い、倫理的でなければなりません\n"
            "• 🧾 虚偽、AI生成、または誤解を招くコンテンツを使用してはなりません\n"
            "• 📍 追加の説明や場所の証明を求められることがあります\n"
            "• 💸 成功した報酬請求から5%のプラットフォーム手数料が差し引かれます\n"
            "• 🚫 誤用、恐喝、または不審な行動は、永久的な追放と法的措置につながります\n"
            "• ❗️ 虚偽または未確認の請求を拒否する権利を留保します\n\n"
            "これらの条件に同意しますか？"
        ),
        "enter_name": "名前を入力してください：",
        "reward_too_low_tip": (
            "💸 <b>報酬は{amount} {type}に設定されています</b>\n\n"
            "💡 <b>ヒント：</b> 報酬が高いほど、より多くの注目を集めます！\n"
            "寛大な報酬を提供することで、より多くの人々が捜索に参加する動機付けになります — "
            "より早くその人を見つける可能性が高まります。🕵️‍♂️💬\n"
            "少しの追加が、あなたのケースの背後に強力な群衆を結集させるのに大いに役立ちます。"
        ),
        "cancel_edit_button": "❌ キャンセル / 編集",
        "increase_reward_button": "💰 報酬を増やす",
        "back_button": "🔙 戻る",
        "enter_reward_amount_usdt": "報酬額をUSDTで入力してください。",
        "transfer_successful": "転送は成功しました。",
        "transfer_error": "転送の処理中にエラーが発生しました。もう一度お試しください。",
        "invalid_confirmation": "無効な応答です。「はい」または「いいえ」で確認してください。",
        "enter_reason_for_finding": "探している理由を教えてください。",
        "case_submitted": "ケースは正常に送信されました。",
        "case_completed": "ケースは完了しました。",
        "choose_existing_mobile": "既存の番号を選択するか、新しい番号を追加してください。",
        "tac_invalid": "❌ 無効なTACです。もう一度お試しください。",
        "wallet_name_empty": "ウォレット名は空にできません。もう一度お試しください。",
        "wallet_name_exists": "❌ この名前のウォレットはすでに存在します。別の名前を選択してください。",
        "wallet_create_details": (
            "✅ ウォレットが作成されました！\n"
            "🧾 名前: {name}\n"
            "💰 タイプ: {wallet_type}\n"
            "🔐 公開鍵: <code>{public_key}</code>\n"
            "🌐 ネットワーク: {network}\n"
        ),
        "mobile_number_doesnt_exist": "入力した電話番号は存在しません。もう一度やり直してください。",
        "invalid_choice": "⚠️ <b>無効な選択</b>\n\n有効なオプションを選んでください。",
        "mobile_selected_with_tac": "入力した電話番号は検証済みです。認証コードを入力してください:",
        "enter_valid_mobile": "❌ 無効な電話番号です。正しい10桁の番号を入力してください。",
        "wallet_create_err": "ウォレット作成中にエラーが発生しました。再度お試しください。",
        "wallet_name_prompt": "{wallet_type} ウォレットの名前を入力してください:",
        "wallet_create_details_with_balance": (
            "✅ ウォレットが作成されました！\n"
            "🧾 名前: {name}\n"
            "💰 タイプ: {wallet_type}\n"
            "🔐 公開鍵: <code>{public_key}</code>\n"
            "🌐 ネットワーク: {network}\n"
            "💵 残高: {balance} {wallet_type}\n"
        ),
        "understood_and_agree": "✅ 理解し、同意します",
    },
    "korean": {
        "case_poster_disclaimer": (
            "📜 *계속하기 전에 – 주의 깊게 읽어주세요*\n\n"
            "PeopleTrace에 사례를 게시함으로써 다음 사항에 동의하게 됩니다:\n\n"
            "• 🧾 모든 정보는 정확하고 정직해야 합니다\n"
            "• 🚫 이 플랫폼을 타인을 괴롭히거나, 스토킹하거나, 해를 끼치는 데 사용해서는 안 됩니다\n"
            "• 🕵️‍♂️ 합법적인 인물 찾기에만 사용됩니다\n"
            "• 📍 먼저 지역 당국에 사건을 신고해야 합니다\n"
            "• 🔍 모든 사례 세부 정보는 공개됩니다\n"
            "• 💰 보상금은 확인될 때까지 에스크로에 보관됩니다\n"
            "• ⚠️ PeopleTrace는 오용 또는 제3자 결과에 대해 책임을 지지 않습니다\n"
            "• ❗️허위 보고, 불쾌한 콘텐츠 또는 불법적인 의도는 영구적인 차단 및 법적 조치로 이어질 것입니다\n\n"
            "*이 조건에 동의하십니까?*"
        ),
        "create_case_title": "사례 세부 정보",
        "enter_person_name": "👤 찾고 있는 사람의 전체 이름을 입력하세요:",
        "male_option": "♂ 남성",
        "female_option": "♀ 여성",
        "other_option": "기타",
        "gender": "⚧️ 성별:",
        "valid_age": "유효한 나이를 숫자로 입력하세요.",
        "age": "🎂 나이 (또는 대략적인 나이):",
        "hair_color": "🧑 머리 색깔:",
        "eye_color": "👁️ 눈 색깔:",
        "height": "📏 키 (cm):",
        "weight": "⚖️ 몸무게 (kg)",
        "relationship": "🤝 이 사람과의 관계는 무엇입니까?",
        "upload_photo": "📸 선명하고 최근 사진을 업로드하세요 (최대 5MB):",
        "no_photo_found": "사진을 찾을 수 없습니다. 유효한 이미지 파일을 업로드하세요.",
        "enter_valid_height": "유효한 키(cm)를 입력하세요.",
        "last_seen_location": "👕 이 사람이 마지막으로 목격되었을 때 무엇을 입고 있었나요? \n (의류 종류, 색상, 액세서리, 신발 등 포함)",
        "enter_valid_weight": "유효한 몸무게(kg)를 입력하세요.",
        "distinctive_features": "🧷 독특한 신체적 특징이 있나요? (문신, 흉터 등)",
        "reason_for_finding": "❓ 왜 이 사람을 찾고 있나요?",
        "case_not_found": "사례를 찾을 수 없습니다. 다시 시도하세요.",
        "enter_reward_amount": (
            "💰 <b>보상 설정</b>\n\n"
            "확인된 단서에 대해 어떤 보상을 제공하시겠습니까? ({type} 단위)"
        ),
        "reward_amount_negative": "❌ 보상액은 0보다 커야 합니다. 입력한 값: {0}.",
        "insufficient_balance": "🚫 잔액 부족. 사용 가능한 금액은 {0}뿐입니다.",
        "refresh_wallet_balance": "🔄 지갑 잔액을 새로고침하거나 보상액을 낮추세요.",
        "reward_amount_confirmed": (
            "💸 보상액 {0}이(가) 확인되었습니다.\n\n"
            "🔒 지갑 잔액을 확인 중입니다..."
        ),
        "insufficient_balance_for_transfer": (
            "🚫 <b>잔액 부족</b>\n\n"
            "지갑에 <b>{wallet_balance} {wallet_type}</b>만 있습니다.\n"
            "보상액은 <b>{reward_amount} {wallet_type}</b>입니다.\n"
            "진행하려면 지갑에 충분한 잔액이 있는지 확인하세요."
        ),
        "congratulates_advertiser": (
            "🎉 <b>축하합니다!</b>\n\n"
            "<b>{reward_amount} {wallet_type}</b>의 보상이 저희 플랫폼으로 성공적으로 이체되었습니다.\n\n"
            "📝 <b>사례 요약:</b>\n"
            "👤 <b>사례 이름:</b> {case_name}\n"
            "📍 <b>위치:</b> {location}\n"
            "🎁 <b>제공된 보상:</b> {reward_amount} {wallet_type}\n"
            "💸 <b>플랫폼 수수료 (5%):</b> {platform_fee} {wallet_type}\n"
            "🔒 <b>에스크로 순액:</b> {net_amount} {wallet_type}\n\n"
            "🙌 사례를 접수했으며 보상은 봇 소유자의 지갑으로 이동되었습니다.\n"
            "🛡️ <b>보상은 안전하게 에스크로에 보관되며</b>, 확인된 성공적인 단서가 있을 때만 지급됩니다.\n\n"
            "🚀 저희 플랫폼의 일원이 되어주셔서 감사합니다!"
        ),
        "owner_message": (
            "📢 <b>새로운 보상 이체가 완료되었습니다</b>\n\n"
            "🆔 <b>사용자 ID:</b> <code>{user_id}</code>\n"
            "📄 <b>사례 ID:</b> <code>{case.id}</code>\n"
            "💰 <b>금액:</b> {reward_amount} {wallet_type}\n"
            "🔐 <b>지갑:</b> <code>{wallet.public_key}</code>\n"
            "🏷️ <b>지갑 이름:</b> {wallet.name}\n\n"
            "✅ <b>상태:</b> 보상이 성공적으로 이체되었습니다.\n"
            "🔍 /listing을 사용하여 모든 활성 사례를 확인하세요."
        ),
        "transaction_failed": "❌ <b>이체 실패</b>\n\n보상 이체 처리 중 문제가 발생했습니다. 나중에 다시 시도하세요.",
        "transfer_failed": "이체에 실패했습니다. 다시 시도하세요.",
        "transfer_canceled": "이체가 취소되었습니다.",
        "enter_reward_amount_unknown": "보상액을 입력하세요 (알 수 없는 지갑 유형).",
        "reward_amount_invalid": "❌ 유효한 숫자 보상액을 입력하세요.",
        "finder_disclaimer": (
            "📜 계속하기 전에 – 주의 깊게 읽어주세요\n\n"
            "PeopleTrace의 파인더로 참여함으로써 다음 사항에 동의하게 됩니다:\n\n"
            "• 🔍 이 플랫폼을 합법적인 실종자 찾기에만 사용합니다\n"
            "• 📹 단서에는 검증 가능한 증거(사진/비디오)가 포함되어야 합니다\n"
            "• 💬 포스터와의 의사소통은 존중하고 윤리적이어야 합니다\n"
            "• 🧾 허위, AI 생성 또는 오해의 소지가 있는 콘텐츠를 사용하지 마십시오\n"
            "• 📍 추가 설명이나 위치 증명을 요청받을 수 있습니다\n"
            "• 💸 성공적인 보상 청구에서 5%의 플랫폼 수수료가 공제됩니다\n"
            "• 🚫 오용, 갈취 또는 의심스러운 행동은 영구적인 차단 및 법적 조치로 이어질 것입니다\n"
            "• ❗️ 허위 또는 미확인된 주장을 거부할 권리가 있습니다\n\n"
            "이 조건에 동의하십니까?"
        ),
        "enter_name": "이름을 입력하세요:",
        "reward_too_low_tip": (
            "💸 <b>보상은 {amount} {type}로 설정되었습니다</b>\n\n"
            "💡 <b>팁:</b> 보상이 높을수록 더 많은 관심을 끌 수 있습니다!\n"
            "관대한 보상을 제공하면 더 많은 사람들이 수색에 참여하도록 동기를 부여합니다 — "
            "그 사람을 더 빨리 찾을 가능성을 높입니다. 🕵️‍♂️💬\n"
            "약간의 추가 금액이 당신의 사건 뒤에 강력한 군중을 모으는 데 큰 도움이 될 수 있습니다."
        ),
        "cancel_edit_button": "❌ 취소 / 편집",
        "increase_reward_button": "💰 보상 늘리기",
        "back_button": "🔙 뒤로",
        "enter_reward_amount_usdt": "보상액을 USDT로 입력하세요.",
        "transfer_successful": "이체가 성공했습니다.",
        "transfer_error": "이체 처리 중 오류가 발생했습니다. 다시 시도하세요.",
        "invalid_confirmation": "잘못된 응답입니다. '예' 또는 '아니오'로 확인하세요.",
        "enter_reason_for_finding": "찾는 이유를 알려주세요.",
        "case_submitted": "사례가 성공적으로 제출되었습니다.",
        "case_completed": "사례가 완료되었습니다.",
        "choose_existing_mobile": "기존 번호를 선택하거나 새 번호를 추가하세요.",
        "tac_invalid": "❌ 잘못된 TAC입니다. 다시 시도하세요.",
        "wallet_name_empty": "지갑 이름은 비워둘 수 없습니다. 다시 시도하세요.",
        "wallet_name_exists": "❌ 이 이름의 지갑이 이미 존재합니다. 다른 이름을 선택하세요.",
        "wallet_create_details": (
            "✅ 지갑이 생성되었습니다!\n"
            "🧾 이름: {name}\n"
            "💰 유형: {wallet_type}\n"
            "🔐 공개 키: <code>{public_key}</code>\n"
            "🌐 네트워크: {network}\n"
        ),
        "mobile_number_doesnt_exist": "입력한 휴대전화 번호가 존재하지 않습니다. 다시 시도해 주세요.",
        "invalid_choice": "⚠️ <b>잘못된 선택</b>\n\n올바른 옵션을 선택해 주세요.",
        "mobile_selected_with_tac": "입력한 전화번호가 인증되었습니다. 인증 코드를 입력해 주세요:",
        "enter_valid_mobile": "❌ 유효하지 않은 휴대폰 번호입니다. 올바른 10자리 번호를 입력하세요.",
        "wallet_create_err": "지갑 생성 중 오류가 발생했습니다. 다시 시도해 주세요.",
        "wallet_name_prompt": "{wallet_type} 지갑 이름을 입력하세요:",
        "wallet_create_details_with_balance": (
            "✅ 지갑 생성 성공!\n"
            "🧾 이름: {name}\n"
            "💰 유형: {wallet_type}\n"
            "🔐 공개 키: <code>{public_key}</code>\n"
            "🌐 네트워크: {network}\n"
            "💵 잔액: {balance} {wallet_type}\n"
        ),
        "understood_and_agree": "✅ 이해하고 동의합니다",
    },
    "khmer": {
        "case_poster_disclaimer": (
            "📜 *មុនពេលអ្នកបន្ត – សូមអានដោយយកចិត្តទុកដាក់*\n\n"
            "តាមរយៈការបង្ហោះករណីនៅលើ PeopleTrace អ្នកយល់ព្រមនឹងចំណុចខាងក្រោម៖\n\n"
            "• 🧾 ព័ត៌មានទាំងអស់ត្រូវតែត្រឹមត្រូវ និងស្មោះត្រង់\n"
            "• 🚫 វេទិកានេះមិនត្រូវប្រើដើម្បីបៀតបៀន, តាមដាន, ឬធ្វើបាបអ្នកដទៃឡើយ\n"
            "• 🕵️‍♂️ ការប្រើប្រាស់គឺសម្រាប់តែការស្វែងរកមនុស្សដោយស្របច្បាប់ប៉ុណ្ណោះ\n"
            "• 📍 អ្នកត្រូវតែរាយការណ៍ករណីនេះទៅអាជ្ញាធរមូលដ្ឋានជាមុនសិន\n"
            "• 🔍 ពត៌មានលំអិតនៃករណីទាំងអស់នឹងត្រូវបានបង្ហាញជាសាធារណៈ\n"
            "• 💰 រង្វាន់នឹងត្រូវបានរក្សាទុកក្នុង escrow រហូតដល់ការផ្ទៀងផ្ទាត់\n"
            "• ⚠️ PeopleTrace មិនទទួលខុសត្រូវចំពោះការប្រើប្រាស់ខុស ឬផលវិបាកពីភាគីទីបីឡើយ\n"
            "• ❗️របាយការណ៍មិនពិត, ខ្លឹមសារប្រមាថ, ឬចេតនាខុសច្បាប់នឹងនាំឱ្យមានការហាមឃាត់ជាអចិន្ត្រៃយ៍ និងវិធានការផ្លូវច្បាប់\n\n"
            "*តើអ្នកយល់ព្រមនឹងលក្ខខណ្ឌទាំងនេះទេ?*"
        ),
        "create_case_title": "ពត៌មានលំអិតករណី",
        "enter_person_name": "👤 បញ្ចូលឈ្មោះពេញរបស់បុគ្គលដែលអ្នកកំពុងស្វែងរក៖",
        "male_option": "♂ បុរស",
        "female_option": "♀ ស្ត្រី",
        "other_option": "ផ្សេងៗ",
        "gender": "⚧️ ភេទ៖",
        "valid_age": "សូមបញ្ចូលលេខត្រឹមត្រូវសម្រាប់អាយុ។",
        "age": "🎂 អាយុ (ឬប្រហាក់ប្រហែល)៖",
        "hair_color": "🧑 ពណ៌សក់៖",
        "eye_color": "👁️ ពណ៌ភ្នែក៖",
        "height": "📏 កម្ពស់ (គិតជាសង់ទីម៉ែត្រ)៖",
        "weight": "⚖️ ទម្ងន់ (គិតជាគីឡូក្រាម)",
        "relationship": "🤝 តើអ្នកមានទំនាក់ទំនងអ្វីជាមួយបុគ្គលនេះ?",
        "upload_photo": "📸 បង្ហោះរូបថតថ្មីៗ និងច្បាស់ (ទំហំអតិបរមា 5MB)៖",
        "no_photo_found": "រកមិនឃើញរូបថតទេ។ សូមបង្ហោះឯកសាររូបភាពដែលត្រឹមត្រូវ។",
        "enter_valid_height": "សូមបញ្ចូលកម្ពស់ដែលត្រឹមត្រូវ (សង់ទីម៉ែត្រ)។",
        "last_seen_location": "👕 តើបុគ្គលនេះស្លៀកពាក់អ្វីនៅពេលឃើញចុងក្រោយ? \n (រួមបញ្ចូលប្រភេទសម្លៀកបំពាក់, ពណ៌, គ្រឿងអលង្ការ, ស្បែកជើង ។ល។)",
        "enter_valid_weight": "សូមបញ្ចូលទម្ងន់ដែលត្រឹមត្រូវ (គីឡូក្រាម)។",
        "distinctive_features": "🧷 តើមានលក្ខណៈពិសេសរាងកាយប្លែកៗអ្វីខ្លះ? (ស្នាមសាក់, ស្លាកស្នាម ។ល។)",
        "reason_for_finding": "❓ ហេតុអ្វីបានជាអ្នកស្វែងរកបុគ្គលនេះ?",
        "case_not_found": "រកមិនឃើញករណីទេ។ សូមព្យាយាមម្តងទៀត។",
        "enter_reward_amount": (
            "💰 <b>ការរៀបចំរង្វាន់</b>\n\n"
            "តើអ្នកចង់ផ្តល់រង្វាន់អ្វីសម្រាប់ព័ត៌មានដែលបានផ្ទៀងផ្ទាត់? (គិតជា {type})"
        ),
        "reward_amount_negative": "❌ ចំនួនរង្វាន់ត្រូវតែធំជាង 0។ អ្នកបានបញ្ចូល៖ {0}។",
        "insufficient_balance": "🚫 ទឹកប្រាក់មិនគ្រប់គ្រាន់។ អ្នកមានតែ {0} ប៉ុណ្ណោះ។",
        "refresh_wallet_balance": "🔄 សូមធ្វើបច្ចុប្បន្នភាពសមតុល្យកាបូបរបស់អ្នក ឬបន្ថយរង្វាន់។",
        "reward_amount_confirmed": (
            "💸 ចំនួនរង្វាន់ {0} ត្រូវបានបញ្ជាក់។\n\n"
            "🔒 កំពុងពិនិត្យសមតុល្យកាបូបរបស់អ្នក..."
        ),
        "insufficient_balance_for_transfer": (
            "🚫 <b>ទឹកប្រាក់មិនគ្រប់គ្រាន់</b>\n\n"
            "កាបូបរបស់អ្នកមានតែ <b>{wallet_balance} {wallet_type}</b> ប៉ុណ្ណោះ។\n"
            "ចំនួនរង្វាន់គឺ <b>{reward_amount} {wallet_type}</b>។\n"
            "សូមប្រាកដថាកាបូបរបស់អ្នកមានសមតុល្យគ្រប់គ្រាន់ដើម្បីបន្ត។"
        ),
        "congratulates_advertiser": (
            "🎉 <b>សូមអបអរសាទរ!</b>\n\n"
            "រង្វាន់របស់អ្នកចំនួន <b>{reward_amount} {wallet_type}</b> ត្រូវបានផ្ទេរទៅកាន់វេទិការបស់យើងដោយជោគជ័យ។\n\n"
            "📝 <b>សេចក្តីសង្ខេបករណី៖</b>\n"
            "👤 <b>ឈ្មោះករណី៖</b> {case_name}\n"
            "📍 <b>ទីតាំង៖</b> {location}\n"
            "🎁 <b>រង្វាន់ដែលផ្តល់ជូន៖</b> {reward_amount} {wallet_type}\n"
            "💸 <b>ថ្លៃសេវាវេទិកា (5%)៖</b> {platform_fee} {wallet_type}\n"
            "🔒 <b>ចំនួនទឹកប្រាក់សុទ្ធដែលរក្សាទុកក្នុង escrow៖</b> {net_amount} {wallet_type}\n\n"
            "🙌 យើងបានដាក់ពាក្យបណ្តឹងរបស់អ្នកហើយ ហើយរង្វាន់ត្រូវបានផ្ទេរទៅកាបូបរបស់ម្ចាស់បូត។\n"
            "🛡️ <b>រង្វាន់របស់អ្នកត្រូវបានរក្សាទុកយ៉ាងមានសុវត្ថិភាពក្នុង escrow</b> ហើយនឹងត្រូវបានចេញផ្សាយតែនៅពេលមានព័ត៌មានដែលបានផ្ទៀងផ្ទាត់ និងជោគជ័យប៉ុណ្ណោះ។\n\n"
            "🚀 សូមអរគុណដែលបានក្លាយជាផ្នែកមួយនៃវេទិការបស់យើង!"
        ),
        "owner_message": (
            "📢 <b>ការផ្ទេររង្វាន់ថ្មីបានបញ្ចប់</b>\n\n"
            "🆔 <b>លេខសម្គាល់អ្នកប្រើប្រាស់៖</b> <code>{user_id}</code>\n"
            "📄 <b>លេខសម្គាល់ករណី៖</b> <code>{case.id}</code>\n"
            "💰 <b>ចំនួនទឹកប្រាក់៖</b> {reward_amount} {wallet_type}\n"
            "🔐 <b>កាបូប៖</b> <code>{wallet.public_key}</code>\n"
            "🏷️ <b>ឈ្មោះកាបូប៖</b> {wallet.name}\n\n"
            "✅ <b>ស្ថានភាព៖</b> ការផ្ទេររង្វាន់បានជោគជ័យ។\n"
            "🔍 ប្រើ /listing ដើម្បីមើលករណីសកម្មទាំងអស់។"
        ),
        "transaction_failed": "❌ <b>ការផ្ទេរបានបរាជ័យ</b>\n\nមានបញ្ហាអ្វីមួយកើតឡើងខណៈពេលកំពុងដំណើរការការផ្ទេររង្វាន់។ សូមព្យាយាមម្តងទៀតនៅពេលក្រោយ។",
        "transfer_failed": "ការផ្ទេរបានបរាជ័យ។ សូមព្យាយាមម្តងទៀត។",
        "transfer_canceled": "ការផ្ទេរត្រូវបានលុបចោល។",
        "enter_reward_amount_unknown": "សូមបញ្ចូលចំនួនរង្វាន់ (ប្រភេទកាបូបមិនស្គាល់)។",
        "reward_amount_invalid": "❌ សូមបញ្ចូលចំនួនរង្វាន់ជាលេខដែលត្រឹមត្រូវ។",
        "finder_disclaimer": (
            "📜 មុនពេលអ្នកបន្ត – សូមអានដោយយកចិត្តទុកដាក់\n\n"
            "តាមរយៈការចូលរួមជាអ្នកស្វែងរកនៅលើ PeopleTrace អ្នកយល់ព្រមនឹងចំណុចខាងក្រោម៖\n\n"
            "• 🔍 អ្នកនឹងប្រើវេទិកានេះដើម្បីជួយស្វែងរកមនុស្សដែលបាត់ខ្លួនដោយស្របច្បាប់តែប៉ុណ្ណោះ\n"
            "• 📹 ព័ត៌មានត្រូវតែរួមបញ្ចូលភស្តុតាងដែលអាចផ្ទៀងផ្ទាត់បាន (រូបថត/វីដេអូ)\n"
            "• 💬 ការប្រាស្រ័យទាក់ទងជាមួយអ្នកបង្ហោះត្រូវតែគោរព និងមានសីលធម៌\n"
            "• 🧾 កុំប្រើខ្លឹមសារមិនពិត, បង្កើតដោយ AI, ឬ گمراه کننده\n"
            "• 📍 អ្នកអាចត្រូវបានស្នើសុំឱ្យបញ្ជាក់បន្ថែម ឬភស្តុតាងទីតាំង\n"
            "• 💸 ថ្លៃសេវាវេទិកា 5% ត្រូវបានកាត់ចេញពីការទាមទាររង្វាន់ដែលជោគជ័យ\n"
            "• 🚫 ការប្រើប្រាស់ខុស, ការជំរិត, ឬพฤติกรรมน่าสงสัยនឹងនាំឱ្យមានការហាមឃាត់ជាអចិន្ត្រៃយ៍ និងវិធានការផ្លូវច្បាប់\n"
            "• ❗️ យើងขอสงวนสิทธิ์ในการปฏิเสธคำร้องหรือหลักฐานที่ไม่จริงหรือไม่สามารถตรวจสอบได้\n\n"
            "តើអ្នកយល់ព្រមនឹងលក្ខខណ្ឌទាំងនេះទេ?"
        ),
        "enter_name": "សូមបញ្ចូលឈ្មោះរបស់អ្នក:",
        "reward_too_low_tip": (
            "💸 <b>រង្វាន់ត្រូវបានកំណត់ទៅ {amount} {type}</b>\n\n"
            "💡 <b>គន្លឹះ៖</b> រង្វាន់កាន់តែខ្ពស់ ការចាប់អារម្មណ៍កាន់តែច្រើន!\n"
            "ការផ្តល់រង្វាន់ដ៏សប្បុរសជំរុញឱ្យមនុស្សកាន់តែច្រើនចូលរួមក្នុងការស្វែងរក — "
            "បង្កើនឱកាសរបស់អ្នកក្នុងការស្វែងរកបុគ្គលនោះបានលឿនជាងមុន។ 🕵️‍♂️💬\n"
            "ការបន្ថែមបន្តិចបន្តួចអាចជួយប្រមូលផ្តុំហ្វូងមនុស្សដ៏មានឥទ្ធិពលនៅពីក្រោយករណីរបស់អ្នក។"
        ),
        "cancel_edit_button": "❌ បោះបង់ / កែសម្រួល",
        "increase_reward_button": "💰 បង្កើនរង្វាន់",
        "back_button": "🔙 ត្រឡប់",
        "enter_reward_amount_usdt": "សូមបញ្ចូលចំនួនរង្វាន់ជា USDT:",
        "transfer_successful": "ការផ្ទេរបានជោគជ័យ។",
        "transfer_error": "កំហុសមួយបានកើតឡើងខណៈពេលដំណើរការផ្ទេរ។ សូមព្យាយាមម្តងទៀត។",
        "invalid_confirmation": "ចម្លើយមិនត្រឹមត្រូវ។ សូមបញ្ជាក់ដោយប្រើ 'បាទ' ឬ 'ទេ'។",
        "enter_reason_for_finding": "សូមបញ្ចូលហេតុផលសម្រាប់ការស្វែងរក។",
        "case_submitted": "ករណីរបស់អ្នកត្រូវបានបញ្ជូនដោយជោគជ័យ។",
        "case_completed": "ករណីរបស់អ្នកត្រូវបានបញ្ចប់។",
        "choose_existing_mobile": "សូមជ្រើសរើសលេខដែលមានស្រាប់ ឬបន្ថែមលេខថ្មី។",
        "tac_invalid": "❌ TAC មិនត្រឹមត្រូវ។ សូមព្យាយាមម្តងទៀត។",
        "wallet_name_empty": "ឈ្មោះកាបូបមិនអាចទទេបានទេ។ សូមព្យាយាមម្តងទៀត។",
        "wallet_name_exists": "❌ កាបូបដែលមានឈ្មោះនេះមានស្រាប់ហើយ។ សូមជ្រើសរើសឈ្មោះផ្សេងទៀត។",
        "wallet_create_details": (
            "✅ កាបូបត្រូវបានបង្កើតដោយជោគជ័យ!\n"
            "🧾 ឈ្មោះ: {name}\n"
            "💰 ប្រភេទ: {wallet_type}\n"
            "🔐 គន្លឹះសាធារណៈ: <code>{public_key}</code>\n"
            "🌐 បណ្តាញ: {network}\n"
        ),
        "mobile_number_doesnt_exist": "លេខទូរសព្ទដែលអ្នកបានបញ្ចូលមិនមានទេ។ សូមព្យាយាមម្តងទៀត។",
        "invalid_choice": "⚠️ <b>ជម្រើសមិនត្រឹមត្រូវ</b>\n\nសូមជ្រើសរើសជម្រើសដែលត្រឹមត្រូវ។",
        "mobile_selected_with_tac": "លេខទូរសព្ទដែលអ្នកបានបញ្ចូលត្រូវបានផ្ទៀងផ្ទាត់។ សូមបញ្ចូលលេខកូដផ្ទៀងផ្ទាត់:",
        "enter_valid_mobile": "❌ លេខទូរសព្ទមិនត្រឹមត្រូវ។ សូមបញ្ចូលលេខទូរសព្ទ១០ខ្ទង់ត្រឹមត្រូវ។",
        "wallet_create_err": "កំហុសកើតឡើងក្នុងការបង្កើតកាបូប។ សូមព្យាយាមម្តងទៀត។",
        "wallet_name_prompt": "សូមបញ្ចូលឈ្មោះសម្រាប់កាបូប {wallet_type} របស់អ្នក:",
        "wallet_create_details_with_balance": (
            "✅ កាបូបត្រូវបានបង្កើតដោយជោគជ័យ!\n"
            "🧾 ឈ្មោះ: {name}\n"
            "💰 ប្រភេទ: {wallet_type}\n"
            "🔐 គន្លឹះសាធារណៈ: <code>{public_key}</code>\n"
            "🌐 បណ្តាញ: {network}\n"
            "💵 សមតុល្យ: {balance} {wallet_type}\n"
        ),
        "understood_and_agree": "✅ ខ្ញុំយល់ និងយល់ព្រម",
    },
    "malay": {
        "case_poster_disclaimer": (
            "📜 *Sebelum Anda Teruskan – Sila Baca Dengan Teliti*\n\n"
            "Dengan menyiarkan kes di PeopleTrace, anda bersetuju dengan yang berikut:\n\n"
            "• 🧾 Semua maklumat mestilah tepat dan jujur\n"
            "• 🚫 Platform ini tidak boleh digunakan untuk mengganggu, menghendap, atau mencederakan orang lain\n"
            "• 🕵️‍♂️ Penggunaan adalah semata-mata untuk mencari orang secara sah\n"
            "• 📍 Anda mesti melaporkan kes itu kepada pihak berkuasa tempatan terlebih dahulu\n"
            "• 🔍 Semua butiran kes akan dapat dilihat oleh umum\n"
            "• 💰 Ganjaran disimpan dalam escrow sehingga pengesahan\n"
            "• ⚠️ PeopleTrace tidak bertanggungjawab atas penyalahgunaan atau akibat pihak ketiga\n"
            "• ❗️Laporan palsu, kandungan yang menyinggung perasaan, atau niat yang menyalahi undang-undang akan membawa kepada larangan kekal dan tindakan undang-undang\n\n"
            "*Adakah anda bersetuju dengan terma-terma ini?*"
        ),
        "create_case_title": "Butiran Kes",
        "enter_person_name": "👤 Masukkan nama penuh orang yang anda cari:",
        "male_option": "♂ Lelaki",
        "female_option": "♀ Perempuan",
        "other_option": "Lain-lain",
        "gender": "⚧️ Jantina:",
        "valid_age": "Sila masukkan nombor yang sah untuk umur.",
        "age": "🎂 Umur (atau anggaran):",
        "hair_color": "🧑 Warna rambut:",
        "eye_color": "👁️ Warna mata:",
        "height": "📏 Ketinggian (dalam cm):",
        "weight": "⚖️ Berat (dalam kg)",
        "relationship": "🤝 Apakah hubungan anda dengan orang ini?",
        "upload_photo": "📸 Muat naik foto yang jelas dan terkini (Maksimum 5MB):",
        "no_photo_found": "Tiada foto dijumpai. Sila muat naik fail imej yang sah.",
        "enter_valid_height": "Sila masukkan ketinggian yang sah (cm).",
        "last_seen_location": "👕 Apakah pakaian terakhir yang dipakai oleh orang ini? \n (Sertakan jenis pakaian, warna, aksesori, kasut, dll.)",
        "enter_valid_weight": "Sila masukkan berat yang sah (kg).",
        "distinctive_features": "🧷 Adakah ciri fizikal yang unik? (tatu, parut, dll.)",
        "reason_for_finding": "❓ Mengapa anda mencari orang ini?",
        "case_not_found": "Kes tidak dijumpai. Sila cuba lagi.",
        "enter_reward_amount": (
            "💰 <b>Penyediaan Ganjaran</b>\n\n"
            "Apakah ganjaran yang ingin anda tawarkan untuk petunjuk yang disahkan? (dalam {type})"
        ),
        "reward_amount_negative": "❌ Jumlah ganjaran mestilah lebih besar daripada 0. Anda memasukkan: {0}.",
        "insufficient_balance": "🚫 Baki Tidak Mencukupi. Anda hanya mempunyai {0} yang tersedia.",
        "refresh_wallet_balance": "🔄 Sila segarkan baki dompet anda atau kurangkan ganjaran.",
        "reward_amount_confirmed": (
            "💸 Jumlah ganjaran sebanyak {0} telah disahkan.\n\n"
            "🔒 Baki dompet anda sedang disemak..."
        ),
        "insufficient_balance_for_transfer": (
            "🚫 <b>Baki Tidak Mencukupi</b>\n\n"
            "Dompet anda hanya mempunyai <b>{wallet_balance} {wallet_type}</b>.\n"
            "Jumlah ganjaran ialah <b>{reward_amount} {wallet_type}</b>.\n"
            "Sila pastikan dompet anda mempunyai baki yang mencukupi untuk meneruskan."
        ),
        "congratulates_advertiser": (
            "🎉 <b>Tahniah!</b>\n\n"
            "Ganjaran anda sebanyak <b>{reward_amount} {wallet_type}</b> telah berjaya dipindahkan ke platform kami.\n\n"
            "📝 <b>Ringkasan Kes:</b>\n"
            "👤 <b>Nama Kes:</b> {case_name}\n"
            "📍 <b>Lokasi:</b> {location}\n"
            "🎁 <b>Ganjaran yang Ditawarkan:</b> {reward_amount} {wallet_type}\n"
            "💸 <b>Yuran Platform (5%):</b> {platform_fee} {wallet_type}\n"
            "🔒 <b>Bersih yang Dipegang dalam Escrow:</b> {net_amount} {wallet_type}\n\n"
            "🙌 Kami telah mengemukakan kes anda dan ganjaran telah dipindahkan ke dompet pemilik bot.\n"
            "🛡️ <b>Ganjaran anda dipegang dengan selamat dalam escrow</b> dan hanya akan dikeluarkan setelah petunjuk yang disahkan dan berjaya.\n\n"
            "🚀 Terima kasih kerana menjadi sebahagian daripada platform kami!"
        ),
        "owner_message": (
            "📢 <b>Pemindahan Ganjaran Baharu Selesai</b>\n\n"
            "🆔 <b>ID Pengguna:</b> <code>{user_id}</code>\n"
            "📄 <b>ID Kes:</b> <code>{case.id}</code>\n"
            "💰 <b>Jumlah:</b> {reward_amount} {wallet_type}\n"
            "🔐 <b>Dompet:</b> <code>{wallet.public_key}</code>\n"
            "🏷️ <b>Nama Dompet:</b> {wallet.name}\n\n"
            "✅ <b>Status:</b> Ganjaran berjaya dipindahkan.\n"
            "🔍 Gunakan /listing untuk melihat semua kes aktif."
        ),
        "transaction_failed": "❌ <b>Pemindahan Gagal</b>\n\nAda sesuatu yang salah semasa memproses pemindahan ganjaran. Sila cuba lagi nanti.",
        "transfer_failed": "Pemindahan gagal. Sila cuba lagi.",
        "transfer_canceled": "Pemindahan telah dibatalkan.",
        "enter_reward_amount_unknown": "Sila masukkan jumlah ganjaran (jenis dompet tidak diketahui).",
        "reward_amount_invalid": "❌ Sila masukkan jumlah ganjaran numerik yang sah.",
        "finder_disclaimer": (
            "📜 Sebelum Anda Teruskan – Sila Baca Dengan Teliti\n\n"
            "Dengan menyertai sebagai Pencari di PeopleTrace, anda bersetuju dengan berikut:\n\n"
            "• 🔍 Anda hanya akan menggunakan platform ini untuk membantu mencari orang hilang secara sah\n"
            "• 📹 Petunjuk mesti merangkumi bukti yang boleh disahkan (foto/video)\n"
            "• 💬 Komunikasi dengan pemberi maklumat harus kekal sopan dan bermoral\n"
            "• 🧾 Jangan gunakan kandungan palsu, dijana oleh AI atau menyesatkan\n"
            "• 📍 Anda mungkin diminta memberikan penjelasan tambahan atau bukti lokasi\n"
            "• 💸 5% yuran platform akan dikenakan pada tuntutan ganjaran yang berjaya\n"
            "• 🚫 Penyalahgunaan, ugutan atau tingkah laku mencurigakan akan membawa kepada penggantungan kekal dan tindakan undang-undang\n"
            "• ❗ Kami berhak menolak tuntutan palsu atau tidak disahkan\n\n"
            "Adakah anda bersetuju dengan terma-terma ini?"
        ),
        "enter_name": "Masukkan nama anda:",
        "reward_too_low_tip": (
            "💸 <b>Ganjaran ditetapkan kepada {amount} {type}</b>\n\n"
            "💡 <b>Petua:</b> Semakin tinggi ganjaran, semakin banyak mata yang anda tarik!\n"
            "Menawarkan ganjaran yang murah hati mendorong lebih ramai orang untuk menyertai pencarian — "
            "meningkatkan peluang anda untuk mencari orang itu dengan lebih cepat. 🕵️‍♂️💬\n"
            "Sedikit tambahan boleh membantu mengumpulkan orang ramai yang kuat di belakang kes anda."
        ),
        "cancel_edit_button": "❌ Batal / Edit",
        "increase_reward_button": "💰 Tingkatkan Ganjaran",
        "back_button": "🔙 Kembali",
        "enter_reward_amount_usdt": "Sila masukkan jumlah ganjaran dalam USDT.",
        "transfer_successful": "Pemindahan berjaya.",
        "transfer_error": "Ralat berlaku semasa memproses pemindahan. Sila cuba lagi.",
        "invalid_confirmation": "Jawapan tidak sah. Sila sahkan dengan 'ya' atau 'tidak'.",
        "enter_reason_for_finding": "Sila nyatakan sebab mencari.",
        "case_submitted": "Kes anda telah berjaya dihantar.",
        "case_completed": "Kes anda telah selesai.",
        "choose_existing_mobile": "Sila pilih nombor sedia ada atau tambah yang baru.",
        "tac_invalid": "❌ Kod pengesahan tidak sah. Sila cuba lagi.",
        "wallet_name_empty": "Nama dompet tidak boleh kosong. Sila cuba lagi.",
        "wallet_name_exists": "❌ Dompet dengan nama ini sudah wujud. Sila pilih nama lain.",
        "wallet_create_details": (
            "✅ Dompet Dicipta!\n"
            "🧾 Nama: {name}\n"
            "💰 Jenis: {wallet_type}\n"
            "🔐 Kunci Awam: <code>{public_key}</code>\n"
            "🌐 Rangkaian: {network}\n"
        ),
        "mobile_number_doesnt_exist": "Nombor telefon bimbit yang anda masukkan tidak wujud. Sila cuba lagi.",
        "invalid_choice": "⚠️ <b>Pilihan Tidak Sah</b>\n\nSila pilih pilihan yang sah.",
        "mobile_selected_with_tac": "Nombor telefon bimbit yang dimasukkan telah disahkan. Sila masukkan kod pengesahan:",
        "enter_valid_mobile": "❌ Nombor telefon bimbit tidak sah. Sila masukkan nombor 10 digit yang sah.",
        "wallet_create_err": "Ralat berlaku semasa mencipta dompet. Sila cuba lagi.",
        "wallet_name_prompt": "Sila masukkan nama untuk dompet {wallet_type} anda:",
        "wallet_create_details_with_balance": (
            "✅ Dompet Dicipta!\n"
            "🧾 Nama: {name}\n"
            "💰 Jenis: {wallet_type}\n"
            "🔐 Kunci Awam: <code>{public_key}</code>\n"
            "🌐 Rangkaian: {network}\n"
            "💵 Baki: {balance} {wallet_type}\n"
        ),
        "understood_and_agree": "✅ Saya Faham dan Setuju",
    },
    "indonesian": {
        "case_poster_disclaimer": (
            "📜 *Sebelum Lanjut – Harap Dibaca Dengan Seksama*\n\n"
            "Dengan memposting kasus di PeopleTrace, Anda menyetujui hal-hal berikut:\n\n"
            "• 🧾 Semua informasi harus akurat dan jujur\n"
            "• 🚫 Platform ini tidak boleh digunakan untuk melecehkan, menguntit, atau merugikan orang lain\n"
            "• 🕵️‍♂️ Penggunaan hanya untuk mencari orang secara sah\n"
            "• 📍 Anda harus melaporkan kasus ini ke pihak berwenang setempat terlebih dahulu\n"
            "• 🔍 Semua detail kasus akan dapat dilihat oleh publik\n"
            "• 💰 Hadiah disimpan dalam escrow hingga verifikasi\n"
            "• ⚠️ PeopleTrace tidak bertanggung jawab atas penyalahgunaan atau konsekuensi pihak ketiga\n"
            "• ❗️Laporan palsu, konten yang menyinggung, atau niat ilegal akan menyebabkan pemblokiran permanen dan tindakan hukum\n\n"
            "*Apakah Anda setuju dengan ketentuan ini?*"
        ),
        "create_case_title": "Detail Kasus",
        "enter_person_name": "👤 Masukkan nama lengkap orang yang Anda cari:",
        "male_option": "♂ Laki-laki",
        "female_option": "♀ Perempuan",
        "other_option": "Lainnya",
        "gender": "⚧️ Jenis Kelamin:",
        "valid_age": "Silakan masukkan angka yang valid untuk usia.",
        "age": "🎂 Usia (atau perkiraan):",
        "hair_color": "🧑 Warna rambut:",
        "eye_color": "👁️ Warna mata:",
        "height": "📏 Tinggi badan (dalam cm):",
        "weight": "⚖️ Berat badan (dalam kg)",
        "relationship": "🤝 Apa hubungan Anda dengan orang ini?",
        "upload_photo": "📸 Unggah foto yang jelas dan terbaru (Maksimal 5MB):",
        "no_photo_found": "Tidak ada foto ditemukan. Silakan unggah file gambar yang valid.",
        "enter_valid_height": "Silakan masukkan tinggi badan yang valid (cm).",
        "last_seen_location": "👕 Apa yang terakhir kali dikenakan orang ini? \n (Sertakan jenis pakaian, warna, aksesori, sepatu, dll.)",
        "enter_valid_weight": "Silakan masukkan berat badan yang valid (kg).",
        "distinctive_features": "🧷 Apakah ada ciri fisik khusus? (tato, bekas luka, dll.)",
        "reason_for_finding": "❓ Mengapa Anda mencari orang ini?",
        "case_not_found": "Kasus tidak ditemukan. Silakan coba lagi.",
        "enter_reward_amount": (
            "💰 <b>Pengaturan Hadiah</b>\n\n"
            "Hadiah apa yang ingin Anda tawarkan untuk petunjuk yang terverifikasi? (dalam {type})"
        ),
        "reward_amount_negative": "❌ Jumlah hadiah harus lebih besar dari 0. Anda memasukkan: {0}.",
        "insufficient_balance": "🚫 Saldo Tidak Cukup. Anda hanya memiliki {0} yang tersedia.",
        "refresh_wallet_balance": "🔄 Harap segarkan saldo dompet Anda atau kurangi hadiah.",
        "reward_amount_confirmed": (
            "💸 Jumlah hadiah sebesar {0} telah dikonfirmasi.\n\n"
            "🔒 Saldo dompet Anda sedang diperiksa..."
        ),
        "insufficient_balance_for_transfer": (
            "🚫 <b>Saldo Tidak Cukup</b>\n\n"
            "Dompet Anda hanya memiliki <b>{wallet_balance} {wallet_type}</b>.\n"
            "Jumlah hadiah adalah <b>{reward_amount} {wallet_type}</b>.\n"
            "Harap pastikan dompet Anda memiliki saldo yang cukup untuk melanjutkan."
        ),
        "congratulates_advertiser": (
            "🎉 <b>Selamat!</b>\n\n"
            "Hadiah Anda sebesar <b>{reward_amount} {wallet_type}</b> telah berhasil ditransfer ke platform kami.\n\n"
            "📝 <b>Ringkasan Kasus:</b>\n"
            "👤 <b>Nama Kasus:</b> {case_name}\n"
            "📍 <b>Lokasi:</b> {location}\n"
            "🎁 <b>Hadiah yang Ditawarkan:</b> {reward_amount} {wallet_type}\n"
            "💸 <b>Biaya Platform (5%):</b> {platform_fee} {wallet_type}\n"
            "🔒 <b>Bersih yang Disimpan dalam Escrow:</b> {net_amount} {wallet_type}\n\n"
            "🙌 Kami telah mengajukan kasus Anda dan hadiah telah dipindahkan ke dompet pemilik bot.\n"
            "🛡️ <b>Hadiah Anda disimpan dengan aman di escrow</b> dan hanya akan dilepaskan setelah petunjuk yang terverifikasi dan berhasil.\n\n"
            "🚀 Terima kasih telah menjadi bagian dari platform kami!"
        ),
        "owner_message": (
            "📢 <b>Transfer Hadiah Baru Selesai</b>\n\n"
            "🆔 <b>ID Pengguna:</b> <code>{user_id}</code>\n"
            "📄 <b>ID Kasus:</b> <code>{case.id}</code>\n"
            "💰 <b>Jumlah:</b> {reward_amount} {wallet_type}\n"
            "🔐 <b>Dompet:</b> <code>{wallet.public_key}</code>\n"
            "🏷️ <b>Nama Dompet:</b> {wallet.name}\n\n"
            "✅ <b>Status:</b> Hadiah berhasil ditransfer.\n"
            "🔍 Gunakan /listing untuk melihat semua kasus aktif."
        ),
        "transaction_failed": "❌ <b>Transfer Gagal</b>\n\nTerjadi masalah saat memproses transfer hadiah. Silakan coba lagi nanti.",
        "transfer_failed": "Transfer gagal. Silakan coba lagi.",
        "transfer_canceled": "Transfer telah dibatalkan.",
        "enter_reward_amount_unknown": "Silakan masukkan jumlah hadiah (jenis dompet tidak diketahui).",
        "reward_amount_invalid": "❌ Silakan masukkan jumlah hadiah numerik yang valid.",
        "finder_disclaimer": (
            "📜 Sebelum Lanjut – Harap Dibaca Dengan Seksama\n\n"
            "Dengan menjadi Penemu di PeopleTrace, Anda setuju hal-hal berikut:\n\n"
            "• 🔍 Anda hanya menggunakan platform ini untuk mencari orang hilang secara legal\n"
            "• 📹 Bukti harus meliputi data yang dapat diverifikasi (foto/video)\n"
            "• 💬 Komunikasi dengan pelapor harus tetap sopan dan etis\n"
            "• 🧾 Jangan gunakan konten palsu, hasil AI, atau menyesatkan\n"
            "• 📍 Anda mungkin diminta klarifikasi tambahan atau bukti lokasi\n"
            "• 💸 Biaya platform 5% akan dipotong dari klaim hadiah yang berhasil\n"
            "• 🚫 Penyalahgunaan, pemerasan, atau perilaku mencurigakan akan berujung pada larangan permanen dan tindakan hukum\n"
            "• ❗ Kami berhak menolak klaim palsu atau tidak terverifikasi\n\n"
            "Apakah Anda setuju dengan ketentuan ini?"
        ),
        "enter_name": "Masukkan nama Anda:",
        "reward_too_low_tip": (
            "💸 <b>Hadiah ditetapkan sebesar {amount} {type}</b>\n\n"
            "💡 <b>Tips:</b> Semakin tinggi hadiah, semakin banyak perhatian yang Anda dapatkan!\n"
            "Menawarkan hadiah yang besar akan memotivasi lebih banyak orang untuk bergabung dalam pencarian — "
            "meningkatkan peluang Anda untuk menemukan orang tersebut lebih cepat. 🕵️‍♂️💬\n"
            "Sedikit tambahan bisa sangat membantu dalam mengumpulkan dukungan yang kuat di belakang kasus Anda."
        ),
        "cancel_edit_button": "❌ Batal / Edit",
        "increase_reward_button": "💰 Tingkatkan Hadiah",
        "back_button": "🔙 Kembali",
        "enter_reward_amount_usdt": "Silakan masukkan jumlah hadiah dalam USDT.",
        "transfer_successful": "Transfer berhasil.",
        "transfer_error": "Terjadi kesalahan saat memproses transfer. Silakan coba lagi.",
        "invalid_confirmation": "Respons tidak valid. Silakan konfirmasi dengan 'ya' atau 'tidak'.",
        "enter_reason_for_finding": "Silakan tuliskan alasan pencarian.",
        "case_submitted": "Kasus Anda telah berhasil diajukan.",
        "case_completed": "Kasus Anda telah selesai.",
        "choose_existing_mobile": "Silakan pilih nomor yang ada atau tambah nomor baru.",
        "tac_invalid": "❌ Kode verifikasi tidak valid. Silakan coba lagi.",
        "wallet_name_empty": "Nama dompet tidak boleh kosong. Silakan coba lagi.",
        "wallet_name_exists": "❌ Dompet dengan nama ini sudah ada. Silakan pilih nama lain.",
        "wallet_create_details": (
            "✅ Dompet Dibuat!\n"
            "🧾 Nama: {name}\n"
            "💰 Jenis: {wallet_type}\n"
            "🔐 Kunci Publik: <code>{public_key}</code>\n"
            "🌐 Jaringan: {network}\n"
        ),
        "mobile_number_doesnt_exist": "Nomor telepon seluler yang Anda masukkan tidak ada. Silakan coba lagi.",
        "invalid_choice": "⚠️ <b>Pilihan Tidak Valid</b>\n\nSilakan pilih opsi yang benar.",
        "mobile_selected_with_tac": "Nomor telepon yang Anda masukkan telah diverifikasi. Silakan masukkan kode verifikasi:",
        "enter_valid_mobile": "❌ Nomor telepon tidak valid. Silakan masukkan nomor 10 digit yang benar.",
        "wallet_create_err": "Terjadi kesalahan saat membuat dompet. Silakan coba lagi.",
        "wallet_name_prompt": "Silakan masukkan nama untuk dompet {wallet_type} Anda:",
        "wallet_create_details_with_balance": (
            "✅ Dompet Dibuat!\n"
            "🧾 Nama: {name}\n"
            "💰 Jenis: {wallet_type}\n"
            "🔐 Kunci Publik: <code>{public_key}</code>\n"
            "🌐 Jaringan: {network}\n"
            "💵 Saldo: {balance} {wallet_type}\n"
        ),
        "understood_and_agree": "✅ Saya Mengerti dan Setuju",
    },
    "thai": {
        "case_poster_disclaimer": (
            "📜 *ก่อนที่คุณจะดำเนินการต่อ – กรุณาอ่านอย่างละเอียด*\n\n"
            "โดยการโพสต์เคสบน PeopleTrace คุณยอมรับเงื่อนไขดังต่อไปนี้:\n\n"
            "• 🧾 ข้อมูลทั้งหมดต้องถูกต้องและเป็นจริง\n"
            "• 🚫 ห้ามใช้แพลตฟอร์มนี้ในการคุกคาม, ติดตาม, หรือทำร้ายผู้อื่น\n"
            "• 🕵️‍♂️ การใช้งานมีไว้สำหรับการค้นหาบุคคลอย่างถูกกฎหมายเท่านั้น\n"
            "• 📍 คุณต้องรายงานเคสต่อเจ้าหน้าที่ท้องถิ่นก่อน\n"
            "• 🔍 รายละเอียดเคสทั้งหมดจะถูกเปิดเผยต่อสาธารณะ\n"
            "• 💰 รางวัลจะถูกเก็บไว้ในเอสโครว์จนกว่าจะมีการตรวจสอบ\n"
            "• ⚠️ PeopleTrace ไม่รับผิดชอบต่อการใช้งานในทางที่ผิดหรือผลที่ตามมาจากบุคคลที่สาม\n"
            "• ❗️รายงานเท็จ, เนื้อหาที่ไม่เหมาะสม, หรือเจตนาที่ผิดกฎหมายจะนำไปสู่การแบนถาวรและการดำเนินการทางกฎหมาย\n\n"
            "*คุณยอมรับเงื่อนไขเหล่านี้หรือไม่?*"
        ),
        "create_case_title": "รายละเอียดเคส",
        "enter_person_name": "👤 กรุณาป้อนชื่อเต็มของบุคคลที่คุณกำลังตามหา:",
        "male_option": "♂ ชาย",
        "female_option": "♀ หญิง",
        "other_option": "อื่น ๆ",
        "gender": "⚧️ เพศ:",
        "valid_age": "กรุณาป้อนอายุเป็นตัวเลขที่ถูกต้อง",
        "age": "🎂 อายุ (หรือประมาณอายุ):",
        "hair_color": "🧑 สีผม:",
        "eye_color": "👁️ สีตา:",
        "height": "📏 ความสูง (เซนติเมตร):",
        "weight": "⚖️ น้ำหนัก (กิโลกรัม)",
        "relationship": "🤝 คุณมีความสัมพันธ์กับบุคคลนี้อย่างไร?",
        "upload_photo": "📸 อัปโหลดรูปภาพที่ชัดเจนและใหม่ล่าสุด (สูงสุด 5MB):",
        "no_photo_found": "ไม่พบไฟล์รูปภาพ กรุณาอัปโหลดไฟล์รูปภาพที่ถูกต้อง",
        "enter_valid_height": "กรุณาป้อนความสูงที่ถูกต้อง (ซม.).",
        "last_seen_location": "👕 บุคคลนี้สวมใส่อะไรครั้งสุดท้ายที่พบเห็น? \n (รวมถึงประเภทเสื้อผ้า, สี, เครื่องประดับ, รองเท้า, ฯลฯ)",
        "enter_valid_weight": "กรุณาป้อนน้ำหนักที่ถูกต้อง (กก.).",
        "distinctive_features": "🧷 มีลักษณะเด่นทางกายภาพใดบ้าง? (รอยสัก, แผลเป็น ฯลฯ)",
        "reason_for_finding": "❓ ทำไมคุณถึงตามหาบุคคลนี้?",
        "case_not_found": "ไม่พบเคส กรุณาลองใหม่",
        "enter_reward_amount": (
            "💰 <b>การตั้งค่ารางวัล</b>\n\n"
            "คุณต้องการเสนอรางวัลอะไรสำหรับเบาะแสที่ตรวจสอบแล้ว? (ใน {type})"
        ),
        "reward_amount_negative": "❌ จำนวนเงินรางวัลต้องมากกว่า 0. คุณป้อน: {0}.",
        "insufficient_balance": "🚫 ยอดคงเหลือไม่เพียงพอ คุณมี {0} อยู่ในบัญชี",
        "refresh_wallet_balance": "🔄 กรุณาอัปเดทยอดคงเหลือของกระเป๋าเงินหรือลดรางวัล",
        "reward_amount_confirmed": (
            "💸 จำนวนเงินรางวัล {0} ของคุณได้รับการยืนยันแล้ว\n\n"
            "🔒 กำลังตรวจสอบยอดคงเหลือในกระเป๋าเงินของคุณ..."
        ),
        "insufficient_balance_for_transfer": (
            "🚫 <b>ยอดคงเหลือไม่เพียงพอ</b>\n\n"
            "กระเป๋าเงินของคุณมีเพียง <b>{wallet_balance} {wallet_type}</b>.\n"
            "จำนวนเงินรางวัลคือ <b>{reward_amount} {wallet_type}</b>.\n"
            "กรุณาตรวจสอบให้แน่ใจว่ากระเป๋าเงินของคุณมียอดคงเหลือเพียงพอที่จะดำเนินการต่อ"
        ),
        "congratulates_advertiser": (
            "🎉 <b>ขอแสดงความยินดี!</b>\n\n"
            "รางวัลของคุณจำนวน <b>{reward_amount} {wallet_type}</b> ได้รับการโอนไปยังแพลตฟอร์มของเราเรียบร้อยแล้ว\n\n"
            "📝 <b>สรุปเคส:</b>\n"
            "👤 <b>ชื่อเคส:</b> {case_name}\n"
            "📍 <b>สถานที่:</b> {location}\n"
            "🎁 <b>รางวัลที่เสนอ:</b> {reward_amount} {wallet_type}\n"
            "💸 <b>ค่าธรรมเนียมแพลตฟอร์ม (5%):</b> {platform_fee} {wallet_type}\n"
            "🔒 <b>ยอดสุทธิที่เก็บในเอสโครว์:</b> {net_amount} {wallet_type}\n\n"
            "🙌 เราได้ยื่นเคสของคุณแล้วและรางวัลได้ถูกโอนไปยังกระเป๋าเงินของเจ้าของบอท\n"
            "🛡️ <b>รางวัลของคุณถูกเก็บไว้อย่างปลอดภัยในเอสโครว์</b> และจะถูกปล่อยออกมาเมื่อมีเบาะแสที่ตรวจสอบแล้วและประสบความสำเร็จเท่านั้น\n\n"
            "🚀 ขอบคุณที่เป็นส่วนหนึ่งของแพลตฟอร์มของเรา!"
        ),
        "owner_message": (
            "📢 <b>การโอนรางวัลใหม่เสร็จสมบูรณ์</b>\n\n"
            "🆔 <b>รหัสผู้ใช้:</b> <code>{user_id}</code>\n"
            "📄 <b>รหัสเคส:</b> <code>{case.id}</code>\n"
            "💰 <b>จำนวน:</b> {reward_amount} {wallet_type}\n"
            "🔐 <b>กระเป๋าเงิน:</b> <code>{wallet.public_key}</code>\n"
            "🏷️ <b>ชื่อกระเป๋าเงิน:</b> {wallet.name}\n\n"
            "✅ <b>สถานะ:</b> โอนรางวัลสำเร็จ\n"
            "🔍 ใช้ /listing เพื่อดูเคสที่ใช้งานอยู่ทั้งหมด"
        ),
        "transaction_failed": "❌ <b>การทำธุรกรรมล้มเหลว</b>\n\nเกิดปัญหาขึ้นขณะประมวลผลการโอนเงินรางวัล กรุณาลองใหม่ภายหลัง",
        "transfer_failed": "โอนล้มเหลว กรุณาลองใหม่",
        "transfer_canceled": "การโอนถูกยกเลิก",
        "enter_reward_amount_unknown": "กรุณาป้อนจำนวนเงินรางวัล (ประเภทกระเป๋าเงินไม่ทราบ)",
        "reward_amount_invalid": "❌ กรุณาป้อนจำนวนเงินรางวัลเป็นตัวเลขที่ถูกต้อง",
        "finder_disclaimer": (
            "📜 *ก่อนที่คุณจะดำเนินการต่อ – กรุณาอ่านอย่างละเอียด*\n\n"
            "โดยการเข้าร่วมเป็น*ผู้ค้นหา*บน PeopleTrace คุณยอมรับเงื่อนไขดังต่อไปนี้:\n\n"
            "• 🔍 คุณจะใช้แพลตฟอร์มนี้เพื่อช่วยตามหาบุคคลที่หายสาบสูญอย่างถูกกฎหมายเท่านั้น\n"
            "• 📹 เอกสารหลักฐานต้องมีข้อมูลที่ตรวจสอบได้ (รูปภาพ/วิดีโอ)\n"
            "• 💬 การสื่อสารกับผู้ลงประกาศต้องสุภาพและมีจริยธรรม\n"
            "• 🧾 ห้ามใช้เนื้อหาที่เป็นเท็จหรือสร้างจาก AI หรือทำให้เข้าใจผิด\n"
            "• 📍 คุณอาจถูกขอให้ให้คำชี้แจงเพิ่มเติมหรือหลักฐานเกี่ยวกับสถานที่\n"
            "• 💸 มีค่าธรรมเนียมแพลตฟอร์ม 5% จากจำนวนเงินรางวัลที่สำเร็จ\n"
            "• 🚫 การใช้งานในทางที่ผิด การเรียกร้องเงิน หรือพฤติกรรมน่าสงสัย จะนำไปสู่การแบนถาวรและดำเนินคดี\n"
            "• ❗ เราขอสงวนสิทธิ์ในการปฏิเสธคำร้องหรือหลักฐานที่ไม่จริงหรือไม่สามารถตรวจสอบได้\n\n"
            "*คุณยอมรับเงื่อนไขเหล่านี้หรือไม่?*"
        ),
        "enter_name": "กรุณาป้อนชื่อของคุณ:",
        "reward_too_low_tip": (
            "💸 <b>รางวัลตั้งไว้ที่ {amount} {type}</b>\n\n"
            "💡 <b>เคล็ดลับ:</b> ยิ่งรางวัลสูง ยิ่งดึงดูดความสนใจได้มาก!\n"
            "การเสนอรางวัลที่ щедрый กระตุ้นให้ผู้คนเข้าร่วมการค้นหามากขึ้น — "
            "เพิ่มโอกาสในการค้นหาบุคคลนั้นได้เร็วขึ้น 🕵️‍♂️💬\n"
            "การเพิ่มเล็กน้อยสามารถช่วยรวบรวมฝูงชนที่มีพลังมาสนับสนุนเคสของคุณได้"
        ),
        "cancel_edit_button": "❌ ยกเลิก / แก้ไข",
        "increase_reward_button": "💰 เพิ่มรางวัล",
        "back_button": "🔙 กลับ",
        "enter_reward_amount_usdt": "กรุณาป้อนจำนวนเงินรางวัลในรูปแบบ USDT.",
        "transfer_successful": "โอนสำเร็จ",
        "transfer_error": "เกิดข้อผิดพลาดขณะดำเนินการโอน กรุณาลองใหม่",
        "invalid_confirmation": "คำตอบไม่ถูกต้อง กรุณายืนยันด้วย 'ใช่' หรือ 'ไม่'",
        "enter_reason_for_finding": "กรุณาป้อนเหตุผลในการตามหา",
        "case_submitted": "เคสของคุณถูกส่งสำเร็จแล้ว",
        "case_completed": "เคสของคุณเสร็จสมบูรณ์แล้ว",
        "choose_existing_mobile": "กรุณาเลือกเบอร์โทรศัพท์ที่มีอยู่ หรือเพิ่มเบอร์ใหม่",
        "tac_invalid": "❌ รหัสยืนยันไม่ถูกต้อง กรุณาลองใหม่",
        "wallet_name_empty": "ชื่อกระเป๋าเงินห้ามว่าง กรุณาลองใหม่",
        "wallet_name_exists": "❌ มีกระเป๋าเงินชื่อนี้อยู่แล้ว กรุณาเลือกชื่ออื่น",
        "wallet_create_details": (
            "✅ กระเป๋าเงินถูกสร้างแล้ว!\n"
            "🧾 ชื่อ: {name}\n"
            "💰 ประเภท: {wallet_type}\n"
            "🔐 กุญแจสาธารณะ: <code>{public_key}</code>\n"
            "🌐 เครือข่าย: {network}\n"
        ),
        "mobile_number_doesnt_exist": "เบอร์โทรศัพท์มือถือที่คุณป้อนไม่มีอยู่จริง กรุณาลองใหม่อีกครั้ง",
        "invalid_choice": "⚠️ <b>เลือกไม่ถูกต้อง</b>\n\nกรุณาเลือกตัวเลือกที่ถูกต้อง",
        "mobile_selected_with_tac": "เบอร์โทรศัพท์ที่คุณเลือกได้รับการยืนยันแล้ว กรุณาป้อนรหัสยืนยัน:",
        "enter_valid_mobile": "❌ เบอร์โทรศัพท์ไม่ถูกต้อง กรุณาป้อนเบอร์ 10 หลักที่ถูกต้อง",
        "wallet_create_err": "เกิดข้อผิดพลาดขณะสร้างกระเป๋าเงิน กรุณาลองใหม่",
        "wallet_name_prompt": "กรุณาป้อนชื่อกระเป๋าเงินของคุณสำหรับ {wallet_type}:",
        "wallet_create_details_with_balance": (
            "✅ กระเป๋าเงินถูกสร้างแล้ว!\n"
            "🧾 ชื่อ: {name}\n"
            "💰 ประเภท: {wallet_type}\n"
            "🔐 กุญแจสาธารณะ: <code>{public_key}</code>\n"
            "🌐 เครือข่าย: {network}\n"
            "💵 ยอดคงเหลือ: {balance} {wallet_type}\n"
        ),
        "understood_and_agree": "✅ ฉันเข้าใจและยอมรับ",
    },
    "vietnamese": {
        "case_poster_disclaimer": (
            "📜 *Trước Khi Tiếp Tục – Vui Lòng Đọc Kỹ*\n\n"
            "Bằng cách đăng một vụ việc trên PeopleTrace, bạn đồng ý với những điều sau:\n\n"
            "• 🧾 Mọi thông tin phải chính xác và trung thực\n"
            "• 🚫 Nền tảng này không được sử dụng để quấy rối, theo dõi hoặc làm hại người khác\n"
            "• 🕵️‍♂️ Chỉ sử dụng cho mục đích tìm kiếm người một cách hợp pháp\n"
            "• 📍 Bạn phải báo cáo vụ việc cho chính quyền địa phương trước\n"
            "• 🔍 Mọi chi tiết vụ việc sẽ được công khai\n"
            "• 💰 Phần thưởng được giữ trong ký quỹ cho đến khi được xác minh\n"
            "• ⚠️ PeopleTrace không chịu trách nhiệm về việc lạm dụng hoặc hậu quả từ bên thứ ba\n"
            "• ❗️Báo cáo sai, nội dung xúc phạm hoặc ý định bất hợp pháp sẽ dẫn đến việc bị cấm vĩnh viễn và hành động pháp lý\n\n"
            "*Bạn có đồng ý với các điều khoản này không?*"
        ),
        "create_case_title": "Chi Tiết Vụ Việc",
        "enter_person_name": "👤 Nhập tên đầy đủ của người bạn đang tìm kiếm:",
        "male_option": "♂ Nam",
        "female_option": "♀ Nữ",
        "other_option": "Khác",
        "gender": "⚧️ Giới tính:",
        "valid_age": "Vui lòng nhập một số hợp lệ cho tuổi.",
        "age": "🎂 Tuổi (hoặc khoảng tuổi):",
        "hair_color": "🧑 Màu tóc:",
        "eye_color": "👁️ Màu mắt:",
        "height": "📏 Chiều cao (cm):",
        "weight": "⚖️ Cân nặng (kg)",
        "relationship": "🤝 Mối quan hệ của bạn với người này là gì?",
        "upload_photo": "📸 Tải lên một bức ảnh rõ ràng và mới nhất (Tối đa 5MB):",
        "no_photo_found": "Không tìm thấy ảnh. Vui lòng tải lên tệp hình ảnh hợp lệ.",
        "enter_valid_height": "Vui lòng nhập chiều cao hợp lệ (cm).",
        "last_seen_location": "👕 Người này mặc gì lần cuối được nhìn thấy? \n (Bao gồm loại quần áo, màu sắc, phụ kiện, giày dép, v.v.)",
        "enter_valid_weight": "Vui lòng nhập cân nặng hợp lệ (kg).",
        "distinctive_features": "🧷 Có đặc điểm ngoại hình nào nổi bật không? (hình xăm, sẹo, v.v.)",
        "reason_for_finding": "❓ Tại sao bạn muốn tìm người này?",
        "case_not_found": "Không tìm thấy vụ việc. Vui lòng thử lại.",
        "enter_reward_amount": (
            "💰 <b>Thiết Lập Phần Thưởng</b>\n\n"
            "Bạn muốn tặng phần thưởng gì cho các manh mối đã được xác minh? (tính bằng {type})"
        ),
        "reward_amount_negative": "❌ Số tiền thưởng phải lớn hơn 0. Bạn đã nhập: {0}.",
        "insufficient_balance": "🚫 Số dư không đủ. Bạn chỉ có {0} khả dụng.",
        "refresh_wallet_balance": "🔄 Vui lòng làm mới số dư ví của bạn hoặc giảm phần thưởng.",
        "reward_amount_confirmed": (
            "💸 Số tiền thưởng {0} đã được xác nhận.\n\n"
            "🔒 Đang kiểm tra số dư ví của bạn..."
        ),
        "insufficient_balance_for_transfer": (
            "🚫 <b>Số dư không đủ</b>\n\n"
            "Ví của bạn chỉ có <b>{wallet_balance} {wallet_type}</b>.\n"
            "Số tiền thưởng là <b>{reward_amount} {wallet_type}</b>.\n"
            "Vui lòng đảm bảo ví của bạn có đủ số dư để tiếp tục."
        ),
        "congratulates_advertiser": (
            "🎉 <b>Xin chúc mừng!</b>\n\n"
            "Phần thưởng <b>{reward_amount} {wallet_type}</b> của bạn đã được chuyển thành công đến nền tảng của chúng tôi.\n\n"
            "📝 <b>Tóm Tắt Vụ Việc:</b>\n"
            "👤 <b>Tên Vụ Việc:</b> {case_name}\n"
            "📍 <b>Địa điểm:</b> {location}\n"
            "🎁 <b>Phần Thưởng Được Tặng:</b> {reward_amount} {wallet_type}\n"
            "💸 <b>Phí Nền Tảng (5%):</b> {platform_fee} {wallet_type}\n"
            "🔒 <b>Số tiền ròng được giữ trong ký quỹ:</b> {net_amount} {wallet_type}\n\n"
            "🙌 Chúng tôi đã ghi nhận vụ việc của bạn và phần thưởng đã được chuyển đến ví của chủ sở hữu bot.\n"
            "🛡️ <b>Phần thưởng của bạn được giữ an toàn trong ký quỹ</b> và sẽ chỉ được giải ngân khi có manh mối được xác minh và thành công.\n\n"
            "🚀 Cảm ơn bạn đã là một phần của nền tảng của chúng tôi!"
        ),
        "owner_message": (
            "📢 <b>Chuyển Phần Thưởng Mới Đã Hoàn Tất</b>\n\n"
            "🆔 <b>ID Người Dùng:</b> <code>{user_id}</code>\n"
            "📄 <b>ID Vụ Việc:</b> <code>{case.id}</code>\n"
            "💰 <b>Số tiền:</b> {reward_amount} {wallet_type}\n"
            "🔐 <b>Ví:</b> <code>{wallet.public_key}</code>\n"
            "🏷️ <b>Tên Ví:</b> {wallet.name}\n\n"
            "✅ <b>Trạng thái:</b> Chuyển phần thưởng thành công.\n"
            "🔍 Sử dụng /listing để xem tất cả các vụ việc đang hoạt động."
        ),
        "transaction_failed": "❌ <b>Chuyển tiền thất bại</b>\n\nĐã xảy ra sự cố khi xử lý chuyển tiền thưởng. Vui lòng thử lại sau.",
        "transfer_failed": "Chuyển tiền thất bại. Vui lòng thử lại.",
        "transfer_canceled": "Giao dịch đã bị hủy.",
        "enter_reward_amount_unknown": "Vui lòng nhập số tiền thưởng (loại ví không xác định).",
        "reward_amount_invalid": "❌ Vui lòng nhập số tiền thưởng hợp lệ.",
        "finder_disclaimer": (
            "📜 *Trước Khi Tiếp Tục – Vui Lòng Đọc Kỹ*\n\n"
            "Bằng việc tham gia với tư cách là *Người Tìm Kiếm* trên PeopleTrace, bạn đồng ý với các điều sau:\n\n"
            "• 🔍 Bạn chỉ sử dụng nền tảng này để hỗ trợ tìm người mất tích một cách hợp pháp\n"
            "• 📹 Bằng chứng phải có hình ảnh/video xác thực được\n"
            "• 💬 Giao tiếp với người đăng tin phải tôn trọng và đúng đạo đức\n"
            "• 🧾 Không dùng nội dung giả mạo, tạo bởi AI hoặc gây hiểu lầm\n"
            "• 📍 Bạn có thể bị yêu cầu cung cấp bằng chứng bổ sung hoặc vị trí cụ thể\n"
            "• 💸 Phí nền tảng 5% sẽ được trừ từ số tiền thưởng thành công\n"
            "• 🚫 Hành vi lạm dụng, đe dọa hoặc đáng ngờ sẽ dẫn đến cấm vĩnh viễn và xử lý pháp lý\n"
            "• ❗ Chúng tôi có quyền từ chối các yêu cầu không xác thực hoặc sai sự thật\n\n"
            "*Bạn có đồng ý với các điều khoản này không?*"
        ),
        "enter_name": "Nhập tên của bạn:",
        "reward_too_low_tip": (
            "💸 <b>Phần thưởng được đặt thành {amount} {type}</b>\n\n"
            "💡 <b>Mẹo:</b> Phần thưởng càng cao, bạn càng thu hút được nhiều sự chú ý!\n"
            "Việc đưa ra một phần thưởng hậu hĩnh sẽ thúc đẩy nhiều người tham gia tìm kiếm hơn — "
            "tăng cơ hội tìm thấy người đó nhanh hơn. 🕵️‍♂️💬\n"
            "Một chút bổ sung có thể giúp tập hợp một đám đông mạnh mẽ ủng hộ vụ việc của bạn."
        ),
        "cancel_edit_button": "❌ Hủy / Chỉnh sửa",
        "increase_reward_button": "💰 Tăng phần thưởng",
        "back_button": "🔙 Quay lại",
        "enter_reward_amount_usdt": "Vui lòng nhập số tiền thưởng bằng USDT.",
        "transfer_successful": "Chuyển tiền thành công.",
        "transfer_error": "Đã xảy ra lỗi khi xử lý giao dịch. Vui lòng thử lại.",
        "invalid_confirmation": "Phản hồi không hợp lệ. Vui lòng xác nhận bằng 'có' hoặc 'không'.",
        "enter_reason_for_finding": "Vui lòng nhập lý do tìm kiếm.",
        "case_submitted": "Hồ sơ của bạn đã được gửi thành công.",
        "case_completed": "Hồ sơ của bạn đã hoàn tất.",
        "choose_existing_mobile": "Vui lòng chọn số hiện có hoặc thêm số mới.",
        "tac_invalid": "❌ Mã xác nhận không hợp lệ. Vui lòng thử lại.",
        "wallet_name_empty": "Tên ví không thể trống. Vui lòng thử lại.",
        "wallet_name_exists": "❌ Một ví cùng tên đã tồn tại. Vui lòng chọn tên khác.",
        "wallet_create_details": (
            "✅ Ví đã được tạo!\n"
            "🧾 Tên: {name}\n"
            "💰 Loại: {wallet_type}\n"
            "🔐 Khóa Công Khai: <code>{public_key}</code>\n"
            "🌐 Mạng lưới: {network}\n"
        ),
        "mobile_number_doesnt_exist": "Số điện thoại di động bạn nhập không tồn tại. Vui lòng thử lại.",
        "invalid_choice": "⚠️ <b>Lựa Chọn Không Hợp Lệ</b>\n\nVui lòng chọn tùy chọn hợp lệ.",
        "mobile_selected_with_tac": "Số điện thoại bạn nhập đã được xác minh. Vui lòng nhập mã xác nhận:",
        "enter_valid_mobile": "❌ Số điện thoại không hợp lệ. Vui lòng nhập số 10 chữ số đúng.",
        "wallet_create_err": "Đã xảy ra lỗi khi tạo ví. Vui lòng thử lại.",
        "wallet_name_prompt": "Vui lòng nhập tên cho ví {wallet_type} của bạn:",
        "wallet_create_details_with_balance": (
            "✅ Ví đã được tạo!\n"
            "🧾 Tên: {name}\n"
            "💰 Loại: {wallet_type}\n"
            "🔐 Khóa Công Khai: <code>{public_key}</code>\n"
            "🌐 Mạng lưới: {network}\n"
            "💵 Số dư: {balance} {wallet_type}\n"
        ),
        "understood_and_agree": "✅ Tôi Hiểu Và Đồng Ý",
    },
}
