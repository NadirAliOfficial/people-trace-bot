LISTING_CONSTANT = {
    "en": {
        "no_advertise_cases": "No ADVERTISE cases found.",
        "select_case_details": "📋 **Select a Case to View Details:**",
        "case_not_found": "❌ Case not found.",
        "error_fetching_cases": "An error occurred while fetching cases.",
        "error_fetching_case_details": "❌ An error occurred while fetching case details.",
        "error_paginating_cases": "❌ An error occurred while paginating cases.",
        "invalid_case_id": "❌ Invalid case ID.",
        "not_authorized_edit": "❌ You are not authorized to edit this case.",
        "not_authorized_delete": "❌ You are not authorized to delete this case.",
        "case_deleted_successfully": "✅ Case has been successfully deleted.",
        "edit_canceled": "📋 Edit canceled. Returning to case listing.",
        "enter_new_value": "✏️ Please enter the new value for **{field_name}**: ",
        "field_updated_successfully": "✅ **{field_name}** updated to: **{new_value}**",
        "invalid_value": "❌ {error_message} Please enter a valid value.",
        "edit_field_prompt": "📝 **Which field would you like to edit?**",
        "cancel_edit_button": "❌ Cancel",
        "edit_button": "📝 Edit",
        "delete_button": "🗑 Delete",
        "previous_button": "⬅️ Previous",
        "next_button": "➡️ Next",
        "editable_fields": {
            "Name": "name",
            "Person Name": "person_name",
            "Relationship": "relationship",
            "Last Seen Location": "last_seen_location",
            "Gender": "gender",
            "Age": "age",
            "Hair Color": "hair_color",
            "Eye Color": "eye_color",
            "Height": "height",
            "Weight": "weight",
            "Distinctive Features": "distinctive_features",
            "Country": "country",
            "City": "city",
        },
        "insurfficient_balance": (
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
        "case_details_template": (
            "📌 *Case Details*\n"
            "👤 *Name:* {person_name}\n"
            "📍 *Last Seen Location:* {last_seen_location}\n"
            "📆 *Date:* {last_seen_date}\n"
            "🎂 *Age:* {age}\n"
            "💰 *Reward:* {reward} {reward_type}\n"
            # "🧾 *Posted by:* @{poster_username}\n"
            "📏 *Height:* {height} cm\n"
        ),
        "transfer_failed": "❌ <b>Transfer Failed</b>\n\nSomething went wrong while processing the reward transfer. Please try again later.",
        "invalid_reward_amount": "❌ Invalid reward amount. Maximum reward amount is {max_amount}.",
        "reward_success": "✅ Reward successfully sent to finder {finder_id}.",
        "error_transferring_reward": "❌ An error occurred while transferring reward.",
        "case_or_finder_not_found": "❌ Case or finder not found.",
        "no_finders_for_case": "❌ No finders found for this case.",
        "finder_list_header": "👤 **Finders for this case:**",
        "reward_this_finder": "💰 Reward this finder",
        "enter_reward_amount": "✏️ Please enter the reward amount for this case (max {max_amount}): ",
        "reward_confirmation": "Are you sure you want to send {amount} reward to Finder ID {finder_id} for Case {case_no}?",
        "reward_cancelled": "Reward process cancelled",
        "confirm_button": "✅ Confirm",
        "cancel_button": "❌ Cancel",
        "case_not_found": "⚠️ Case not found.",
        "not_authorized_delete": "🚫 You are not authorized to delete this case.",
        "case_deleted_successfully": "✅ Case has been successfully deleted.",
        "confirm_delete": "❗ Are you sure you want to delete this case?",
        "yes": "✅ Yes",
        "no": "❌ No",
        "delete_cancelled": "❌ Case deletion has been cancelled.",
        "error_deleting_case": "⚠️ An error occurred while deleting the case. Please try again.",
        "extend_reward_button": "Extend Reward ➕",
        "extend_reward_not_found": "❌ No active reward extension request found.",
        "insufficient_funds": "❌ Insufficient funds in your {wallet_type} wallet. Required: {required_amount}",
        "extend_reward_confirmation": (
            "🔄 *Confirm Reward Extension*\n\n"
            "💰 Amount: {amount} {wallet_type}\n"
            "📤 From: `{from_wallet}`\n"
            "📥 To: `{to_wallet}`\n"
            "Are you sure you want to proceed?"
        ),
        "extend_success": "✅ Successfully extended {amount} {wallet_type} reward!",
        "extend_cancelled": "❌ Reward extension cancelled.",
        "transfer_failed": "❌ Transfer failed. Please check wallet balances and try again.",
        "case_or_extend_not_found": "❌ Case or extension request not found.",
        "no_wallet_found": "❌ No wallets found for the selected type.",
        "insufficient_funds_after_selection": "❌ Insufficient funds in the selected wallet.",
        "extend_already_completed": "⚠️ This extend reward request has already been completed.",
        "error_processing_extend": "❌ An error occurred while processing the extend reward request.",
        "error_approving_extend": "❌ An error occurred while approving the extend reward request.",
        "case_not_found": "❌ Case not found.",
        "extend_reward_not_found": "❌ No pending extend reward requests found for this case.",
        "select_wallet_for_extend": (
            "🔄 *Select Wallet for Reward Extension*\n\n"
            "💰 Amount: {amount} {wallet_type}\n"
            "📤 From: `{from_wallet}`\n"
            "📥 To: `{to_wallet}`\n\n"
            "Please select a wallet from the options below:"
        ),
    },
    "zh": {
        "no_advertise_cases": "未找到任何广告案件。",
        "select_case_details": "📋 **选择一个案件查看详情：**",
        "case_not_found": "❌ 案件未找到。",
        "error_fetching_cases": "获取案件时发生错误。",
        "error_fetching_case_details": "❌ 获取案件详情时出错。",
        "error_paginating_cases": "❌ 分页加载案件时出错。",
        "invalid_case_id": "❌ 无效的案件ID。",
        "not_authorized_edit": "❌ 您无权编辑此案件。",
        "not_authorized_delete": "❌ 您无权删除此案件。",
        "case_deleted_successfully": "✅ 案件已成功删除。",
        "edit_canceled": "📋 编辑已取消，返回案件列表。",
        "enter_new_value": "✏️ 请输入新的 **{field_name}** 值：",
        "field_updated_successfully": "✅ **{field_name}** 已更新为：**{new_value}**",
        "invalid_value": "❌ {error_message} 请输入有效值。",
        "edit_field_prompt": "📝 **您想编辑哪个字段？**",
        "cancel_edit_button": "❌ 取消",
        "edit_button": "📝 编辑",
        "delete_button": "🗑 删除",
        "previous_button": "⬅️ 上一页",
        "next_button": "➡️ 下一页",
        "editable_fields": {
            "姓名": "name",
            "人员姓名": "person_name",
            "关系": "relationship",
            "最后出现地点": "last_seen_location",
            "性别": "gender",
            "年龄": "age",
            "发色": "hair_color",
            "眼睛颜色": "eye_color",
            "身高": "height",
            "体重": "weight",
            "显著特征": "distinctive_features",
            "国家": "country",
            "城市": "city",
        },
        "insurfficient_balance": (
            "🚫 <b>余额不足</b>\n\n"
            "您的钱包中只有 <b>{wallet_balance} {wallet_type}</b>。\n"
            "所需奖励金额为 <b>{reward_amount} {wallet_type}</b>。\n"
            "请确保您的钱包中有足够的余额。"
        ),
        "congratulates_advertiser": (
            "🎉 <b>恭喜！</b>\n\n"
            "您的奖励金额 <b>{reward_amount} {wallet_type}</b> 已成功转入平台。\n\n"
            "📝 <b>案件概要：</b>\n"
            "👤 <b>案件名称：</b> {case_name}\n"
            "📍 <b>地点：</b> {location}\n"
            "🎁 <b>提供奖励：</b> {reward_amount} {wallet_type}\n"
            "💸 <b>平台费用（5%）：</b> {platform_fee} {wallet_type}\n"
            "🔒 <b>托管净额：</b> {net_amount} {wallet_type}\n\n"
            "🙌 您的案件已提交，奖励已转移至机器人拥有者钱包。\n"
            "🛡️ <b>您的奖励已安全托管</b>，仅在验证成功后释放。\n\n"
            "🚀 感谢您加入我们的平台！"
        ),
        "owner_message": (
            "📢 <b>新奖励转账已完成</b>\n\n"
            "🆔 <b>用户ID：</b> <code>{user_id}</code>\n"
            "📄 <b>案件ID：</b> <code>{case.id}</code>\n"
            "💰 <b>金额：</b> {reward_amount} {wallet_type}\n"
            "🔐 <b>钱包地址：</b> <code>{wallet.public_key}</code>\n"
            "🏷️ <b>钱包名称：</b> {wallet.name}\n\n"
            "✅ <b>状态：</b> 奖励转账成功。\n"
            "🔍 使用 /listing 查看所有活动案件。"
        ),
        "case_details_template": (
            "📌 *案件详情*\n"
            "👤 *姓名:* {person_name}\n"
            "📍 *最后出现地点:* {last_seen_location}\n"
            "📆 *日期:* {last_seen_date}\n"
            "🎂 *年龄:* {age}\n"
            "💰 *奖励:* {reward} {reward_type}\n"
            "📏 *身高:* {height} 厘米\n"
        ),
        "transfer_failed": "❌ <b>转账失败</b>\n\n处理奖励转账时出错，请稍后再试。",
        "invalid_reward_amount": "❌ 无效的奖励金额。最大奖励金额为 {max_amount}。",
        "reward_success": "✅ 奖励已成功发送给发现者 {finder_id}。",
        "error_transferring_reward": "❌ 转账奖励时出错。",
        "case_or_finder_not_found": "❌ 案件或发现者未找到。",
        "no_finders_for_case": "❌ 此案件没有发现者。",
        "finder_list_header": "👤 **本案件的发现者：**",
        "reward_this_finder": "💰 奖励该发现者",
        "enter_reward_amount": "✏️ 请输入本案件的奖励金额（最高 {max_amount}）：",
        "reward_confirmation": "您确定要向发现者 {finder_id} 发送 {amount} 的奖励吗？案件编号：{case_no}",
        "reward_cancelled": "奖励流程已取消",
        "confirm_button": "✅ 确认",
        "cancel_button": "❌ 取消",
        "case_not_found": "⚠️ 案件未找到。",
        "not_authorized_delete": "🚫 您无权删除此案件。",
        "case_deleted_successfully": "✅ 案件已成功删除。",
        "confirm_delete": "❗ 您确定要删除此案件吗？",
        "yes": "✅ 是",
        "no": "❌ 否",
        "delete_cancelled": "❌ 案件删除已取消。",
        "error_deleting_case": "⚠️ 删除案件时出错。请重试。",
        "extend_reward_button": "延长奖励 ➕",
        "extend_reward_not_found": "❌ 未找到待处理的延长请求。",
        "insufficient_funds": "❌ 您的 {wallet_type} 钱包资金不足。需要：{required_amount}",
        "extend_reward_confirmation": (
            "🔄 *确认奖励延长*\n\n"
            "💰 金额：{amount} {wallet_type}\n"
            "📤 来自：`{from_wallet}`\n"
            "📥 到：`{to_wallet}`\n"
            "您确定要继续吗？"
        ),
        "extend_success": "✅ 成功延长奖励 {amount} {wallet_type}！",
        "extend_cancelled": "❌ 奖励延长已取消。",
        "transfer_failed": "❌ 转账失败。请检查钱包余额并重试。",
        "case_or_extend_not_found": "❌ 案件或延长请求未找到。",
        "no_wallet_found": "❌ 未找到所选类型的可用钱包。",
        "insufficient_funds_after_selection": "❌ 所选钱包资金不足。",
        "extend_already_completed": "⚠️ 此延长请求已完成。",
        "error_processing_extend": "❌ 处理延长请求时出错。",
        "error_approving_extend": "❌ 审批延长请求时出错。",
        "case_not_found": "❌ 案件未找到。",
        "extend_reward_not_found": "❌ 本案件无待处理的延长奖励请求。",
        "select_wallet_for_extend": (
            "🔄 *请选择用于奖励延长的钱包*\n\n"
            "💰 金额：{amount} {wallet_type}\n"
            "📤 来自：`{from_wallet}`\n"
            "📥 到：`{to_wallet}`\n\n"
            "请从下方选项中选择一个钱包："
        ),
    },
    "ms": {
        "no_advertise_cases": "Tiada kes iklan dijumpai.",
        "select_case_details": "📋 **Pilih satu kes untuk melihat butiran:**",
        "case_not_found": "❌ Kes tidak dijumpai.",
        "error_fetching_cases": "Ralat berlaku semasa mengambil kes.",
        "error_fetching_case_details": "❌ Ralat berlaku semasa mengambil butiran kes.",
        "error_paginating_cases": "❌ Ralat berlaku semasa membuat penomboran halaman kes.",
        "invalid_case_id": "❌ ID kes tidak sah.",
        "not_authorized_edit": "❌ Anda tidak dibenarkan untuk mengedit kes ini.",
        "not_authorized_delete": "❌ Anda tidak dibenarkan untuk memadam kes ini.",
        "case_deleted_successfully": "✅ Kes telah berjaya dipadam.",
        "edit_canceled": "📋 Pengeditan dibatalkan. Kembali ke senarai kes.",
        "enter_new_value": "✏️ Sila masukkan nilai baru untuk **{field_name}**: ",
        "field_updated_successfully": "✅ **{field_name}** dikemaskini kepada: **{new_value}**",
        "invalid_value": "❌ {error_message} Sila masukkan nilai yang sah.",
        "edit_field_prompt": "📝 **Medan mana yang ingin anda edit?**",
        "cancel_edit_button": "❌ Batal",
        "edit_button": "📝 Edit",
        "delete_button": "🗑 Padam",
        "previous_button": "⬅️ Sebelumnya",
        "next_button": "➡️ Seterusnya",
        "editable_fields": {
            "Nama": "name",
            "Nama Orang": "person_name",
            "Hubungan": "relationship",
            "Lokasi Terakhir Dilihat": "last_seen_location",
            "Jantina": "gender",
            "Umur": "age",
            "Warna Rambut": "hair_color",
            "Warna Mata": "eye_color",
            "Ketinggian": "height",
            "Berat Badan": "weight",
            "Ciri-ciri Khas": "distinctive_features",
            "Negara": "country",
            "Bandar": "city",
        },
        "insurfficient_balance": (
            "🚫 <b>Imbangan Tidak Mencukupi</b>\n\n"
            "Dompet anda hanya mempunyai <b>{wallet_balance} {wallet_type}</b>.\n"
            "Jumlah ganjaran ialah <b>{reward_amount} {wallet_type}</b>.\n"
            "Pastikan dompet anda mencukupi untuk meneruskan."
        ),
        "congratulates_advertiser": (
            "🎉 <b>Tahniah!</b>\n\n"
            "Ganjaran sebanyak <b>{reward_amount} {wallet_type}</b> telah berjaya dipindahkan ke platform kami.\n\n"
            "📝 <b>Ringkasan Kes:</b>\n"
            "👤 <b>Nama Kes:</b> {case_name}\n"
            "📍 <b>Lokasi:</b> {location}\n"
            "🎁 <b>Ganjaran Ditawarkan:</b> {reward_amount} {wallet_type}\n"
            "💸 <b>Yuran Platform (5%):</b> {platform_fee} {wallet_type}\n"
            "🔒 <b>Jumlah Ganjaran dalam Escrow:</b> {net_amount} {wallet_type}\n\n"
            "🙌 Kami telah menyimpan kes anda dan ganjaran telah dipindahkan ke dompet pemilik bot.\n"
            "🛡️ <b>Ganjaran anda disimpan dengan selamat</b> dan hanya akan dikeluarkan apabila kejayaan pengesahan diterima.\n\n"
            "🚀 Terima kasih kerana menjadi sebahagian daripada platform kami!"
        ),
        "owner_message": (
            "📢 <b>Pemindahan Ganjaran Baru Telah Diselesaikan</b>\n\n"
            "🆔 <b>ID Pengguna:</b> <code>{user_id}</code>\n"
            "📄 <b>ID Kes:</b> <code>{case.id}</code>\n"
            "💰 <b>Jumlah:</b> {reward_amount} {wallet_type}\n"
            "🔐 <b>Dompet:</b> <code>{wallet.public_key}</code>\n"
            "🏷️ <b>Nama Dompet:</b> {wallet.name}\n\n"
            "✅ <b>Status:</b> Ganjaran berjaya dipindahkan.\n"
            "🔍 Gunakan /listing untuk melihat semua kes aktif."
        ),
        "case_details_template": (
            "📌 *Butiran Kes*\n"
            "👤 *Nama:* {person_name}\n"
            "📍 *Lokasi Akhir Dijumpai:* {last_seen_location}\n"
            "📆 *Tarikh:* {last_seen_date}\n"
            "🎂 *Umur:* {age}\n"
            "💰 *Ganjaran:* {reward} {reward_type}\n"
            "📏 *Tinggi:* {height} cm\n"
        ),
        "transfer_failed": "❌ <b>Pemindahan Gagal</b>\n\nRalat berlaku semasa memproses pemindahan ganjaran. Sila cuba lagi nanti.",
        "invalid_reward_amount": "❌ Jumlah ganjaran tidak sah. Jumlah maksimum ialah {max_amount}.",
        "reward_success": "✅ Ganjaran berjaya dihantar kepada pencari {finder_id}.",
        "error_transferring_reward": "❌ Ralat berlaku semasa memindahkan ganjaran.",
        "case_or_finder_not_found": "❌ Kes atau pencari tidak dijumpai.",
        "no_finders_for_case": "❌ Tiada pencari dijumpai untuk kes ini.",
        "finder_list_header": "👤 **Pencari untuk kes ini:**",
        "reward_this_finder": "💰 Ganjar pencari ini",
        "enter_reward_amount": "✏️ Sila masukkan jumlah ganjaran untuk kes ini (maksimum {max_amount}): ",
        "reward_confirmation": "Adakah anda pasti ingin menghantar ganjaran sebanyak {amount} kepada Pencari ID {finder_id} untuk Kes {case_no}?",
        "reward_cancelled": "Proses ganjaran dibatalkan",
        "confirm_button": "✅ Sahkan",
        "cancel_button": "❌ Batal",
        "case_not_found": "⚠️ Kes tidak dijumpai.",
        "not_authorized_delete": "🚫 Anda tidak dibenarkan untuk memadam kes ini.",
        "case_deleted_successfully": "✅ Kes telah berjaya dipadam.",
        "confirm_delete": "❗ Adakah anda pasti ingin memadam kes ini?",
        "yes": "✅ Ya",
        "no": "❌ Tidak",
        "delete_cancelled": "❌ Pemadaman kes telah dibatalkan.",
        "error_deleting_case": "⚠️ Ralat berlaku semasa memadam kes. Sila cuba lagi.",
        "extend_reward_button": "Lanjut Ganjaran ➕",
        "extend_reward_not_found": "❌ Tiada permintaan lanjutan ganjaran aktif dijumpai.",
        "insufficient_funds": "❌ Dana tidak mencukupi di dalam dompet {wallet_type} anda. Diperlukan: {required_amount}",
        "extend_reward_confirmation": (
            "🔄 *Sahkan Lanjutan Ganjaran*\n\n"
            "💰 Jumlah: {amount} {wallet_type}\n"
            "📤 Dari: `{from_wallet}`\n"
            "📥 Ke: `{to_wallet}`\n"
            "Adakah anda pasti ingin meneruskannya?"
        ),
        "extend_success": "✅ Berjaya melanjutkan ganjaran sebanyak {amount} {wallet_type}!",
        "extend_cancelled": "❌ Lanjutan ganjaran dibatalkan.",
        "transfer_failed": "❌ Pemindahan gagal. Sila semak baki dompet dan cuba lagi.",
        "case_or_extend_not_found": "❌ Kes atau permintaan lanjutan tidak dijumpai.",
        "no_wallet_found": "❌ Tiada dompet dijumpai untuk jenis terpilih.",
        "insufficient_funds_after_selection": "❌ Dana tidak mencukupi di dalam dompet terpilih.",
        "extend_already_completed": "⚠️ Permintaan lanjutan ganjaran ini sudah selesai.",
        "error_processing_extend": "❌ Ralat berlaku semasa memproses permintaan lanjutan ganjaran.",
        "error_approving_extend": "❌ Ralat berlaku semasa meluluskan permintaan lanjutan ganjaran.",
        "case_not_found": "❌ Kes tidak dijumpai.",
        "extend_reward_not_found": "❌ Tiada permintaan lanjutan ganjaran tertunggu dijumpai untuk kes ini.",
        "select_wallet_for_extend": (
            "🔄 *Pilih Dompet untuk Lanjutan Ganjaran*\n\n"
            "💰 Jumlah: {amount} {wallet_type}\n"
            "📤 Dari: `{from_wallet}`\n"
            "📥 Ke: `{to_wallet}`\n\n"
            "Sila pilih dompet dari pilihan di bawah:"
        ),
    },
    "th": {
        "no_advertise_cases": "ไม่พบคดีประเภทโฆษณา",
        "select_case_details": "📋 **เลือกเคสเพื่อดูรายละเอียด:**",
        "case_not_found": "❌ ไม่พบเคส",
        "error_fetching_cases": "เกิดข้อผิดพลาดขณะโหลดรายการเคส",
        "error_fetching_case_details": "❌ เกิดข้อผิดพลาดขณะโหลดรายละเอียดเคส",
        "error_paginating_cases": "❌ เกิดข้อผิดพลาดขณะเปลี่ยนหน้าของรายการเคส",
        "invalid_case_id": "❌ ID เคอสไม่ถูกต้อง",
        "not_authorized_edit": "❌ คุณไม่มีสิทธิ์แก้ไขเคสนี้",
        "not_authorized_delete": "❌ คุณไม่มีสิทธิ์ลบเคสนี้",
        "case_deleted_successfully": "✅ เคสได้รับการลบเรียบร้อยแล้ว",
        "edit_canceled": "📋 การแก้ไขถูกยกเลิก กลับไปที่รายการเคส",
        "enter_new_value": "✏️ กรุณากรอกค่าใหม่สำหรับ **{field_name}**: ",
        "field_updated_successfully": "✅ **{field_name}** ได้รับการอัปเดตเป็น: **{new_value}**",
        "invalid_value": "❌ {error_message} กรุณากรอกค่าที่ถูกต้อง",
        "edit_field_prompt": "📝 **คุณต้องการแก้ไขฟิลด์ใด?**",
        "cancel_edit_button": "❌ ยกเลิก",
        "edit_button": "📝 แก้ไข",
        "delete_button": "🗑 ลบ",
        "previous_button": "⬅️ ก่อนหน้า",
        "next_button": "➡️ ถัดไป",
        "editable_fields": {
            "ชื่อ": "name",
            "ชื่อบุคคล": "person_name",
            "ความสัมพันธ์": "relationship",
            "สถานที่พบครั้งสุดท้าย": "last_seen_location",
            "เพศ": "gender",
            "อายุ": "age",
            "สีผม": "hair_color",
            "สีตา": "eye_color",
            "ความสูง": "height",
            "น้ำหนัก": "weight",
            "ลักษณะเฉพาะ": "distinctive_features",
            "ประเทศ": "country",
            "เมือง": "city",
        },
        "insurfficient_balance": (
            "🚫 <b>ยอดเงินไม่เพียงพอ</b>\n\n"
            "กระเป๋าเงินของคุณมีเพียง <b>{wallet_balance} {wallet_type}</b>.\n"
            "จำนวนเงินรางวัลอยู่ที่ <b>{reward_amount} {wallet_type}</b>.\n"
            "กรุณาตรวจสอบให้แน่ใจว่ากระเป๋าเงินของคุณมีเงินเพียงพอ"
        ),
        "congratulates_advertiser": (
            "🎉 <b>ยินดีด้วย!</b>\n\n"
            "รางวัลของคุณจำนวน <b>{reward_amount} {wallet_type}</b> ได้ถูกโอนเข้าระบบของเราแล้ว\n\n"
            "📝 <b>สรุปเคส:</b>\n"
            "👤 <b>ชื่อเคส:</b> {case_name}\n"
            "📍 <b>สถานที่:</b> {location}\n"
            "🎁 <b>จำนวนรางวัล:</b> {reward_amount} {wallet_type}\n"
            "💸 <b>ค่าธรรมเนียมแพลตฟอร์ม (5%):</b> {platform_fee} {wallet_type}\n"
            "🔒 <b>จำนวนสุทธิที่อยู่ใน Escrow:</b> {net_amount} {wallet_type}\n\n"
            "🙌 เราได้บันทึกเคสของคุณและรางวัลได้ถูกโอนไปยังกระเป๋าเงินของเจ้าของบอทแล้ว\n"
            "🛡️ <b>รางวัลของคุณถูกเก็บไว้อย่างปลอดภัย</b> และจะปล่อยออกมาเมื่อมีหลักฐานที่ยืนยันแล้วเท่านั้น\n\n"
            "🚀 ขอบคุณที่เป็นส่วนหนึ่งของแพลตฟอร์มของเรา!"
        ),
        "owner_message": (
            "📢 <b>การโอนรางวัลใหม่เสร็จสมบูรณ์</b>\n\n"
            "🆔 <b>ID ผู้ใช้งาน:</b> <code>{user_id}</code>\n"
            "📄 <b>ID เคส:</b> <code>{case.id}</code>\n"
            "💰 <b>จำนวน:</b> {reward_amount} {wallet_type}\n"
            "🔐 <b>กระเป๋าเงิน:</b> <code>{wallet.public_key}</code>\n"
            "🏷️ <b>ชื่อกระเป๋าเงิน:</b> {wallet.name}\n\n"
            "✅ <b>สถานะ:</b> โอนรางวัลสำเร็จ\n"
            "🔍 พิมพ์ /listing เพื่อดูรายการเคสทั้งหมด"
        ),
        "case_details_template": (
            "📌 *รายละเอียดเคส*\n"
            "👤 *ชื่อ:* {person_name}\n"
            "📍 *สถานที่พบครั้งสุดท้าย:* {last_seen_location}\n"
            "📆 *วันที่:* {last_seen_date}\n"
            "🎂 *อายุ:* {age}\n"
            "💰 *รางวัล:* {reward} {reward_type}\n"
            "📏 *ส่วนสูง:* {height} ซม.\n"
        ),
        "transfer_failed": "❌ <b>การโอนล้มเหลว</b>\n\nเกิดข้อผิดพลาดขณะดำเนินการโอนรางวัล กรุณาลองใหม่ภายหลัง",
        "invalid_reward_amount": "❌ จำนวนรางวัลไม่ถูกต้อง สูงสุดคือ {max_amount}",
        "reward_success": "✅ โอนรางวัลให้ผู้ค้นหา {finder_id} เรียบร้อยแล้ว",
        "error_transferring_reward": "❌ เกิดข้อผิดพลาดขณะโอนรางวัล",
        "case_or_finder_not_found": "❌ ไม่พบเคสหรือผู้ค้นหา",
        "no_finders_for_case": "❌ ไม่พบผู้ค้นหาสำหรับเคสนี้",
        "finder_list_header": "👤 **รายชื่อผู้ค้นหาสำหรับเคสนี้:**",
        "reward_this_finder": "💰 มอบรางวัลให้ผู้ค้นหาคนนี้",
        "enter_reward_amount": "✏️ กรุณากรอกจำนวนรางวัลสำหรับเคสนี้ (สูงสุด {max_amount}): ",
        "reward_confirmation": "คุณแน่ใจหรือไม่ว่าต้องการโอน {amount} เป็นรางวัลให้ผู้ค้นหา ID {finder_id} สำหรับเคส {case_no}?",
        "reward_cancelled": "ยกเลิกกระบวนการมอบรางวัล",
        "confirm_button": "✅ ยืนยัน",
        "cancel_button": "❌ ยกเลิก",
        "case_not_found": "⚠️ ไม่พบเคส",
        "not_authorized_delete": "🚫 คุณไม่มีสิทธิ์ในการลบเคสนี้",
        "case_deleted_successfully": "✅ เคสถูกลบสำเร็จ",
        "confirm_delete": "❗ คุณต้องการลบเคสนี้หรือไม่?",
        "yes": "✅ ใช่",
        "no": "❌ ไม่",
        "delete_cancelled": "❌ การลบเคสถูกยกเลิก",
        "error_deleting_case": "⚠️ เกิดข้อผิดพลาดขณะลบเคส กรุณาลองใหม่",
        "extend_reward_button": "ขยายรางวัล ➕",
        "extend_reward_not_found": "❌ ไม่พบคำขอขยายรางวัลที่ยังไม่ได้ดำเนินการ",
        "insufficient_funds": "❌ กระเป๋าเงิน {wallet_type} ของคุณมีไม่เพียงพอ จำเป็นต้องใช้ {required_amount}",
        "extend_reward_confirmation": (
            "🔄 *ยืนยันการขยายรางวัล*\n\n"
            "💰 จำนวน: {amount} {wallet_type}\n"
            "📤 จาก: `{from_wallet}`\n"
            "📥 ไปยัง: `{to_wallet}`\n"
            "คุณแน่ใจหรือว่าต้องการทำรายการนี้?"
        ),
        "extend_success": "✅ ขยายรางวัล {amount} {wallet_type} เรียบร้อยแล้ว!",
        "extend_cancelled": "❌ การขยายรางวัลถูกยกเลิก",
        "transfer_failed": "❌ การโอนล้มเหลว กรุณาตรวจสอบยอดคงเหลือและลองใหม่อีกครั้ง",
        "case_or_extend_not_found": "❌ ไม่พบเคสหรือคำขอขยายรางวัล",
        "no_wallet_found": "❌ ไม่พบกระเป๋าเงินสำหรับประเภทที่เลือก",
        "insufficient_funds_after_selection": "❌ กระเป๋าเงินที่เลือกมียอดไม่เพียงพอ",
        "extend_already_completed": "⚠️ คำขอขยายรางวัลนี้ดำเนินการเสร็จสิ้นแล้ว",
        "error_processing_extend": "❌ เกิดข้อผิดพลาดขณะประมวลผลคำขอขยายรางวัล",
        "error_approving_extend": "❌ เกิดข้อผิดพลาดขณะยืนยันคำขอขยายรางวัล",
        "case_not_found": "❌ ไม่พบเคส",
        "extend_reward_not_found": "❌ ไม่พบคำขอขยายรางวัลที่รอการดำเนินการสำหรับเคสนี้",
        "select_wallet_for_extend": (
            "🔄 *เลือกกระเป๋าเงินสำหรับขยายรางวัล*\n\n"
            "💰 จำนวน: {amount} {wallet_type}\n"
            "📤 จาก: `{from_wallet}`\n"
            "📥 ไปยัง: `{to_wallet}`\n\n"
            "กรุณาเลือกกระเป๋าเงินจากตัวเลือกด้านล่าง:"
        ),
    },
    "vi": {
        "no_advertise_cases": "Không tìm thấy trường hợp quảng cáo nào.",
        "select_case_details": "📋 **Chọn một trường hợp để xem chi tiết:**",
        "case_not_found": "❌ Không tìm thấy trường hợp này.",
        "error_fetching_cases": "Đã xảy ra lỗi khi tải danh sách trường hợp.",
        "error_fetching_case_details": "❌ Đã xảy ra lỗi khi tải chi tiết trường hợp.",
        "error_paginating_cases": "❌ Lỗi phân trang các trường hợp.",
        "invalid_case_id": "❌ Mã trường hợp không hợp lệ.",
        "not_authorized_edit": "❌ Bạn không được phép chỉnh sửa trường hợp này.",
        "not_authorized_delete": "❌ Bạn không được phép xóa trường hợp này.",
        "case_deleted_successfully": "✅ Trường hợp đã được xóa thành công.",
        "edit_canceled": "📋 Hủy chỉnh sửa. Quay lại danh sách trường hợp.",
        "enter_new_value": "✏️ Vui lòng nhập giá trị mới cho **{field_name}**: ",
        "field_updated_successfully": "✅ **{field_name}** đã được cập nhật thành: **{new_value}**",
        "invalid_value": "❌ {error_message} Vui lòng nhập giá trị hợp lệ.",
        "edit_field_prompt": "📝 **Bạn muốn chỉnh sửa trường nào?**",
        "cancel_edit_button": "❌ Hủy bỏ",
        "edit_button": "📝 Chỉnh sửa",
        "delete_button": "🗑 Xóa",
        "previous_button": "⬅️ Trước đó",
        "next_button": "➡️ Kế tiếp",
        "editable_fields": {
            "Tên": "name",
            "Tên người": "person_name",
            "Mối quan hệ": "relationship",
            "Nơi xuất hiện lần cuối": "last_seen_location",
            "Giới tính": "gender",
            "Tuổi": "age",
            "Màu tóc": "hair_color",
            "Màu mắt": "eye_color",
            "Chiều cao": "height",
            "Cân nặng": "weight",
            "Đặc điểm nổi bật": "distinctive_features",
            "Quốc gia": "country",
            "Thành phố": "city",
        },
        "insurfficient_balance": (
            "🚫 <b>Số dư không đủ</b>\n\n"
            "Ví của bạn chỉ có <b>{wallet_balance} {wallet_type}</b>.\n"
            "Số tiền thưởng là <b>{reward_amount} {wallet_type}</b>.\n"
            "Hãy đảm bảo ví của bạn có đủ số dư để tiếp tục."
        ),
        "congratulates_advertiser": (
            "🎉 <b>Chúc mừng!</b>\n\n"
            "Phần thưởng <b>{reward_amount} {wallet_type}</b> đã được chuyển thành công lên nền tảng của chúng tôi.\n\n"
            "📝 <b>Tóm tắt trường hợp:</b>\n"
            "👤 <b>Tên trường hợp:</b> {case_name}\n"
            "📍 <b>Vị trí:</b> {location}\n"
            "🎁 <b>Phần thưởng:</b> {reward_amount} {wallet_type}\n"
            "💸 <b>Lệ phí nền tảng (5%):</b> {platform_fee} {wallet_type}\n"
            "🔒 <b>Số tiền giữ trong tài khoản tạm giữ:</b> {net_amount} {wallet_type}\n\n"
            "🙌 Chúng tôi đã ghi nhận trường hợp của bạn và phần thưởng đã được chuyển vào ví của chủ sở hữu bot.\n"
            "🛡️ <b>Phần thưởng của bạn được giữ an toàn</b>, chỉ phát hành khi có bằng chứng xác minh thành công.\n\n"
            "🚀 Cảm ơn bạn đã tham gia nền tảng của chúng tôi!"
        ),
        "owner_message": (
            "📢 <b>Giao dịch thưởng mới đã hoàn tất</b>\n\n"
            "🆔 <b>ID Người dùng:</b> <code>{user_id}</code>\n"
            "📄 <b>ID Trường hợp:</b> <code>{case.id}</code>\n"
            "💰 <b>Số tiền:</b> {reward_amount} {wallet_type}\n"
            "🔐 <b>Ví:</b> <code>{wallet.public_key}</code>\n"
            "🏷️ <b>Tên ví:</b> {wallet.name}\n\n"
            "✅ <b>Trạng thái:</b> Thưởng đã được chuyển thành công.\n"
            "🔍 Dùng lệnh /listing để xem tất cả trường hợp đang hoạt động."
        ),
        "case_details_template": (
            "📌 *Thông tin chi tiết*\n"
            "👤 *Tên:* {person_name}\n"
            "📍 *Nơi xuất hiện lần cuối:* {last_seen_location}\n"
            "📆 *Ngày:* {last_seen_date}\n"
            "🎂 *Tuổi:* {age}\n"
            "💰 *Thưởng:* {reward} {reward_type}\n"
            "📏 *Chiều cao:* {height} cm\n"
        ),
        "transfer_failed": "❌ <b>Giao dịch thất bại</b>\n\nCó lỗi xảy ra khi xử lý phần thưởng. Vui lòng thử lại sau.",
        "invalid_reward_amount": "❌ Số tiền thưởng không hợp lệ. Mức tối đa là {max_amount}.",
        "reward_success": "✅ Đã gửi phần thưởng thành công cho người tìm thấy {finder_id}.",
        "error_transferring_reward": "❌ Có lỗi xảy ra khi chuyển phần thưởng.",
        "case_or_finder_not_found": "❌ Không tìm thấy trường hợp hoặc người tìm thấy.",
        "no_finders_for_case": "❌ Không có ai tìm thấy trường hợp này.",
        "finder_list_header": "👤 **Danh sách người tìm thấy:**",
        "reward_this_finder": "💰 Trả thưởng cho người này",
        "enter_reward_amount": "✏️ Nhập số tiền thưởng cho trường hợp này (tối đa {max_amount}): ",
        "reward_confirmation": "Bạn có chắc chắn muốn thưởng {amount} cho người tìm thấy ID {finder_id} với mã trường hợp {case_no}?",
        "reward_cancelled": "Đã hủy quy trình thưởng",
        "confirm_button": "✅ Xác nhận",
        "cancel_button": "❌ Hủy",
        "case_not_found": "⚠️ Không tìm thấy trường hợp",
        "not_authorized_delete": "🚫 Bạn không được phép xóa trường hợp này.",
        "case_deleted_successfully": "✅ Trường hợp đã được xóa thành công.",
        "confirm_delete": "❗ Bạn có chắc chắn muốn xóa trường hợp này?",
        "yes": "✅ Có",
        "no": "❌ Không",
        "delete_cancelled": "❌ Hủy việc xóa trường hợp.",
        "error_deleting_case": "⚠️ Lỗi khi xóa trường hợp. Vui lòng thử lại.",
        "extend_reward_button": "Kéo dài phần thưởng ➕",
        "extend_reward_not_found": "❌ Không tìm thấy yêu cầu kéo dài thưởng đang chờ xử lý.",
        "insufficient_funds": "❌ Tài khoản {wallet_type} không đủ. Cần ít nhất {required_amount}",
        "extend_reward_confirmation": (
            "🔄 *Xác nhận kéo dài phần thưởng*\n\n"
            "💰 Số tiền: {amount} {wallet_type}\n"
            "📤 Từ: `{from_wallet}`\n"
            "📥 Đến: `{to_wallet}`\n"
            "Bạn có chắc chắn muốn tiếp tục không?"
        ),
        "extend_success": "✅ Kéo dài phần thưởng {amount} {wallet_type} thành công!",
        "extend_cancelled": "❌ Kéo dài phần thưởng bị hủy.",
        "transfer_failed": "❌ Giao dịch thất bại. Vui lòng kiểm tra số dư và thử lại.",
        "case_or_extend_not_found": "❌ Không tìm thấy trường hợp hoặc yêu cầu kéo dài.",
        "no_wallet_found": "❌ Không tìm thấy ví nào phù hợp loại đã chọn.",
        "insufficient_funds_after_selection": "❌ Ví đã chọn không đủ tiền.",
        "extend_already_completed": "⚠️ Yêu cầu kéo dài thưởng đã hoàn tất trước đó.",
        "error_processing_extend": "❌ Có lỗi xảy ra khi xử lý yêu cầu kéo dài thưởng.",
        "error_approving_extend": "❌ Có lỗi xảy ra khi duyệt yêu cầu kéo dài thưởng.",
        "case_not_found": "❌ Không tìm thấy trường hợp.",
        "extend_reward_not_found": "❌ Không tìm thấy yêu cầu kéo dài thưởng chưa xử lý cho trường hợp này.",
        "select_wallet_for_extend": (
            "🔄 *Chọn ví để kéo dài phần thưởng*\n\n"
            "💰 Số tiền: {amount} {wallet_type}\n"
            "📤 Từ: `{from_wallet}`\n"
            "📥 Đến: `{to_wallet}`\n\n"
            "Vui lòng chọn một ví từ danh sách bên dưới:"
        ),
    },
    "km": {
        "no_advertise_cases": "គ្មានករណីផ្សព្វផ្សាយនៅទីនោះទេ។",
        "select_case_details": "📋 **ជ្រើសរើសករណីមួយដើម្បីមើលព័ត៌មានលម្អិត:**",
        "case_not_found": "❌ មិនរកឃើញករណីនោះទេ។",
        "error_fetching_cases": "កំហុសកើតឡើងខណៈពេលទាញយកករណី។",
        "error_fetching_case_details": "❌ កំហុសកើតឡើងខណៈពេលទាញយកព័ត៌មានលម្អិតអំពីករណី។",
        "error_paginating_cases": "❌ កំហុសកើតឡើងខណៈពេលធ្វើការបែងចែកទំព័រករណី។",
        "invalid_case_id": "❌ ID ករណីមិនត្រឹមត្រូវ។",
        "not_authorized_edit": "❌ អ្នកគ្មានសិទ្ធិកែសម្រួលករណីនេះទេ។",
        "not_authorized_delete": "❌ អ្នកគ្មានសិទ្ធិលុបករណីនេះទេ។",
        "case_deleted_successfully": "✅ ករណីត្រូវបានលុបដោយជោគជ័យ។",
        "edit_canceled": "📋 ការកែសម្រួលត្រូវបានបោះបង់។ ត្រលប់ទៅបញ្ជីករណីវិញ។",
        "enter_new_value": "✏️ សូមបញ្ចូលតម្លៃថ្មីសម្រាប់ **{field_name}**: ",
        "field_updated_successfully": "✅ **{field_name}** ត្រូវបានកែប្រែទៅជា: **{new_value}**",
        "invalid_value": "❌ {error_message} សូមបញ្ចូលតម្លៃដែលត្រឹមត្រូវ។",
        "edit_field_prompt": "📝 **តើ​អ្នក​ចង់កែប្រែ​វាល​ណា?**",
        "cancel_edit_button": "❌ បោះបង់",
        "edit_button": "📝 កែប្រែ",
        "delete_button": "🗑 លុប",
        "previous_button": "⬅️ មុន",
        "next_button": "➡️ បន្ទាប់",
        "editable_fields": {
            "ឈ្មោះ": "name",
            "ឈ្មោះបុគ្គល": "person_name",
            "ទំនាក់ទំនង": "relationship",
            "ទីតាំងដែលបានឃើញចុងក្រោយ": "last_seen_location",
            "ភេទ": "gender",
            "អាយុ": "age",
            "ពណ៌សក់": "hair_color",
            "ពណ៌ភ្នែក": "eye_color",
            "កំពស់": "height",
            "ទម្ងន់": "weight",
            "លក្ខណៈសម្គាល់": "distinctive_features",
            "ប្រទេស": "country",
            "ទីក្រុង": "city",
        },
        "insurfficient_balance": (
            "🚫 <b>ចំនួនទឹកប្រាក់មិនគ្រប់គ្រាន់</b>\n\n"
            "កាបូបរបស់អ្នកមានតែ <b>{wallet_balance} {wallet_type}</b> ប៉ុណ្ណោះ។\n"
            "ចំនួនទឹកប្រាក់រង្វាន់គឺ <b>{reward_amount} {wallet_type}</b>។\n"
            "សូមប្រាកដថាកាបូបរបស់អ្នកមានចំនួនគ្រប់គ្រាន់ដើម្បីបន្ត។"
        ),
        "congratulates_advertiser": (
            "🎉 <b>អបអរសាទរ!</b>\n\n"
            "រង្វាន់របស់អ្នកចំនួន <b>{reward_amount} {wallet_type}</b> ត្រូវបានផ្ទេរទៅវេទិកាយើងខ្ញុំដោយជោគជ័យ។\n\n"
            "📝 <b>សង្ខេបករណី:</b>\n"
            "👤 <b>ឈ្មោះករណី:</b> {case_name}\n"
            "📍 <b>ទីតាំង:</b> {location}\n"
            "🎁 <b>រង្វាន់:</b> {reward_amount} {wallet_type}\n"
            "💸 <b>ថ្លៃវេទិកា (5%):</b> {platform_fee} {wallet_type}\n"
            "🔒 <b>ចំនួនសុទ្ធដែលរក្សាទុក:</b> {net_amount} {wallet_type}\n\n"
            "🙌 យើងខ្ញុំបានរក្សាទុកករណីរបស់អ្នក និងរង្វាន់ត្រូវបានផ្ទេរទៅកាបូបរបស់អ្នកប្រើប្រាស់រួចរាល់ហើយ។\n"
            "🛡️ <b>រង្វាន់របស់អ្នកត្រូវបានរក្សាទុកដោយសុវត្ថិភាព</b> ហើយនឹងត្រូវបានបញ្ចេញតែតាមរយៈភស្តុតាងដែលបានផ្ទៀងផ្ទាត់ប៉ុណ្ណោះ។\n\n"
            "🚀 សូមអរគុណចំពោះការចូលរួមនៅក្នុងវេទិការបស់យើងខ្ញុំ!"
        ),
        "owner_message": (
            "📢 <b>ការផ្ទេររង្វាន់ថ្មីត្រូវបានបញ្ចប់</b>\n\n"
            "🆔 <b>ID អ្នកប្រើប្រាស់:</b> <code>{user_id}</code>\n"
            "📄 <b>ID ករណី:</b> <code>{case.id}</code>\n"
            "💰 <b>ចំនួនទឹកប្រាក់:</b> {reward_amount} {wallet_type}\n"
            "🔐 <b>កាបូប:</b> <code>{wallet.public_key}</code>\n"
            "🏷️ <b>ឈ្មោះកាបូប:</b> {wallet.name}\n\n"
            "✅ <b>ស្ថានភាព:</b> រង្វាន់ត្រូវបានផ្ទេរដោយជោគជ័យ។\n"
            "🔍 ប្រើ /listing ដើម្បីមើលករណីទាំងអស់។"
        ),
        "case_details_template": (
            "📌 *ព័ត៌មានលម្អិតអំពីករណី*\n"
            "👤 *ឈ្មោះ:* {person_name}\n"
            "📍 *ទីតាំងដែលបានឃើញចុងក្រោយ:* {last_seen_location}\n"
            "📆 *កាលបរិច្ឆេទ:* {last_seen_date}\n"
            "🎂 *អាយុ:* {age}\n"
            "💰 *រង្វាន់:* {reward} {reward_type}\n"
            "📏 *កំពស់:* {height} cm\n"
        ),
        "transfer_failed": "❌ <b>ការផ្ទេរបានបរាជ័យ</b>\n\nមានអ្វីមួយខុសបានកើតឡើងក្នុងការផ្ទេររង្វាន់។ សូមព្យាយាមម្តងទៀត។",
        "invalid_reward_amount": "❌ ចំនួនរង្វាន់មិនត្រឹមត្រូវ។ ចំនួនអតិបរមាគឺ {max_amount}។",
        "reward_success": "✅ រង្វាន់ត្រូវបានផ្ទេរទៅអ្នករកឃើញ {finder_id} ដោយជោគជ័យ។",
        "error_transferring_reward": "❌ កំហុសកើតឡើងក្នុងការផ្ទេររង្វាន់។",
        "case_or_finder_not_found": "❌ មិនរកឃើញករណី ឬអ្នករកឃើញទេ។",
        "no_finders_for_case": "❌ មិនរកឃើញអ្នករកឃើញសម្រាប់ករណីនេះទេ។",
        "finder_list_header": "👤 **អ្នករកឃើញសម្រាប់ករណីនេះ:**",
        "reward_this_finder": "💰 ផ្តល់រង្វាន់អ្នករកឃើញនេះ",
        "enter_reward_amount": "✏️ សូមបញ្ចូលចំនួនរង្វាន់សម្រាប់ករណីនេះ (អតិបរមា {max_amount}): ",
        "reward_confirmation": "តើ​អ្នក​ប្រាកដ​ជា​ចង់ផ្ញើរ {amount} ទៅអ្នករកឃើញ ID {finder_id} សម្រាប់ករណី {case_no}?",
        "reward_cancelled": "បានបោះបង់ការផ្តល់រង្វាន់",
        "confirm_button": "✅ បញ្ជាក់",
        "cancel_button": "❌ បោះបង់",
        "case_not_found": "⚠️ មិនរកឃើញករណីនោះទេ។",
        "not_authorized_delete": "🚫 អ្នកគ្មានសិទ្ធិលុបករណីនេះទេ។",
        "case_deleted_successfully": "✅ ករណីត្រូវបានលុបដោយជោគជ័យ។",
        "confirm_delete": "❗ តើ​អ្នក​ចង់លុបករណីនេះមែនទេ?",
        "yes": "✅ បាទ/ចាស",
        "no": "❌ ទេ",
        "delete_cancelled": "❌ ការលុបករណីត្រូវបានបោះបង់។",
        "error_deleting_case": "⚠️ កំហុសកើតឡើងក្នុងការលុបករណី។ សូមព្យាយាមម្តងទៀត។",
        "extend_reward_button": "បន្ថែមរង្វាន់ ➕",
        "extend_reward_not_found": "❌ មិនរកឃើញសំណើបន្ថែមរង្វាន់ដែលកំពុងរង់ចាំទេ។",
        "insufficient_funds": "❌ មិនមានឥណទានគ្រប់គ្រាន់នៅក្នុងកាបូប {wallet_type} របស់អ្នកទេ។ ចាំបាច់ត្រូវការ {required_amount}",
        "extend_reward_confirmation": (
            "🔄 *បញ្ជាក់ការបន្ថែមរង្វាន់*\n\n"
            "💰 ចំនួនទឹកប្រាក់: {amount} {wallet_type}\n"
            "📤 ពី: `{from_wallet}`\n"
            "📥 ទៅ: `{to_wallet}`\n"
            "តើ​អ្នក​ប្រាកដ​ថា​ចង់​បន្ត​មែនទេ?"
        ),
        "extend_success": "✅ បានបន្ថែមរង្វាន់ {amount} {wallet_type} ដោយជោគជ័យ!",
        "extend_cancelled": "❌ ការបន្ថែមរង្វាន់ត្រូវបានបោះបង់។",
        "transfer_failed": "❌ ការផ្ទេរបានបរាជ័យ។ សូមពិនិត្យមើលចំនួនទឹកប្រាក់ ហើយព្យាយាមម្តងទៀត។",
        "case_or_extend_not_found": "❌ មិនរកឃើញករណី ឬសំណើបន្ថែមទេ។",
        "no_wallet_found": "❌ មិនរកឃើញកាបូបសម្រាប់ប្រភេទដែលបានជ្រើសរើសទេ។",
        "insufficient_funds_after_selection": "❌ កាបូបដែលបានជ្រើសរើសគ្មានចំនួនគ្រប់គ្រាន់ទេ។",
        "extend_already_completed": "⚠️ សំណើបន្ថែមរង្វាន់នេះត្រូវបានបញ្ចប់រួចហើយ។",
        "error_processing_extend": "❌ កំហុសកើតឡើងក្នុងការដំណើរការសំណើបន្ថែមរង្វាន់។",
        "error_approving_extend": "❌ កំហុសកើតឡើងក្នុងការអនុម័តសំណើបន្ថែមរង្វាន់។",
        "case_not_found": "❌ មិនរកឃើញករណីទេ។",
        "extend_reward_not_found": "❌ មិនរកឃើញសំណើបន្ថែមរង្វាន់ដែលរង់ចាំនៅក្នុងករណីនេះទេ។",
        "select_wallet_for_extend": (
            "🔄 *ជ្រើសរើសកាបូបសម្រាប់ការបន្ថែមរង្វាន់*\n\n"
            "💰 ចំនួនទឹកប្រាក់: {amount} {wallet_type}\n"
            "📤 ពី: `{from_wallet}`\n"
            "📥 ទៅ: `{to_wallet}`\n\n"
            "សូមជ្រើសរើសកាបូបមួយពីជម្រើសខាងក្រោម:"
        ),
    },
    "ur": {
        "no_advertise_cases": "کوئی اشتہاری کیس نہیں ملا۔",
        "select_case_details": "📋 **تفصیلات دیکھنے کے لیے ایک کیس منتخب کریں:**",
        "case_not_found": "❌ کیس نہیں ملا۔",
        "error_fetching_cases": "کیسز کو حاصل کرتے وقت کچھ غلطی ہو گئی۔",
        "error_fetching_case_details": "❌ کیس کی تفصیل حاصل کرنے میں خرابی۔",
        "error_paginating_cases": "❌ کیسز پیج کرنے میں خرابی۔",
        "invalid_case_id": "❌ غیر درست کیس ID۔",
        "not_authorized_edit": "❌ آپ کو اس کیس کو ترمیم کرنے کی اجازت نہیں ہے۔",
        "not_authorized_delete": "❌ آپ کو اس کیس کو حذف کرنے کی اجازت نہیں ہے۔",
        "case_deleted_successfully": "✅ کیس کامیابی سے حذف کر دیا گیا۔",
        "edit_canceled": "📋 ترمیم منسوخ۔ کیسز کی فہرست میں واپس جا رہے ہیں۔",
        "enter_new_value": "✏️ براہ کرم **{field_name}** کے لیے نیا مقدار درج کریں: ",
        "field_updated_successfully": "✅ **{field_name}** کو اپ ڈیٹ کیا گیا: **{new_value}**",
        "invalid_value": "❌ {error_message} درست قدر درج کریں۔",
        "edit_field_prompt": "📝 **آپ کون سا فیلڈ تبدیل کرنا چاہتے ہیں؟**",
        "cancel_edit_button": "❌ منسوخ کریں",
        "edit_button": "📝 ترمیم کریں",
        "delete_button": "🗑 حذف کریں",
        "previous_button": "⬅️ پچھلا",
        "next_button": "➡️ اگلا",
        "editable_fields": {
            "نام": "name",
            "شخص کا نام": "person_name",
            "تعلقات": "relationship",
            "آخری بار دیکھا گیا مقام": "last_seen_location",
            "جنس": "gender",
            "عمر": "age",
            "بالوں کا رنگ": "hair_color",
            "آنکھوں کا رنگ": "eye_color",
            "قد": "height",
            "وزن": "weight",
            "تمایز کی خصوصیات": "distinctive_features",
            "ملک": "country",
            "شہر": "city",
        },
        "insurfficient_balance": (
            "🚫 <b>بقایا ناکافی</b>\n\n"
            "آپ کے والیٹ میں صرف <b>{wallet_balance} {wallet_type}</b> موجود ہے۔\n"
            "انعام کی رقم <b>{reward_amount} {wallet_type}</b> ہے۔\n"
            "براہ کرم یقین کریں کہ آپ کے والیٹ میں کافی رقم موجود ہے۔"
        ),
        "congratulates_advertiser": (
            "🎉 <b>مبارکباد!</b>\n\n"
            "آپ کا انعام <b>{reward_amount} {wallet_type}</b> ہماری ویب سائٹ پر منتقل کر دیا گیا ہے۔\n\n"
            "📝 <b>کیس کا خلاصہ:</b>\n"
            "👤 <b>کیس کا نام:</b> {case_name}\n"
            "📍 <b>مقام:</b> {location}\n"
            "🎁 <b>پیش کردہ انعام:</b> {reward_amount} {wallet_type}\n"
            "💸 <b>پلیٹ فارم فیس (5%):</b> {platform_fee} {wallet_type}\n"
            "🔒 <b>اسکرو میں رکھا گیا خالص مقدار:</b> {net_amount} {wallet_type}\n\n"
            "🙌 ہم نے آپ کا کیس درج کر لیا ہے اور انعام بوسٹ اوونر کے والیٹ میں منتقل کر دیا گیا ہے۔\n"
            "🛡️ <b>آپ کا انعام محفوظ اسکرو میں رکھا گیا ہے</b> اور صرف تصدیق شدہ کامیابی کے بعد جاری کیا جائے گا۔\n\n"
            "🚀 ہماری ویب سائٹ کا حصہ بننے پر شکریہ!"
        ),
        "owner_message": (
            "📢 <b>نیا انعام منتقل کر دیا گیا</b>\n\n"
            "🆔 <b>صارف آئی ڈی:</b> <code>{user_id}</code>\n"
            "📄 <b>کیس آئی ڈی:</b> <code>{case.id}</code>\n"
            "💰 <b>مقدار:</b> {reward_amount} {wallet_type}\n"
            "🔐 <b>والیٹ:</b> <code>{wallet.public_key}</code>\n"
            "🏷️ <b>والیٹ کا نام:</b> {wallet.name}\n\n"
            "✅ <b>حالت:</b> انعام کامیابی سے منتقل کیا گیا۔\n"
            "🔍 تمام فعال کیسز دیکھنے کے لیے /listing استعمال کریں۔"
        ),
        "case_details_template": (
            "📌 *کیس کی تفصیل*\n"
            "👤 *نام:* {person_name}\n"
            "📍 *آخری دفعہ دیکھا گیا مقام:* {last_seen_location}\n"
            "📆 *تاریخ:* {last_seen_date}\n"
            "🎂 *عمر:* {age}\n"
            "💰 *انعام:* {reward} {reward_type}\n"
            "📏 *قد:* {height} سینٹی میٹر\n"
        ),
        "transfer_failed": "❌ <b>منتقلی ناکام</b>\n\nانعام کی منتقلی کے دوران کچھ غلطی ہو گئی۔ براہ کرم بعد میں دوبارہ کوشش کریں۔",
        "invalid_reward_amount": "❌ غیر درست انعام کی رقم۔ زیادہ سے زیادہ رقم {max_amount} ہے۔",
        "reward_success": "✅ انعام کامیابی سے {finder_id} کو بھیج دیا گیا۔",
        "error_transferring_reward": "❌ انعام منتقل کرنے میں خرابی۔",
        "case_or_finder_not_found": "❌ کیس یا تلاش کنندہ نہیں ملا۔",
        "no_finders_for_case": "❌ اس کیس کے لیے کوئی تلاش کنندہ نہیں ملا۔",
        "finder_list_header": "👤 **اس کیس کے تلاش کنندہ:**",
        "reward_this_finder": "💰 اس تلاش کنندہ کو انعام دیں",
        "enter_reward_amount": "✏️ براہ کرم اس کیس کے لیے انعام کی رقم درج کریں (زیادہ سے زیادہ {max_amount}): ",
        "reward_confirmation": "کیا آپ کیس {case_no} کے لیے تلاش کنندہ {finder_id} کو {amount} انعام دینا چاہتے ہیں؟",
        "reward_cancelled": "انعام کی تقسیم منسوخ کر دی گئی",
        "confirm_button": "✅ تصدیق کریں",
        "cancel_button": "❌ منسوخ کریں",
        "case_not_found": "⚠️ کیس نہیں ملا۔",
        "not_authorized_delete": "🚫 آپ کو اس کیس کو حذف کرنے کی اجازت نہیں ہے۔",
        "case_deleted_successfully": "✅ کیس کامیابی سے حذف کر دیا گیا۔",
        "confirm_delete": "❗ کیا آپ واقعی اس کیس کو حذف کرنا چاہتے ہیں؟",
        "yes": "✅ ہاں",
        "no": "❌ نہیں",
        "delete_cancelled": "❌ کیس حذف کرنے کی کارروائی منسوخ کر دی گئی۔",
        "error_deleting_case": "⚠️ کیس حذف کرتے وقت خرابی۔ دوبارہ کوشش کریں۔",
        "extend_reward_button": "انعام میں توسیع ➕",
        "extend_reward_not_found": "❌ کوئی متحرک انعام توسیع کی درخواست نہیں ملی۔",
        "insufficient_funds": "❌ آپ کے {wallet_type} والیٹ میں فنڈز ناکافی ہیں۔ درکار رقم: {required_amount}",
        "extend_reward_confirmation": (
            "🔄 <b>انعام کی توسیع کی تصدیق</b>\n\n"
            "💰 رقم: {amount} {wallet_type}\n"
            "📤 سے: `{from_wallet}`\n"
            "📥 تک: `{to_wallet}`\n"
            "کیا آپ واقعی جاری رکھنا چاہتے ہیں؟"
        ),
        "extend_success": "✅ {amount} {wallet_type} انعام کی توسیع کامیاب رہی!",
        "extend_cancelled": "❌ انعام کی توسیع منسوخ کر دی گئی۔",
        "transfer_failed": "❌ منتقلی ناکام۔ براہ کرم والیٹ کی موجودہ رقم چیک کر کے دوبارہ کوشش کریں۔",
        "case_or_extend_not_found": "❌ کیس یا توسیع کی درخواست نہیں ملی۔",
        "no_wallet_found": "❌ منتخب کردہ قسم کے لیے والیٹ نہیں ملا۔",
        "insufficient_funds_after_selection": "❌ منتخب کردہ والیٹ میں فنڈز ناکافی ہیں۔",
        "extend_already_completed": "⚠️ یہ انعام توسیع کی درخواست پہلے ہی مکمل ہو چکی ہے۔",
        "error_processing_extend": "❌ انعام کی توسیع کی درخواست کی پروسیسنگ کے دوران خرابی۔",
        "error_approving_extend": "❌ انعام کی توسیع کی درخواست کی منظوری کے دوران خرابی۔",
        "case_not_found": "❌ کیس نہیں ملا۔",
        "extend_reward_not_found": "❌ اس کیس کے لیے کوئی توسیع کی درخواست نہیں ملی۔",
        "select_wallet_for_extend": (
            "🔄 <b>انعام کی توسیع کے لیے والیٹ منتخب کریں</b>\n\n"
            "💰 رقم: {amount} {wallet_type}\n"
            "📤 سے: `{from_wallet}`\n"
            "📥 تک: `{to_wallet}`\n\n"
            "براہ کرم ذیلی آپشنز میں سے ایک والیٹ منتخب کریں:"
        ),
    },
    "ja": {
        "no_advertise_cases": "広告案件は見つかりませんでした。",
        "select_case_details": "📋 **詳細を表示する案件を選択してください：**",
        "case_not_found": "❌ 案件が見つかりません。",
        "error_fetching_cases": "案件の取得中にエラーが発生しました。",
        "error_fetching_case_details": "❌ 案件詳細の取得中にエラーが発生しました。",
        "error_paginating_cases": "❌ 案件のページネーション中にエラーが発生しました。",
        "invalid_case_id": "❌ 無効な案件IDです。",
        "not_authorized_edit": "❌ この案件を編集する権限がありません。",
        "not_authorized_delete": "❌ この案件を削除する権限がありません。",
        "case_deleted_successfully": "✅ 案件は正常に削除されました。",
        "edit_canceled": "📋 編集をキャンセルしました。案件一覧に戻ります。",
        "enter_new_value": "✏️ **{field_name}** の新しい値を入力してください：",
        "field_updated_successfully": "✅ **{field_name}** を以下に更新しました： **{new_value}**",
        "invalid_value": "❌ {error_message} 正しい値を入力してください。",
        "edit_field_prompt": "📝 **どのフィールドを編集しますか？**",
        "cancel_edit_button": "❌ キャンセル",
        "edit_button": "📝 編集",
        "delete_button": "🗑 削除",
        "previous_button": "⬅️ 前へ",
        "next_button": "➡️ 次へ",
        "editable_fields": {
            "名前": "name",
            "人物名": "person_name",
            "関係性": "relationship",
            "最後に確認した場所": "last_seen_location",
            "性別": "gender",
            "年齢": "age",
            "髪の色": "hair_color",
            "目の色": "eye_color",
            "身長": "height",
            "体重": "weight",
            "特徴": "distinctive_features",
            "国": "country",
            "都市": "city",
        },
        "insurfficient_balance": (
            "🚫 <b>残高不足</b>\n\n"
            "あなたのウォレットには <b>{wallet_balance} {wallet_type}</b> のみあります。\n"
            "必要金額は <b>{reward_amount} {wallet_type}</b> です。\n"
            "処理を続行するために、ウォレットに十分な残高があることを確認してください。"
        ),
        "congratulates_advertiser": (
            "🎉 <b>おめでとうございます！</b>\n\n"
            "あなたの提供した報酬 <b>{reward_amount} {wallet_type}</b> はプラットフォームに正しく送金されました。\n\n"
            "📝 <b>案件概要：</b>\n"
            "👤 <b>案件名：</b> {case_name}\n"
            "📍 <b>場所：</b> {location}\n"
            "🎁 <b>報酬：</b> {reward_amount} {wallet_type}\n"
            "💸 <b>プラットフォーム手数料 (5%)：</b> {platform_fee} {wallet_type}\n"
            "🔒 <b>エスクロー中の純額：</b> {net_amount} {wallet_type}\n\n"
            "🙌 案件を登録し、報酬をボット所有者のウォレットに移動させました。\n"
            "🛡️ <b>報酬は安全にエスクローされています。</b> 適格な証拠提出後のみリリースされます。\n\n"
            "🚀 当プラットフォームの一員になっていただきありがとうございます！"
        ),
        "owner_message": (
            "📢 <b>新規報酬送金が完了しました</b>\n\n"
            "🆔 <b>ユーザーID：</b> <code>{user_id}</code>\n"
            "📄 <b>案件ID：</b> <code>{case.id}</code>\n"
            "💰 <b>金額：</b> {reward_amount} {wallet_type}\n"
            "🔐 <b>ウォレット：</b> <code>{wallet.public_key}</code>\n"
            "🏷️ <b>ウォレット名：</b> {wallet.name}\n\n"
            "✅ <b>ステータス：</b> 報酬が正しく送金されました。\n"
            "🔍 /listing を使用してすべてのアクティブ案件を確認できます。"
        ),
        "case_details_template": (
            "📌 *案件詳細*\n"
            "👤 *氏名:* {person_name}\n"
            "📍 *最後に確認された場所:* {last_seen_location}\n"
            "📆 *日付:* {last_seen_date}\n"
            "🎂 *年齢:* {age}\n"
            "💰 *報酬:* {reward} {reward_type}\n"
            "📏 *身長:* {height} cm\n"
        ),
        "transfer_failed": "❌ <b>送金失敗</b>\n\n報酬の送金中に問題が発生しました。後でもう一度やり直してください。",
        "invalid_reward_amount": "❌ 無効な報酬金額です。最大額は {max_amount} です。",
        "reward_success": "✅ ファインダー {finder_id} に報酬を送金しました。",
        "error_transferring_reward": "❌ 報酬の転送中にエラーが発生しました。",
        "case_or_finder_not_found": "❌ 案件またはファインダーが見つかりません。",
        "no_finders_for_case": "❌ この案件に該当するファインダーはいません。",
        "finder_list_header": "👤 **この案件に関わるファインダー：**",
        "reward_this_finder": "💰 このファインダーに報酬を支払う",
        "enter_reward_amount": "✏️ この案件の報酬金額を入力してください（最大 {max_amount}）：",
        "reward_confirmation": "{case_no} のファインダー {finder_id} に {amount} を報酬として送信してもよろしいですか？",
        "reward_cancelled": "報酬プロセスがキャンセルされました。",
        "confirm_button": "✅ 確認",
        "cancel_button": "❌ キャンセル",
        "case_not_found": "⚠️ 案件が見つかりません。",
        "not_authorized_delete": "🚫 この案件を削除する権限がありません。",
        "case_deleted_successfully": "✅ 案件は正しく削除されました。",
        "confirm_delete": "❗ この案件を削除してもよろしいですか？",
        "yes": "✅ はい",
        "no": "❌ いいえ",
        "delete_cancelled": "❌ 案件の削除がキャンセルされました。",
        "error_deleting_case": "⚠️ 案件削除中にエラーが発生しました。再試行してください。",
        "extend_reward_button": "報酬延長 ➕",
        "extend_reward_not_found": "❌ アクティブな報酬延長リクエストが見つかりません。",
        "insufficient_funds": "❌ 選択した {wallet_type} ウォレットに資金がありません。必要な金額：{required_amount}",
        "extend_reward_confirmation": (
            "🔄 *報酬延長の確認*\n\n"
            "💰 金額: {amount} {wallet_type}\n"
            "📤 から: `{from_wallet}`\n"
            "📥 へ: `{to_wallet}`\n"
            "本当に実行しますか？"
        ),
        "extend_success": "✅ 報酬を {amount} {wallet_type} 分だけ延長しました！",
        "extend_cancelled": "❌ 報酬延長がキャンセルされました。",
        "transfer_failed": "❌ 転送に失敗しました。ウォレット残高を確認してやり直してください。",
        "case_or_extend_not_found": "❌ 案件または延長要求が見つかりません。",
        "no_wallet_found": "❌ 選択されたタイプのウォレットが見つかりません。",
        "insufficient_funds_after_selection": "❌ 選択されたウォレットの資金が不足しています。",
        "extend_already_completed": "⚠️ この報酬延長リクエストは既に完了しています。",
        "error_processing_extend": "❌ 報酬延長リクエストの処理中にエラーが発生しました。",
        "error_approving_extend": "❌ 報酬延長リクエストの承認中にエラーが発生しました。",
        "case_not_found": "❌ 案件が見つかりません。",
        "extend_reward_not_found": "❌ この案件には保留中の報酬延長リクエストがありません。",
        "select_wallet_for_extend": (
            "🔄 *報酬延長用ウォレットを選択してください*\n\n"
            "💰 金額: {amount} {wallet_type}\n"
            "📤 から: `{from_wallet}`\n"
            "📥 へ: `{to_wallet}`\n\n"
            "以下のオプションからウォレットを選択してください："
        ),
    },
    "ko": {
        "no_advertise_cases": "광고 케이스가 없습니다.",
        "select_case_details": "📋 **상세 정보를 확인할 케이스를 선택하세요:**",
        "case_not_found": "❌ 케이스를 찾을 수 없습니다.",
        "error_fetching_cases": "케이스를 가져오는 중 오류가 발생했습니다.",
        "error_fetching_case_details": "❌ 케이스 상세 정보를 가져오는 중 오류가 발생했습니다.",
        "error_paginating_cases": "❌ 케이스 페이지네이션 중 오류가 발생했습니다.",
        "invalid_case_id": "❌ 잘못된 케이스 ID입니다.",
        "not_authorized_edit": "❌ 이 케이스를 편집할 권한이 없습니다.",
        "not_authorized_delete": "❌ 이 케이스를 삭제할 권한이 없습니다.",
        "case_deleted_successfully": "✅ 케이스가 성공적으로 삭제되었습니다.",
        "edit_canceled": "📋 편집이 취소되었습니다. 케이스 목록으로 돌아갑니다.",
        "enter_new_value": "✏️ **{field_name}** 에 대한 새로운 값을 입력하세요: ",
        "field_updated_successfully": "✅ **{field_name}** 이(가) 다음 값으로 업데이트되었습니다: **{new_value}**",
        "invalid_value": "❌ {error_message} 유효한 값을 입력해 주세요.",
        "edit_field_prompt": "📝 **어떤 필드를 편집하시겠습니까?**",
        "cancel_edit_button": "❌ 취소",
        "edit_button": "📝 편집",
        "delete_button": "🗑 삭제",
        "previous_button": "⬅️ 이전",
        "next_button": "➡️ 다음",
        "editable_fields": {
            "이름": "name",
            "사람 이름": "person_name",
            "관계": "relationship",
            "마지막 발견 장소": "last_seen_location",
            "성별": "gender",
            "나이": "age",
            "머리카락 색": "hair_color",
            "눈 색": "eye_color",
            "키": "height",
            "몸무게": "weight",
            "특징": "distinctive_features",
            "국가": "country",
            "도시": "city",
        },
        "insurfficient_balance": (
            "🚫 <b>잔액 부족</b>\n\n"
            "당신의 지갑에는 <b>{wallet_balance} {wallet_type}</b> 만큼만 있습니다.\n"
            "요청한 보상 금액은 <b>{reward_amount} {wallet_type}</b> 입니다.\n"
            "계속 진행하려면 충분한 잔액이 있는지 확인하세요."
        ),
        "congratulates_advertiser": (
            "🎉 <b>축하합니다!</b>\n\n"
            "보상금 <b>{reward_amount} {wallet_type}</b> 가 플랫폼에 성공적으로 전송되었습니다.\n\n"
            "📝 <b>케이스 요약:</b>\n"
            "👤 <b>케이스 이름:</b> {case_name}\n"
            "📍 <b>장소:</b> {location}\n"
            "🎁 <b>제안된 보상:</b> {reward_amount} {wallet_type}\n"
            "💸 <b>플랫폼 수수료 (5%):</b> {platform_fee} {wallet_type}\n"
            "🔒 <b>에스크로에 보관된 순금액:</b> {net_amount} {wallet_type}\n\n"
            "🙌 케이스를 등록했으며, 보상금은 봇 소유자의 지갑으로 이동되었습니다.\n"
            "🛡️ <b>보상금은 안전하게 에스크로 상태로 보관되며</b>, 검증된 성공적인 제보 시에만 해제됩니다.\n\n"
            "🚀 플랫폼에 참여해주셔서 감사합니다!"
        ),
        "owner_message": (
            "📢 <b>새 보상금 전송 완료됨</b>\n\n"
            "🆔 <b>사용자 ID:</b> <code>{user_id}</code>\n"
            "📄 <b>케이스 ID:</b> <code>{case.id}</code>\n"
            "💰 <b>금액:</b> {reward_amount} {wallet_type}\n"
            "🔐 <b>지갑:</b> <code>{wallet.public_key}</code>\n"
            "🏷️ <b>지갑 이름:</b> {wallet.name}\n\n"
            "✅ <b>상태:</b> 보상금이 성공적으로 전송되었습니다.\n"
            "🔍 /listing 명령어로 모든 활성 케이스를 확인하세요."
        ),
        "case_details_template": (
            "📌 *케이스 세부 정보*\n"
            "👤 *이름:* {person_name}\n"
            "📍 *마지막으로 본 위치:* {last_seen_location}\n"
            "📆 *날짜:* {last_seen_date}\n"
            "🎂 *나이:* {age}\n"
            "💰 *보상:* {reward} {reward_type}\n"
            "📏 *키:* {height} cm\n"
        ),
        "transfer_failed": "❌ <b>전송 실패</b>\n\n보상금 전송 처리 중 문제가 발생했습니다. 나중에 다시 시도해 주세요.",
        "invalid_reward_amount": "❌ 잘못된 보상금액입니다. 최대 보상금액은 {max_amount} 입니다.",
        "reward_success": "✅ 탐문자 {finder_id}에게 보상금이 성공적으로 전달되었습니다.",
        "error_transferring_reward": "❌ 보상금 전송 중 오류 발생.",
        "case_or_finder_not_found": "❌ 케이스 또는 탐문자를 찾을 수 없습니다.",
        "no_finders_for_case": "❌ 이 케이스에 해당하는 탐문자가 없습니다.",
        "finder_list_header": "👤 **이 케이스의 탐문자 목록:**",
        "reward_this_finder": "💰 이 탐문자에게 보상금 지급",
        "enter_reward_amount": "✏️ 이 케이스의 보상금을 입력하세요 (최대 {max_amount}): ",
        "reward_confirmation": "{case_no} 케이스의 탐문자 {finder_id}에게 {amount} 보상금을 지급하시겠습니까?",
        "reward_cancelled": "보상금 프로세스가 취소되었습니다.",
        "confirm_button": "✅ 확인",
        "cancel_button": "❌ 취소",
        "case_not_found": "⚠️ 케이스를 찾을 수 없습니다.",
        "not_authorized_delete": "🚫 이 케이스를 삭제할 권한이 없습니다.",
        "case_deleted_successfully": "✅ 케이스가 성공적으로 삭제되었습니다.",
        "confirm_delete": "❗ 정말로 이 케이스를 삭제하시겠습니까?",
        "yes": "✅ 예",
        "no": "❌ 아니오",
        "delete_cancelled": "❌ 케이스 삭제가 취소되었습니다.",
        "error_deleting_case": "⚠️ 케이스 삭제 중 오류가 발생했습니다. 다시 시도해 주세요.",
        "extend_reward_button": "보상 연장 ➕",
        "extend_reward_not_found": "❌ 대기 중인 보상 연장 요청이 없습니다.",
        "insufficient_funds": "❌ {wallet_type} 지갑에 자금이 부족합니다. 필요 금액: {required_amount}",
        "extend_reward_confirmation": (
            "🔄 <b>보상 연장을 확인하세요</b>\n\n"
            "💰 금액: {amount} {wallet_type}\n"
            "📤 보낸 지갑: `{from_wallet}`\n"
            "📥 받는 지갑: `{to_wallet}`\n"
            "정말로 진행하시겠습니까?"
        ),
        "extend_success": "✅ {amount} {wallet_type} 보상을 성공적으로 연장했습니다!",
        "extend_cancelled": "❌ 보상 연장이 취소되었습니다.",
        "transfer_failed": "❌ 전송 실패. 지갑 잔액을 확인하고 다시 시도하세요.",
        "case_or_extend_not_found": "❌ 케이스 또는 연장 요청을 찾을 수 없습니다.",
        "no_wallet_found": "❌ 선택한 유형의 지갑을 찾을 수 없습니다.",
        "insufficient_funds_after_selection": "❌ 선택한 지갑에 자금이 부족합니다.",
        "extend_already_completed": "⚠️ 이 보상 연장 요청은 이미 완료되었습니다.",
        "error_processing_extend": "❌ 보상 연장 요청 처리 중 오류 발생.",
        "error_approving_extend": "❌ 보상 연장 요청 승인 중 오류 발생.",
        "case_not_found": "❌ 케이스를 찾을 수 없습니다.",
        "extend_reward_not_found": "❌ 이 케이스에 대기 중인 보상 연장 요청이 없습니다.",
        "select_wallet_for_extend": (
            "🔄 <b>보상 연장을 위한 지갑을 선택하세요</b>\n\n"
            "💰 금액: {amount} {wallet_type}\n"
            "📤 보낸 지갑: `{from_wallet}`\n"
            "📥 받는 지갑: `{to_wallet}`\n\n"
            "다음 옵션에서 지갑을 선택하세요:"
        ),
    },
    "id": {
        "no_advertise_cases": "Tidak ada kasus iklan ditemukan.",
        "select_case_details": "📋 **Pilih Kasus untuk Melihat Detail:**",
        "case_not_found": "❌ Kasus tidak ditemukan.",
        "error_fetching_cases": "Terjadi kesalahan saat mengambil daftar kasus.",
        "error_fetching_case_details": "❌ Terjadi kesalahan saat mengambil detail kasus.",
        "error_paginating_cases": "❌ Terjadi kesalahan saat memuat halaman kasus.",
        "invalid_case_id": "❌ ID kasus tidak valid.",
        "not_authorized_edit": "❌ Anda tidak diizinkan untuk mengedit kasus ini.",
        "not_authorized_delete": "❌ Anda tidak diizinkan untuk menghapus kasus ini.",
        "case_deleted_successfully": "✅ Kasus berhasil dihapus.",
        "edit_canceled": "📋 Pengeditan dibatalkan. Kembali ke daftar kasus.",
        "enter_new_value": "✏️ Masukkan nilai baru untuk **{field_name}**: ",
        "field_updated_successfully": "✅ **{field_name}** berhasil diubah menjadi: **{new_value}**",
        "invalid_value": "❌ {error_message} Sila masukkan nilai yang sah.",
        "edit_field_prompt": "📝 **Bidang mana yang ingin Anda edit?**",
        "cancel_edit_button": "❌ Batal",
        "edit_button": "📝 Edit",
        "delete_button": "🗑 Hapus",
        "previous_button": "⬅️ Sebelumnya",
        "next_button": "➡️ Selanjutnya",
        "editable_fields": {
            "Nama": "name",
            "Nama Orang": "person_name",
            "Hubungan": "relationship",
            "Lokasi Terakhir Diketahui": "last_seen_location",
            "Jenis Kelamin": "gender",
            "Usia": "age",
            "Warna Rambut": "hair_color",
            "Warna Mata": "eye_color",
            "Tinggi": "height",
            "Berat": "weight",
            "Fitur Khusus": "distinctive_features",
            "Negara": "country",
            "Kota": "city",
        },
        "insurfficient_balance": (
            "🚫 <b>Saldo Tidak Cukup</b>\n\n"
            "Dompet Anda hanya memiliki <b>{wallet_balance} {wallet_type}</b>.\n"
            "Jumlah hadiah adalah <b>{reward_amount} {wallet_type}</b>.\n"
            "Harap pastikan dompet Anda memiliki cukup saldo untuk melanjutkan."
        ),
        "congratulates_advertiser": (
            "🎉 <b>Selamat!</b>\n\n"
            "Hadiah sebesar <b>{reward_amount} {wallet_type}</b> telah berhasil ditransfer ke platform kami.\n\n"
            "📝 <b>Ringkasan Kasus:</b>\n"
            "👤 <b>Nama Kasus:</b> {case_name}\n"
            "📍 <b>Lokasi:</b> {location}\n"
            "🎁 <b>Hadiah Ditawarkan:</b> {reward_amount} {wallet_type}\n"
            "💸 <b>Biaya Platform (5%):</b> {platform_fee} {wallet_type}\n"
            "🔒 <b>Total Disimpan dalam Escrow:</b> {net_amount} {wallet_type}\n\n"
            "🙌 Kami telah mendaftarkan kasus Anda dan hadiah telah dipindahkan ke dompet pemilik bot.\n"
            "🛡️ <b>Hadiah Anda aman dan tersimpan dalam escrow</b> dan hanya akan dirilis setelah bukti keberhasilan diverifikasi.\n\n"
            "🚀 Terima kasih atas partisipasi Anda di platform kami!"
        ),
        "owner_message": (
            "📢 <b>Pemindahan Hadiah Baru Berhasil</b>\n\n"
            "🆔 <b>ID Pengguna:</b> <code>{user_id}</code>\n"
            "📄 <b>ID Kasus:</b> <code>{case.id}</code>\n"
            "💰 <b>Jumlah:</b> {reward_amount} {wallet_type}\n"
            "🔐 <b>Dompet:</b> <code>{wallet.public_key}</code>\n"
            "🏷️ <b>Nama Dompet:</b> {wallet.name}\n\n"
            "✅ <b>Status:</b> Hadiah berhasil dipindahkan.\n"
            "🔍 Gunakan /listing untuk melihat semua kasus aktif."
        ),
        "case_details_template": (
            "📌 *Detail Kasus*\n"
            "👤 *Nama:* {person_name}\n"
            "📍 *Lokasi Terakhir Terlihat:* {last_seen_location}\n"
            "📆 *Tanggal:* {last_seen_date}\n"
            "🎂 *Usia:* {age}\n"
            "💰 *Hadiah:* {reward} {reward_type}\n"
            "📏 *Tinggi:* {height} cm\n"
        ),
        "transfer_failed": "❌ <b>Pemindahan Gagal</b>\n\nAda yang salah saat memproses pemindahan hadiah. Sila coba lagi nanti.",
        "invalid_reward_amount": "❌ Jumlah hadiah tidak valid. Jumlah maksimal adalah {max_amount}.",
        "reward_success": "✅ Hadiah berhasil dikirim ke pencari {finder_id}.",
        "error_transferring_reward": "❌ Terjadi kesalahan saat mentransfer hadiah.",
        "case_or_finder_not_found": "❌ Kasus atau pencari tidak ditemukan.",
        "no_finders_for_case": "❌ Tidak ada pencari ditemukan untuk kasus ini.",
        "finder_list_header": "👤 **Pencari untuk kasus ini:**",
        "reward_this_finder": "💰 Beri hadiah pada pencari ini",
        "enter_reward_amount": "✏️ Sila masukkan jumlah hadiah untuk kasus ini (maks {max_amount}): ",
        "reward_confirmation": "Apakah Anda yakin ingin mengirim hadiah sebesar {amount} kepada Pencari ID {finder_id} untuk Kasus {case_no}?",
        "reward_cancelled": "Proses hadiah dibatalkan",
        "confirm_button": "✅ Konfirmasi",
        "cancel_button": "❌ Batalkan",
        "case_not_found": "⚠️ Kasus tidak ditemukan.",
        "not_authorized_delete": "🚫 Anda tidak diizinkan untuk menghapus kasus ini.",
        "case_deleted_successfully": "✅ Kasus berhasil dihapus.",
        "confirm_delete": "❗ Apakah Anda yakin ingin menghapus kasus ini?",
        "yes": "✅ Ya",
        "no": "❌ Tidak",
        "delete_cancelled": "❌ Penghapusan kasus dibatalkan.",
        "error_deleting_case": "⚠️ Terjadi kesalahan saat menghapus kasus. Sila coba lagi.",
        "extend_reward_button": "Perpanjang Ganjaran ➕",
        "extend_reward_not_found": "❌ Tidak ada permintaan perpanjangan ganjaran aktif ditemukan.",
        "insufficient_funds": "❌ Dana tidak mencukupi di dompet {wallet_type} Anda. Dibutuhkan: {required_amount}",
        "extend_reward_confirmation": (
            "🔄 *Konfirmasi Perpanjangan Ganjaran*\n\n"
            "💰 Jumlah: {amount} {wallet_type}\n"
            "📤 Dari: `{from_wallet}`\n"
            "📥 Ke: `{to_wallet}`\n"
            "Apakah Anda yakin ingin melanjutkan?"
        ),
        "extend_success": "✅ Berhasil memperpanjang ganjaran sebesar {amount} {wallet_type}!",
        "extend_cancelled": "❌ Perpanjangan ganjaran dibatalkan.",
        "transfer_failed": "❌ Transfer gagal. Sila periksa saldonya dan coba lagi.",
        "case_or_extend_not_found": "❌ Kasus atau permintaan perpanjangan tidak ditemukan.",
        "no_wallet_found": "❌ Tidak ada dompet ditemukan untuk jenis terpilih.",
        "insufficient_funds_after_selection": "❌ Dana tidak mencukupi di dompet yang dipilih.",
        "extend_already_completed": "⚠️ Permintaan perpanjangan ini sudah selesai.",
        "error_processing_extend": "❌ Terjadi kesalahan saat memproses permintaan perpanjangan.",
        "error_approving_extend": "❌ Terjadi kesalahan saat menyetujui permintaan perpanjangan.",
        "case_not_found": "❌ Kasus tidak ditemukan.",
        "extend_reward_not_found": "❌ Tidak ada permintaan perpanjangan ganjaran tertunda ditemukan untuk kasus ini.",
        "select_wallet_for_extend": (
            "🔄 *Pilih Dompet untuk Perpanjangan Ganjaran*\n\n"
            "💰 Jumlah: {amount} {wallet_type}\n"
            "📤 Dari: `{from_wallet}`\n"
            "📥 Ke: `{to_wallet}`\n\n"
            "Silakan pilih dompet dari opsi di bawah:"
        ),
    },
}
