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
        "cancel_edit_button": "Cancel",
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
        "case_details_template": (
            "📌 **Case Details**\n"
            "👤 **Person Name:** {person_name}\n"
            "📍 **Last Seen Location:** {last_seen_location}\n"
            "💰 **Reward:** {reward} {reward_type}\n"
            "💼 **Wallet:** {wallet}\n"
            "👤 **Gender:** {gender}\n"
            "🧒 **Age:** {age}\n"
            "📏 **Height:** {height} cm\n"
        ),
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
        # ----- Delete Start ------
        "case_not_found": "⚠️ Case not found.",
        "not_authorized_delete": "🚫 You are not authorized to delete this case.",
        "case_deleted_successfully": "✅ Case has been successfully deleted.",
        "confirm_delete": "❗ Are you sure you want to delete this case?",
        "yes": "✅ Yes",
        "no": "❌ No",
        "delete_cancelled": "❌ Case deletion has been cancelled.",
        "error_deleting_case": "⚠️ An error occurred while deleting the case. Please try again.",
        # ----- Delete End ------
        # ----------- Extend Reward Constants ----------
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
        "no_advertise_cases": "未找到广告案例。",
        "select_case_details": "📋 **选择一个案例查看详情：**",
        "case_not_found": "❌ 案例未找到。",
        "error_fetching_cases": "获取案例时发生错误。",
        "error_fetching_case_details": "❌ 获取案例详情时发生错误。",
        "error_paginating_cases": "❌ 分页案例时发生错误。",
        "invalid_case_id": "❌ 无效的案例ID。",
        "not_authorized_edit": "❌ 您无权编辑此案例。",
        "not_authorized_delete": "❌ 您无权删除此案例。",
        "case_deleted_successfully": "✅ 案例已成功删除。",
        "edit_canceled": "📋 编辑已取消。返回案例列表。",
        "enter_new_value": "✏️ 请输入 **{field_name}** 的新值： ",
        "field_updated_successfully": "✅ **{field_name}** 已更新为：**{new_value}**",
        "invalid_value": "❌ {error_message} 请输入有效值。",
        "edit_field_prompt": "📝 **您想编辑哪个字段？**",
        "cancel_edit_button": "取消",
        "edit_button": "📝 编辑",
        "delete_button": "🗑 删除",
        "previous_button": "⬅️ 上一页",
        "next_button": "➡️ 下一页",
        "editable_fields": {
            "姓名": "name",
            "个人姓名": "person_name",
            "关系": "relationship",
            "最后出现地点": "last_seen_location",
            "性别": "gender",
            "年龄": "age",
            "头发颜色": "hair_color",
            "眼睛颜色": "eye_color",
            "身高": "height",
            "体重": "weight",
            "显著特征": "distinctive_features",
            "国家": "country",
            "城市": "city",
        },
        "case_details_template": (
            "📌 **案例详情**\n"
            "👤 **姓名:** {person_name}\n"
            "📍 **最后出现地点:** {last_seen_location}\n"
            "💰 **奖励:** {reward} {reward_type}\n"
            "💼 **钱包:** {wallet}\n"
            "👤 **性别:** {gender}\n"
            "🧒 **年龄:** {age}\n"
            "📏 **身高:** {height} 厘米\n"
        ),
        "invalid_reward_amount": "❌ 无效的奖励金额。最大奖励金额为 {max_amount}。",
        "reward_success": "✅ 已成功向查找者 {finder_id} 发送 {amount} 奖励。",
        "error_transferring_reward": "❌ 发送奖励时出错。",
        "case_or_finder_not_found": "❌ 未找到案例或查找者。",
        "no_finders_for_case": "❌ 未找到此案例的查找者。",
        "finder_list_header": "👤 **此案例的查找者：**",
        "reward_this_finder": "💰 奖励此查找者",
        "enter_reward_amount": "✏️ 请输入此案例的奖励金额（最大 {max_amount}）：",
        "reward_confirmation": "您确定要向查找者 ID {finder_id} 发送 {amount} 奖励吗？",
        "reward_cancelled": "奖励过程已取消。",
        "confirm_button": "✅ 确认",
        "cancel_button": "❌ 取消",
        # ----- Delete Start ------
        "case_not_found": "⚠️ 案例未找到。",
        "not_authorized_delete": "🚫 您无权删除此案例。",
        "case_deleted_successfully": "✅ 案例已成功删除。",
        "confirm_delete": "❗ 您确定要删除此案例吗？",
        "yes": "✅ 是",
        "no": "❌ 否",
        "delete_cancelled": "❌ 案例删除已取消。",
        "error_deleting_case": "⚠️ 删除案例时发生错误。请重试。",
        # ----- Delete End ------
        # ----------- 扩展奖励相关常量 ----------
        "extend_reward_button": "扩展奖励 ➕",
        "extend_reward_not_found": "❌ 未找到有效的奖励扩展请求。",
        "insufficient_funds": "❌ {wallet_type}钱包余额不足，需要：{required_amount}",
        "extend_reward_confirmation": (
            "🔄 *确认扩展奖励*\n\n"
            "💰 金额：{amount} {wallet_type}\n"
            "📤 来源钱包：`{from_wallet}`\n"
            "📥 目标钱包：`{to_wallet}`\n"
            "确定要继续吗？"
        ),
        "extend_success": "✅ 成功扩展了{amount} {wallet_type}奖励！",
        "extend_cancelled": "❌ 奖励扩展已取消。",
        "transfer_failed": "❌ 转账失败，请检查钱包余额后重试。",
        "case_or_extend_not_found": "❌ 未找到案例或扩展请求。",
         "insufficient_funds_after_selection": "❌ 所选钱包余额不足。",
    "extend_already_completed": "⚠️ 此扩展奖励请求已完成。",
    "error_processing_extend": "❌ 处理扩展奖励请求时发生错误。",
    "error_approving_extend": "❌ 批准扩展奖励请求时发生错误。",
    "case_not_found": "❌ 找不到案件。",
    "extend_reward_not_found": "❌ 找不到此案件的待处理扩展奖励请求。",
    },
    "ms": {
        "no_advertise_cases": "Tiada kes IKLAN ditemui.",
        "select_case_details": "📋 **Pilih Kes untuk Lihat Butiran:**",
        "case_not_found": "❌ Kes tidak ditemui.",
        "error_fetching_cases": "Ralat berlaku semasa mengambil kes.",
        "error_fetching_case_details": "❌ Ralat berlaku semasa mengambil butiran kes.",
        "error_paginating_cases": "❌ Ralat berlaku semasa memfailkan kes.",
        "invalid_case_id": "❌ ID kes tidak sah.",
        "not_authorized_edit": "❌ Anda tidak dibenarkan untuk mengedit kes ini.",
        "not_authorized_delete": "❌ Anda tidak dibenarkan untuk memadam kes ini.",
        "case_deleted_successfully": "✅ Kes telah berjaya dipadam.",
        "edit_canceled": "📋 Pengeditan dibatalkan. Kembali ke senarai kes.",
        "enter_new_value": "✏️ Sila masukkan nilai baru untuk **{field_name}**: ",
        "field_updated_successfully": "✅ **{field_name}** dikemas kini kepada: **{new_value}**",
        "invalid_value": "❌ {error_message} Sila masukkan nilai yang sah.",
        "edit_field_prompt": "📝 **Medan mana yang ingin anda edit?**",
        "cancel_edit_button": "Batal",
        "edit_button": "📝 Edit",
        "delete_button": "🗑 Padam",
        "previous_button": "⬅️ Sebelumnya",
        "next_button": "➡️ Seterusnya",
        "editable_fields": {
            "Nama": "name",
            "Nama Individu": "person_name",
            "Hubungan": "relationship",
            "Lokasi Terakhir Dilihat": "last_seen_location",
            "Jantina": "gender",
            "Umur": "age",
            "Warna Rambut": "hair_color",
            "Warna Mata": "eye_color",
            "Ketinggian": "height",
            "Berat Badan": "weight",
            "Ciri-ciri Ketara": "distinctive_features",
            "Negara": "country",
            "Bandar": "city",
        },
        "case_details_template": (
            "📌 **Butiran Kes**\n"
            "👤 **Nama Individu:** {person_name}\n"
            "📍 **Lokasi Terakhir Dilihat:** {last_seen_location}\n"
            "💰 **Hadiah:** {reward} {reward_type}\n"
            "💼 **Dompet:** {wallet}\n"
            "👤 **Jantina:** {gender}\n"
            "🧒 **Umur:** {age}\n"
            "📏 **Ketinggian:** {height} cm\n"
        ),
        "invalid_reward_amount": "❌ Jumlah hadiah tidak sah. Jumlah hadiah maksimum adalah {max_amount}.",
        "reward_success": "✅ Hadiah berjaya dihantar kepada pencari {finder_id}.",
        "error_transferring_reward": "❌ Ralat berlaku semasa menghantar hadiah.",
        "case_or_finder_not_found": "❌ Kes atau pencari tidak ditemui.",
        "no_finders_for_case": "❌ Tiada pencari ditemui untuk kes ini.",
        "finder_list_header": "👤 **Pencari untuk kes ini:**",
        "reward_this_finder": "💰 Beri hadiah kepada pencari ini",
        "enter_reward_amount": "✏️ Sila masukkan jumlah hadiah untuk kes ini (maks {max_amount}): ",
        "reward_confirmation": "Adakah anda pasti ingin menghantar {amount} hadiah kepada Pencari ID {finder_id} untuk Kes {case_no}?",
        "reward_cancelled": "Proses hadiah dibatalkan",
        "confirm_button": "✅ Sahkan",
        "cancel_button": "❌ Batal",
        # ----- Delete Start ------
        "case_not_found": "⚠️ Kes tidak ditemui.",
        "not_authorized_delete": "🚫 Anda tidak dibenarkan untuk memadam kes ini.",
        "case_deleted_successfully": "✅ Kes telah berjaya dipadam.",
        "confirm_delete": "❗ Adakah anda pasti ingin memadam kes ini?",
        "yes": "✅ Ya",
        "no": "❌ Tidak",
        "delete_cancelled": "❌ Pemadaman kes telah dibatalkan.",
        "error_deleting_case": "⚠️ Ralat berlaku semasa memadam kes. Sila cuba lagi.",
        # ----- Delete End ------
        # ----------- Extend Reward Constants ----------
        "extend_reward_button": "Tambah Hadiah ➕",
        "extend_reward_not_found": "❌ Tiada permintaan tambahan hadiah aktif ditemui.",
        "insufficient_funds": "❌ Baki dompet {wallet_type} tidak mencukupi. Diperlukan: {required_amount}",
        "extend_reward_confirmation": (
            "🔄 *Sahkan Penambahan Hadiah*\n\n"
            "💰 Jumlah: {amount} {wallet_type}\n"
            "📤 Dari: `{from_wallet}`\n"
            "📥 Ke: `{to_wallet}`\n"
            "Adakah anda pasti ingin meneruskan?"
        ),
        "extend_success": "✅ Berjaya menambah {amount} {wallet_type} hadiah!",
        "extend_cancelled": "❌ Penambahan hadiah dibatalkan.",
        "transfer_failed": "❌ Pemindahan gagal. Sila semak baki dompet dan cuba lagi.",
        "case_or_extend_not_found": "❌ Kes atau permintaan tambahan tidak ditemui.",
        "insufficient_funds_after_selection": "❌ Baki tidak mencukupi dalam dompet yang dipilih.",
        "extend_already_completed": "⚠️ Permintaan tambahan hadiah ini sudah selesai.",
        "error_processing_extend": "❌ Ralat berlaku semasa memproses permintaan tambahan hadiah.",
        "error_approving_extend": "❌ Ralat berlaku semasa meluluskan permintaan tambahan hadiah.",
        "case_not_found": "❌ Kes tidak ditemui.",
        "extend_reward_not_found": "❌ Tiada permintaan tambahan hadiah yang belum selesai untuk kes ini.",
    },
}
