# handlers/stats_handler.py
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from constant.language_constant import get_text
from constants import State
from services.static_service import StatsService

def format_number(value):
    if value is None:
        return "0"
    if value >= 1_000_000:
        return f"{value/1_000_000:.1f}M"
    if value >= 1_000:
        return f"{value/1_000:.1f}K"
    return f"{value:,}"


async def stats_command(update: Update, context): # type: ignore
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
        [InlineKeyboardButton("🗂 My Submissions", callback_data="view_my_cases")],
        [InlineKeyboardButton("⬅️ Back to Menu", callback_data="back_to_main_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(message, reply_markup=reply_markup, parse_mode="HTML")
    return State.SHOW_STATS_MENU

# handlers/stats_handler.py

async def stats_menu_callback(update: Update, context): # type: ignore
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
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            get_text(user_id, "unsolved_country_list"),
            reply_markup=reply_markup,
            parse_mode="HTML"
        )
        return State.SHOW_UNSOLVED_COUNTRIES

    elif query.data == "view_local_stats":
        # Stub — you can show city/province specific stats here
        await query.edit_message_text("📍 Coming soon: Local Stats based on your location.")
        return State.SHOW_STATS_MENU

    elif query.data == "view_my_cases":
        # Redirect to your existing listing functionality
        await query.edit_message_text("📂 Redirecting to your case submissions...")
        return await context.bot.send_message(
            chat_id=user_id, text="/mycases"
        )

    elif query.data == "back_to_main_menu":
        await query.edit_message_text(get_text(user_id, "main_menu_text"))
        return ConversationHandler.END


# handlers/stats_handler.py

async def unsolved_country_callback(update: Update, context):
    query = update.callback_query
    await query.answer()
    country = query.data.replace("country_", "")
    user_id = query.from_user.id

    # Fetch cases from that country
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
