from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    ContextTypes,
)
from constant.language_constant import get_text
from constants import State
from services.static_service import StatsService
from models.case_model import Case


def format_number(value):
    if value is None:
        return "0"
    if value >= 1_000_000:
        return f"{value/1_000_000:.1f}M"
    if value >= 1_000:
        return f"{value/1_000:.1f}K"
    return f"{value:,}"


# /stats command
async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    stats = await StatsService.get_global_stats()

    message = (
        f"<b>📊 PeopleTrace Community Stats</b>\n"
        f"• <b>Total Cases Submitted:</b> {format_number(stats['total_cases'])}\n"
        f"• <b>Regions Covered:</b> {stats['countries']} countries, {stats['cities']} cities\n"
        f"• <b>🕵️‍♂️ Unsolved Cases:</b> {format_number(stats['unsolved'])} (Click below 👇)\n"
        f"• <b>✅ Successfully Found:</b> {format_number(stats['solved'])}\n"
        f"• <b>🎁 Average Reward Offered:</b> {stats['avg_reward']} USDT\n"
        f"• <b>⏱ Fastest Case Solved:</b> {stats['fastest']} days\n"
        f"• <b>🔥 Top Active Region:</b> {stats['top_region']}\n"
        f"• <b>🧑‍🤝‍🧑 Common Demographic:</b> {stats['top_demo']}\n"
        f"• <b>💰 Highest Reward:</b> {stats['highest']} USDT"
    )

    keyboard = [
        [InlineKeyboardButton("🕵️ View Unsolved Cases", callback_data="view_unsolved")],
        [InlineKeyboardButton("📍 View Local Stats", callback_data="view_local_stats")],
        [InlineKeyboardButton("📂 My Submissions", callback_data="view_my_cases")],
        [InlineKeyboardButton("⬅️ Back to Menu", callback_data="back_to_main_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(message, reply_markup=reply_markup, parse_mode="HTML")
    return State.SHOW_STATS_MENU


# Main menu callbacks
async def stats_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "view_unsolved":
        countries = await StatsService.get_unsolved_by_country()
        keyboard = [
            [InlineKeyboardButton(f"{c['name']} ({c['count']})", callback_data=f"country_{c['name']}")]
            for c in countries
        ]
        keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="back_to_stats")])

        await query.edit_message_text(
            get_text(user_id, "unsolved_country_list"),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )
        return State.SHOW_UNSOLVED_COUNTRIES

    elif query.data == "view_local_stats":
        await query.edit_message_text("📍 Coming soon: Local Stats based on your location.")
        return State.SHOW_STATS_MENU

    elif query.data == "view_my_cases":
        return await view_my_cases_callback(update, context)

    elif query.data == "back_to_main_menu":
        await query.edit_message_text(get_text(user_id, "main_menu_text"))
        return ConversationHandler.END


# Back button logic
async def back_to_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await stats_command(update, context)


# Show unsolved cases for a selected country
async def unsolved_country_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    country = query.data.replace("country_", "")
    user_id = query.from_user.id

    cases = await StatsService.get_unsolved_cases_by_country(country)

    if not cases:
        await query.edit_message_text(f"No cases found in {country}.")
        return State.SHOW_STATS_MENU

    message = f"<b>🕵️ Unsolved Cases in {country}:</b>\n"
    keyboard = [
        [InlineKeyboardButton(f"Case {case.case_no} - {case.person_name}", callback_data=f"case_{case.id}")]
        for case in cases
    ]
    keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="view_unsolved")])

    await query.edit_message_text(message, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
    return State.SHOW_STATS_MENU


# List user-submitted cases
async def view_my_cases_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    cases = await Case.find(Case.user_id == user_id, Case.deleted != True).to_list()

    if not cases:
        await query.edit_message_text("📂 You haven’t submitted any cases yet.")
        return State.SHOW_STATS_MENU

    message = "<b>📂 Your Submitted Cases:</b>\n"
    keyboard = [
        [InlineKeyboardButton(f"Case {case.case_no or 'N/A'} - {case.person_name or 'Unknown'}", callback_data=f"mycase_{case.id}")]
        for case in cases
    ]
    keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="back_to_stats")])

    await query.edit_message_text(message, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
    return State.SHOW_MY_CASES


# View details of a single case
async def my_case_detail_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    case_id = query.data.replace("mycase_", "")
    case = await Case.get(case_id)

    if not case:
        await query.edit_message_text("❌ Case not found.")
        return State.SHOW_MY_CASES

    message = (
        f"<b>📄 Case Details</b>\n"
        f"• <b>Case No:</b> {case.case_no or 'N/A'}\n"
        f"• <b>Name:</b> {case.person_name or 'N/A'}\n"
        f"• <b>Status:</b> {case.status.value.capitalize()}\n"
        f"• <b>Last Seen:</b> {case.last_seen_location or 'N/A'}\n"
        f"• <b>Reward:</b> {case.reward or 0} {case.reward_type or 'USDT'}\n"
        f"• <b>Created At:</b> {case.created_at.strftime('%Y-%m-%d')}"
    )
    keyboard = [[InlineKeyboardButton("⬅️ Back", callback_data="view_my_cases")]]
    await query.edit_message_text(message, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
    return State.SHOW_MY_CASES


# Optional fallback
async def invalid_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "⚠️ <b>Invalid Selection</b>\n\nPlease choose a valid option.",
        parse_mode="HTML"
    )
    return ConversationHandler.END

