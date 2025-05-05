# src/handlers/stats_handler.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
     ConversationHandler,
    ContextTypes,
 
)

from constants import State
from models.case_model import Case, CaseStatus
from services.static_service import StatsService
from constant.language_constant import get_text
from utils.helper import get_city_matches, get_province_matches, paginate_list


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    stats = await StatsService.get_global_stats()

    message = (
        f"{get_text(user_id, 'community_stats_title')}\n"
        f"{get_text(user_id, 'total_cases_submitted').format(stats['total_cases'])}\n"
        f"{get_text(user_id, 'regions_covered').format(stats['countries'], stats['cities'])}\n"
        f"{get_text(user_id, 'unsolved_cases').format(stats['unsolved'])}\n"
        f"{get_text(user_id, 'successfully_found').format(stats['solved'])}\n"
        f"{get_text(user_id, 'average_reward_offered').format(stats['avg_reward'])}\n"
        f"{get_text(user_id, 'fastest_case_solved').format(stats['fastest'])}\n"
        f"{get_text(user_id, 'top_active_region').format(stats['top_region'])}\n"
        f"{get_text(user_id, 'common_demographic').format(stats['top_demo'])}\n"
        f"{get_text(user_id, 'highest_reward').format(stats['highest'])}"
    )

    keyboard = [
        [InlineKeyboardButton(get_text(user_id, "view_unsolved_cases_button"), callback_data="view_unsolved")],
        [InlineKeyboardButton(get_text(user_id, "view_local_stats_button"), callback_data="view_local_stats")],
        [InlineKeyboardButton(get_text(user_id, "my_submissions_button"), callback_data="view_my_cases")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(message, reply_markup=reply_markup, parse_mode="HTML")
    elif update.callback_query:
        await update.callback_query.edit_message_text(message, reply_markup=reply_markup, parse_mode="HTML")

    return State.SHOW_STATS_MENU


# Main menu callbacks
async def stats_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "view_unsolved":
        countries = await StatsService.get_unsolved_by_country()
        if not countries:
            await query.edit_message_text(
                get_text(user_id, "no_unsolved_country"),
                parse_mode="Markdown",
            )
            return ConversationHandler.END

        keyboard = [[InlineKeyboardButton(f"{c['name']} ({c['count']})", callback_data=f"country_{c['name']}")] for c in countries]
        keyboard.append([InlineKeyboardButton(get_text(user_id, "back_button"), callback_data="back_to_stats")])

        await query.edit_message_text(
            get_text(user_id, "unsolved_country_list"),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )
        return State.SHOW_UNSOLVED_COUNTRIES

    elif query.data == "view_local_stats":
        text = get_text(user_id, "ask_for_local_stats_input")
        keyboard = [[InlineKeyboardButton(get_text(user_id, "back_button"), callback_data="back_to_stats")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode="HTML")
        return State.ASK_LOCAL_PROVINCE_CITY

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
        await query.edit_message_text(get_text(user_id, "no_cases_in_country").format(country))
        return State.SHOW_STATS_MENU

    message = get_text(user_id, "unsolved_cases_in_country").format(country)
    keyboard = [[InlineKeyboardButton(f"Case {case.person_name or 'Unknown'}", callback_data=f"case_{case.id}")] for case in cases]
    keyboard.append([InlineKeyboardButton(get_text(user_id, "back_button"), callback_data="view_unsolved")])

    await query.edit_message_text(message, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
    return State.SHOW_STATS_MENU


# List user-submitted cases
async def view_my_cases_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    cases = await Case.find(Case.user_id == user_id, Case.status != CaseStatus.DRAFT.value, Case.deleted != True).to_list()

    if not cases:
        await query.edit_message_text(get_text(user_id, "you_havent_submitted_cases"))
        return State.SHOW_STATS_MENU

    message = get_text(user_id, "your_submitted_cases_title")
    keyboard = [[InlineKeyboardButton(f"Case {case.name or 'N/A'} - {case.person_name or 'Unknown'}", callback_data=f"mycase_{case.id}")] for case in cases]
    keyboard.append([InlineKeyboardButton(get_text(user_id, "back_button"), callback_data="back_to_stats")])

    await query.edit_message_text(message, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
    return State.SHOW_MY_CASES


# View details of a single case
async def my_case_detail_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    case_id = query.data.replace("mycase_", "")
    case = await Case.get(case_id)

    if not case:
        await query.edit_message_text("❌ " + get_text(user_id, "case_not_found"))
        return State.SHOW_MY_CASES

    message = (
        f"{get_text(user_id, 'case_details_title')}\n"
        f"{get_text(user_id, 'case_no_label').format(case.case_no or 'N/A')}\n"
        f"{get_text(user_id, 'name_label').format(case.person_name or 'N/A')}\n"
        f"{get_text(user_id, 'status_label').format(case.status.value.capitalize())}\n"
        f"{get_text(user_id, 'last_seen_label').format(case.last_seen_location or 'N/A')}\n"
        f"{get_text(user_id, 'reward_label').format(case.reward or 0, case.reward_type or 'USDT')}\n"
        f"{get_text(user_id, 'created_at_label').format(case.created_at.strftime('%Y-%m-%d'))}"
    )

    keyboard = [[InlineKeyboardButton(get_text(user_id, "back_button"), callback_data="view_my_cases")]]
    await query.edit_message_text(message, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
    return State.SHOW_MY_CASES


# Ask user for their province and city
async def ask_local_province_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    # Ask for input
    text = get_text(user_id, "ask_for_local_stats_input")
    await query.edit_message_text(text=text, parse_mode="HTML")
    return State.SHOW_LOCAL_STATS_RESULTS


# Handle province/city input and show local cases
async def handle_local_province_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message = update.message.text.strip()

    try:
        city, province = [part.strip() for part in message.split(",", 1)]
    except ValueError:
        # Invalid format
        await update.message.reply_text(get_text(user_id, "invalid_local_stats_format"), parse_mode="HTML")
        return State.ASK_LOCAL_PROVINCE_CITY

    # Save for later use (optional)
    context.user_data["local_city"] = city
    context.user_data["local_province"] = province

    # Fetch local cases
    cases = await Case.find({"city": city, "province": province, "status": CaseStatus.ADVERTISE.value}).to_list()

    if not cases:
        await update.message.reply_text(
            get_text(user_id, "no_local_cases_found").format(city=city, province=province),
            parse_mode="HTML"
        )
        return ConversationHandler.END

    # Build keyboard with cases
    keyboard = [
        [InlineKeyboardButton(f"Case {case.person_name or 'Unknown'}", callback_data=f"case_{case.id}")]
        for case in cases
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        get_text(user_id, "local_cases_found_title").format(city=city, province=province),
        reply_markup=reply_markup,
        parse_mode="HTML"
    )
    return ConversationHandler.END


# Optional fallback
async def invalid_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        get_text(query.from_user.id, "invalid_selection_error"),
        parse_mode="HTML"
    )
    return ConversationHandler.END


# Fallback cancel handler
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Operation cancelled.")
    return ConversationHandler.END