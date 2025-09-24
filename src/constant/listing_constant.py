LISTING_CONSTANT = {
    "english": {
        "no_advertise_cases": "No advertise cases found. Please check back later.",
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
        "enter_new_value": '✏️ What should the new value for "{field_name}" be?',
        "field_updated_successfully": "✅ **{field_name}** updated to: **{new_value}**",
        "invalid_value": "❌ {error_message} Please enter a valid value.",
        "edit_field_prompt": "📝 **Which field would you like to edit?**",
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
            "Province": "province",
            "City": "city",
            "Mobile Number": "mobile",
            "Reason": "reason",
        },
        "error_updating_field": "❌ An error occurred while updating the field. Please try again.",
        "error_canceling_edit": "❌ An error occurred while canceling the edit. Please try again.",
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
        ## ERROR CASES
        "error_processing_reward": "❌ Error processing your reward. Please try again.",
        "error_asking_reward_amount": "❌ Error asking reward amount. Please try again.",
        "enter_reward_amount": "Please enter the reward amount you want to send: (max {max_amount})",
        "extend_reward_header": "🔄 Extend Reward",
        "no_wallet_selected": "🚫 No wallet selected. Please try again.",
        "error_fetching_finder": "❌ Error fetching finder details. Please try again.",
        "no_proof_available": "🚫 No proof available. Please upload a valid image file.",
        "invalid_request": "Invalid request. Please try again.",
        "case_deleted_successfully": "✅ Case has been successfully deleted.",
    }
}
