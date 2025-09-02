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
        "enter_person_name": "👤 Enter the full name of the person you're looking for:",
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
        "reward_setup_prompt_usdt": (
            "💰 <b>Reward Setup</b>\n\n"
            "What reward would you like to offer for verified leads? (in USDT)"
        ),
        "reward_amount_negative": "❌ Reward amount must be greater than 0. You entered: {0}.",
        "insufficient_balance": "🚫 Insufficient Balance. You have only {0} available.",
        "refresh_wallet_balance": "🔄 Please refresh your wallet balance or lower the reward.",
        "reward_amount_confirmed": (
            "💸 Reward amount of {0} has been confirmed.\n\n"
            "🔒 Your wallet balance is being checked..."
        ),
        "reward_set_with_tip": (
            "💸 Reward set to <b>{amount} USDT</b>\n\n"
            "💡 <b>Tip:</b> The higher the reward, the more eyes you attract!\n"
            "Offering a generous reward motivates more people to join the search — "
            "increasing your chances of finding the person faster. 🕵️‍♂️💬\n"
            "A little extra can go a long way in rallying a powerful crowd behind your case."
        ),
        "insufficient_balance_detailed": (
            "🚫 <b>Insufficient Balance</b>\n\n"
            "⚠️ Your current balance is <b>{wallet_balance} USDT</b>.\n"
            "To continue, you'll need to fund your wallet with <b>{reward_amount} USDT</b>.\n\n"
            "🔐 <b>Your Wallet Address:</b>\n"
            "<code>{wallet_address}</code>\n\n"
            "🌐 <b>Network:</b> TRC20 (Tron Network)\n\n"
            "📥 <b>To top up:</b>\n\n"
            "1️⃣ Open your crypto wallet\n"
            "2️⃣ Select <b>Send</b>\n"
            "3️⃣ Paste your wallet address\n"
            "4️⃣ Select the correct network (TRC20)\n"
            "5️⃣ Enter amount and confirm\n\n"
            "🔁 Once you've completed the transfer, press <b>Refresh</b> to update your balance."
        ),
        "case_ready_to_publish": (
            "🔒 Your wallet balance is being checked...\n\n"
            "Once the balance is confirmed, your case will be published and shared with the PeopleTrace community."
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
            "🙌 We've lodged your case and the reward has been moved to the bot owner's wallet.\n"
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
        "refresh_button": "🔄 Refresh",
        "submit_case_button": "📤 Submit Case", 
        "edit_button": "🔁 Edit",
        "cancel_button": "❌ Cancel",
        "increase_reward_btn": "💰 Increase Reward",
        "back_btn": "🔙 Back",
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
        "reward_setup_prompt_usdt": (
            "💰 <b>奖励设置</b>\n\n"
            "您希望为已验证的线索提供多少奖励？（以 USDT 计算）"
        ),
        "reward_amount_negative": "❌ 奖励金额必须大于 0。您输入的是：{0}。",
        "insufficient_balance": "🚫 余额不足。您当前可用余额为 {0}。",
        "refresh_wallet_balance": "🔄 请刷新您的钱包余额或降低奖励金额。",
        "reward_amount_confirmed": (
            "💸 奖励金额 {0} 已确认。\n\n"
            "🔒 正在检查您的钱包余额..."
        ),
        "reward_set_with_tip": (
            "💸 奖励设置为 <b>{amount} USDT</b>\n\n"
            "💡 <b>提示：</b> 奖励越高，吸引的关注就越多！\n"
            "提供丰厚的奖励能激励更多人加入搜索 — "
            "增加您更快找到目标的机会。🕵️‍♂️💬\n"
            "一点额外的奖励就能为您的案件争取到强大的支持。"
        ),
        "insufficient_balance_detailed": (
            "🚫 <b>余额不足</b>\n\n"
            "⚠️ 您当前余额为 <b>{wallet_balance} USDT</b>。\n"
            "要继续，您需要向钱包充值 <b>{reward_amount} USDT</b>。\n\n"
            "🔐 <b>您的钱包地址：</b>\n"
            "<code>{wallet_address}</code>\n\n"
            "🌐 <b>网络：</b> TRC20 (Tron Network)\n\n"
            "📥 <b>充值步骤：</b>\n\n"
            "1️⃣ 打开您的加密钱包\n"
            "2️⃣ 选择 <b>发送</b>\n"
            "3️⃣ 粘贴您的钱包地址\n"
            "4️⃣ 选择正确的网络 (TRC20)\n"
            "5️⃣ 输入金额并确认\n\n"
            "🔁 完成转账后，请按 <b>刷新</b> 更新您的余额。"
        ),
        "case_ready_to_publish": (
            "🔒 正在检查您的钱包余额...\n\n"
            "余额确认后，您的案件将发布并与 PeopleTrace 社区分享。"
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
        "refresh_button": "🔄 刷新",
        "submit_case_button": "📤 提交案件",
        "edit_button": "🔁 编辑",
        "cancel_button": "❌ 取消",
        "increase_reward_btn": "💰 增加奖励",
        "back_btn": "🔙 返回",
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
    # Adding other languages with the new constants for brevity - in a real implementation,
    # you would add all the other language translations here
}