import logging
from handlers.finder_handler import choose_province, get_province_matches
from handlers.settings_handler import settings_command
from models.case_model import Case, CaseStatus
from services.case_service import update_or_create_case
from services.finder_service import FinderService
from services.tron_wallet_service import TronWallet
from services.wallet_service import WalletService
from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import (
    ConversationHandler,
    ContextTypes,
)
from constants import (
    State,
)
from services.user_service import get_user_lang, get_user_mobiles, save_user_lang
from utils.error_wrapper import catch_async
from utils.get_network import get_network
from utils.helper import get_city_matches, get_country_matches, paginate_list
from constant.language_constant import LANG_DATA, get_text, user_data_store


@catch_async
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start command: show banner, ask for language, then show disclaimer."""
    user_id = update.message.from_user.id
    # Step 1: Send Banner Image
    BANNER_URL = "https://ibb.co/SDj7ycyZ"  # Replace with your actual image URL
    # Language buttons
    btns = [
        [
            InlineKeyboardButton(
                f"{LANG_DATA["globals"]['english']['lang_button']}",
                callback_data="lang_english",
            ),
            InlineKeyboardButton(
                f"{LANG_DATA["globals"]['chinese']['lang_button']}",
                callback_data="lang_chinese",
            ),
        ],
        [
            InlineKeyboardButton(
                f"{LANG_DATA["globals"]['malay']['lang_button']}",
                callback_data="lang_malay",
            ),
            InlineKeyboardButton(
                f"{LANG_DATA["globals"]['thai']['lang_button']}",
                callback_data="lang_thai",
            ),
        ],
        [
            InlineKeyboardButton(
                f"{LANG_DATA["globals"]['vietnamese']['lang_button']}",
                callback_data="lang_vietnamese",
            ),
            InlineKeyboardButton(
                f"{LANG_DATA["globals"]['urdu']['lang_button']}",
                callback_data="lang_urdu",
            ),
        ],
        [
            InlineKeyboardButton(
                f"{LANG_DATA["globals"]['japanese']['lang_button']}",
                callback_data="lang_japanese",
            ),
            InlineKeyboardButton(
                f"{LANG_DATA["globals"]['korean']['lang_button']}",
                callback_data="lang_korean",
            ),
        ],
        [
            InlineKeyboardButton(
                f"{LANG_DATA["globals"]['khmer']['lang_button']}",
                callback_data="lang_khmer",
            ),
            InlineKeyboardButton(
                f"{LANG_DATA["globals"]['indonesian']['lang_button']}",
                callback_data="lang_indonesian",
            ),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(btns)
    # Step 2: Send image + caption asking to choose language
    await update.message.reply_photo(
        photo=BANNER_URL,
        caption="<b>👋 Welcome to PeopleTrace</b>\n\n🌐 Please select your language:",
        reply_markup=reply_markup,
        parse_mode="HTML",
    )

    return State.LANGUAGE_SELECTED


@catch_async
async def select_lang_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle language selection."""
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id
    lang = data.replace("lang_", "")
    await save_user_lang(user_id, lang)
    user_data_store[user_id] = {"lang": lang}
    context.user_data["lang"] = lang
    await query.message.delete()
    await query.message.reply_text(
        get_text(user_id, "choose_country", "start-complaints")
    )

    return State.CHOOSE_COUNTRY


#  ----------------------- Country LOGIC ------------------------
@catch_async
async def choose_country(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    txt = update.message.text.strip()

    matches = get_country_matches(txt)
    if not matches:
        await update.message.reply_text(
            get_text(user_id, "country_not_found", "start-complaints"),
            parse_mode="HTML",
        )
        return State.CHOOSE_COUNTRY
    if len(matches) == 1:
        context.user_data["country"] = matches[0]
        await update_or_create_case(user_id, country=matches[0])
        message = update.message
        await message.reply_text(
            f"{get_text(user_id, 'country_selected', "start-complaints")} {matches[0]}",
            parse_mode="HTML",
        )

        await show_disclaimer(update, context)
        return State.SHOW_DISCLAIMER
    else:

        context.user_data["country_matches"] = matches
        context.user_data["country_page"] = 1

        paginated, total = paginate_list(matches, 1)
        kb = []
        for c in paginated:
            kb.append([InlineKeyboardButton(c, callback_data=f"country_select_{c}")])
        # Pagination buttons
        if total > 1:
            kb.append(
                [
                    InlineKeyboardButton(get_text(user_id, "prev", "globals"), callback_data="country_page_0"),
                    InlineKeyboardButton(get_text(user_id, "next", "globals"), callback_data="country_page_2"),
                ]
            )
        markup = InlineKeyboardMarkup(kb)
        await update.message.reply_text(
            get_text(user_id, "country_multi", "start-complaints").format(
                page=1, total=total
            ),
            reply_markup=markup,
            parse_mode="HTML",
        )
        return State.CHOOSE_COUNTRY


@catch_async
async def country_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id
    if data.startswith("country_select_"):

        country = data.replace("country_select_", "")
        context.user_data["country"] = country
        await update_or_create_case(user_id, country=country)

        message = update.message or query.message
        if update.message:
            await update.message.edit_message_text(
                f"{get_text(user_id, 'country_selected', "start-complaints")} {country}",
                parse_mode="HTML",
            )
        else:
            await query.message.edit_text(
                f"{get_text(user_id, 'country_selected', "start-complaints")} {country}",
                parse_mode="HTML",
            )

        await show_disclaimer(update, context)
        return State.SHOW_DISCLAIMER
    elif data.startswith("country_page_"):
        page_str = data.replace("country_page_", "")
        try:
            page_num = int(page_str)
            if page_num < 1:
                page_num = 1
        except ValueError:
            page_num = 1
        matches = context.user_data.get("country_matches", [])
        paginated, total = paginate_list(matches, page_num)
        kb = []
        for c in paginated:
            kb.append([InlineKeyboardButton(c, callback_data=f"country_select_{c}")])
        nav_row = []
        if page_num > 1:
            nav_row.append(
                InlineKeyboardButton(get_text(user_id, "prev", "globals"), callback_data=f"country_page_{page_num-1}")
            )
        if page_num < total:
            nav_row.append(
                InlineKeyboardButton(get_text(user_id, "next", "globals"), callback_data=f"country_page_{page_num+1}")
            )
        if nav_row:
            kb.append(nav_row)
        markup = InlineKeyboardMarkup(kb)
        await query.edit_message_text(
            get_text(user_id, "country_multi", "start-complaints").format(
                page=page_num, total=total
            ),
            reply_markup=markup,
            parse_mode="HTML",
        )

        context.user_data["country_page"] = page_num
        return State.CHOOSE_COUNTRY
    else:
        await query.edit_message_text(
            get_text(user_id, "invalid_choice", "globals"), parse_mode="HTML"
        )
        return State.END


#  ----------------------- Disclaimer LOGIC ------------------------
@catch_async
async def show_disclaimer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = (
        update.effective_user.id
        if update.message
        else update.callback_query.from_user.id
    )
    text = f"{get_text(user_id, 'disclaimer_text', "start-complaints")}"
    kb = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    get_text(user_id, "agree_btn", "globals"), callback_data="agree"
                )
            ],
            [
                InlineKeyboardButton(
                    get_text(user_id, "disagree_btn", "globals"),
                    callback_data="disagree",
                )
            ],
        ]
    )
    if update.callback_query:
        await update.callback_query.message.reply_text(
            text, parse_mode="Markdown", reply_markup=kb
        )
    else:
        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=kb)
    return State.SHOW_DISCLAIMER


@catch_async
async def disclaimer_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    if query.data == "agree":
        # Clearing the province
        await query.edit_message_text(
            get_text(user_id, "enter_province", "start-complaints")
        )
        return State.START_CHOOSE_PROVINCE
    else:
        await query.edit_message_text(
            get_text(user_id, "disagree_end"), parse_mode="HTML"
        )
        return State.END


# ----------------------- Province LOGIC ------------------------


async def start_choose_province(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handles province selection and shows cases for that province."""
    user_id = update.effective_user.id
    txt = update.message.text.strip()

    # Get country from user_data
    country = context.user_data.get("country")
    if not country:
        await update.message.reply_text(
            get_text(user_id, "country_not_found", "start-complaints"),
            parse_mode="HTML",
        )
        return State.CHOOSE_COUNTRY

    # Get matching provinces
    matches = get_province_matches(txt, country)
    print(f"Matched Provinces are: {matches}")

    if len(matches) == 1:
        # Only one match – save and proceed
        context.user_data["province"] = matches[0]
        await update_or_create_case(user_id, province=matches[0])

        await update.message.reply_text(
            f"{get_text(user_id, 'selected', "globals")} {matches[0]}.",
            parse_mode="HTML",
        )
        await update.message.reply_text(
            get_text(user_id, "enter_city", "start-complaints"), parse_mode="HTML"
        )
        return State.CHOOSE_CITY

    elif len(matches) == 0:
        await update.message.reply_text(
            get_text(user_id, "province_not_exist", "start-complaints"),
            parse_mode="HTML",  # Ensure consistency in parse_mode
        )
        return State.START_CHOOSE_PROVINCE

    else:
        # Multiple matches – show inline keyboard
        context.user_data["province_matches"] = matches
        context.user_data["province_page"] = 1
        paginated, total = paginate_list(matches, 1)

        kb = [
            [InlineKeyboardButton(p, callback_data=f"start_province_select_{p}")]
            for p in paginated
        ]

        if total > 1:
            kb.append(
                [
                    InlineKeyboardButton(get_text(user_id, "prev", "globals"), callback_data="start_province_page_0"),
                    InlineKeyboardButton(get_text(user_id, "next", "globals"), callback_data="start_province_page_2"),
                ]
            )

        markup = InlineKeyboardMarkup(kb)
        await update.message.reply_text(
            get_text(user_id, "province_multi", "start-complaints").format(page=1, total=total),
            reply_markup=markup,
            parse_mode="HTML",
        )
        return State.START_CHOOSE_PROVINCE


async def start_province_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = update.effective_user.id

    if data.startswith("start_province_select_"):
        province = data.replace("start_province_select_", "")
        context.user_data["province"] = province
        await query.edit_message_text(
            f"{get_text(user_id, 'selected', "globals")} {province}",
            parse_mode="HTML",
        )
        await query.message.reply_text(
            get_text(user_id, "enter_city", "start-complaints"), parse_mode="HTML"
        )
        return State.CHOOSE_CITY

    elif data.startswith("start_province_page_"):
        try:
            page_num = max(1, int(data.replace("start_province_page_", "")))
        except ValueError:
            page_num = 1

        matches = context.user_data.get("province_matches", [])
        paginated, total = paginate_list(matches, page_num)

        kb = [
            [InlineKeyboardButton(p, callback_data=f"start_province_select_{p}")]
            for p in paginated
        ]

        nav_row = []
        if page_num > 1:
            nav_row.append(
                InlineKeyboardButton(
                    get_text(user_id, "prev", "globals"), callback_data=f"start_province_page_{page_num - 1}"
                )
            )
        if page_num < total:
            nav_row.append(
                InlineKeyboardButton(
                    get_text(user_id, "next", "globals"), callback_data=f"start_province_page_{page_num + 1}"
                )
            )
        if nav_row:
            kb.append(nav_row)

        markup = InlineKeyboardMarkup(kb)
        await query.edit_message_text(
            get_text(user_id, "province_multi", "start-complaints").format(page=page_num, total=total),
            reply_markup=markup,
            parse_mode="HTML",
        )

        context.user_data["province_page"] = page_num
        return State.START_CHOOSE_PROVINCE

    else:
        await query.edit_message_text(
            get_text(user_id, "invalid_choice", "globals"), parse_mode="HTML"
        )
        return State.END


@catch_async
async def choose_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    city_input = update.message.text.strip()
    country = context.user_data.get("country")
    if not country:
        await update.message.reply_text(
            get_text(user_id, "invalid_choice", "globals"), parse_mode="HTML"
        )
        return State.END
    matches = get_city_matches(country, city_input)
    if not matches:
        await update.message.reply_text(
            get_text(user_id, "city_not_found", "start-complaints"), parse_mode="HTML"
        )
        return State.CHOOSE_CITY
    if len(matches) == 1:
        context.user_data["city"] = matches[0]
        await update_or_create_case(user_id, city=matches[0])

        await update.message.reply_text(
            f"{get_text(user_id, 'city_selected', "start-complaints")} {matches[0]}",
            parse_mode="HTML",
        )
        await choose_action(update, context)
        return State.CHOOSE_ACTION
    else:
        context.user_data["city_matches"] = matches
        context.user_data["city_page"] = 1
        paginated, total = paginate_list(matches, 1)
        kb = []
        for c in paginated:
            kb.append([InlineKeyboardButton(c, callback_data=f"city_select_{c}")])
        # Pagination
        if total > 1:
            kb.append(
                [
                    InlineKeyboardButton(get_text(user_id, "prev", "globals"), callback_data="city_page_0"),
                    InlineKeyboardButton(get_text(user_id, "next", "globals"), callback_data="city_page_2"),
                ]
            )
        markup = InlineKeyboardMarkup(kb)
        await update.message.reply_text(
            get_text(user_id, "city_multi", "start-complaints").format(page=1, total=total),
            reply_markup=markup,
            parse_mode="HTML",
        )
        return State.CHOOSE_CITY


@catch_async
async def city_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data
    if data.startswith("city_select_"):
        city = data.replace("city_select_", "")
        context.user_data["city"] = city
        await update_or_create_case(user_id, city=city)

        await query.edit_message_text(
            f"{get_text(user_id, 'city_selected', "start-complaints")} {city}",
            parse_mode="HTML",
        )
        await choose_action(update, context)
        return State.CHOOSE_ACTION
    elif data.startswith("city_page_"):
        page_str = data.replace("city_page_", "")
        try:
            page_num = int(page_str)
            if page_num < 1:
                page_num = 1
        except ValueError:
            page_num = 1
        matches = context.user_data.get("city_matches", [])
        paginated, total = paginate_list(matches, page_num)
        kb = []
        for c in paginated:
            kb.append([InlineKeyboardButton(c, callback_data=f"city_select_{c}")])
        nav_row = []
        if page_num > 1:
            nav_row.append(
                InlineKeyboardButton(get_text(user_id, "prev", "globals"), callback_data=f"city_page_{page_num-1}")
            )
        if page_num < total:
            nav_row.append(
                InlineKeyboardButton(get_text(user_id, "next", "globals" ), callback_data=f"city_page_{page_num+1}")
            )
        if nav_row:
            kb.append(nav_row)
        markup = InlineKeyboardMarkup(kb)
        await query.edit_message_text(
            get_text(user_id, "city_multi", "start-complaints").format(
                page=page_num, total=total
            ),
            reply_markup=markup,
            parse_mode="HTML",
        )
        context.user_data["city_page"] = page_num
        return State.CHOOSE_CITY
    else:
        await query.edit_message_text(
            get_text(user_id, "invalid_choice", "globals"), parse_mode="HTML"
        )
        return State.END


@catch_async
async def choose_action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = (
        update.effective_user.id
        if update.message
        else update.callback_query.from_user.id
    )
    kb = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    get_text(user_id, "advertise_btn", "start-complaints"),
                    callback_data="advertise",
                ),
                InlineKeyboardButton(
                    get_text(user_id, "find_btn", "start-complaints"),
                    callback_data="find_people",
                ),
            ]
        ]
    )
    if update.callback_query:
        await update.callback_query.message.reply_text(
            get_text(user_id, "choose_action", "start-complaints"), reply_markup=kb
        )
    else:
        await update.message.reply_text(
            get_text(user_id, "choose_action", "start-complaints"), reply_markup=kb
        )
    return State.CHOOSE_ACTION


#  Ended  Start Command


@catch_async
async def action_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    choice = query.data
    province = context.user_data.get("province", None)
    country = context.user_data.get("country", None)
    city = context.user_data.get("city", None)

    if choice == "advertise":
        existing_mobiles = await get_user_mobiles(user_id)

        print(f"Mobile numbers: {existing_mobiles}")

        if existing_mobiles:
            kb = [
                [InlineKeyboardButton(mobile, callback_data=f"select_mobile_{mobile}")]
                for mobile in existing_mobiles
            ]
            kb.append([InlineKeyboardButton("➕ Add New", callback_data="mobile_add")])

            await query.edit_message_text(
                get_text(user_id, "choose_existing_mobile", "start-mobile"),
                reply_markup=InlineKeyboardMarkup(kb),
            )
            return State.MOBILE_MANAGEMENT
        else:
            await query.edit_message_text(
                get_text(user_id, "enter_mobile_post_case", "start-complaints"), parse_mode="Markdown"
            )
            return State.CREATE_CASE_MOBILE
    elif choice == "find_people":
        # Clearing the province
        await FinderService.update_or_create_finder(
            user_id=user_id,
            province=province,
            city=city,
            country=country,
        )
        context.user_data["province"] = province  # Save province in context

        # Fetch cases from DB where last_seen_location matches province
        cases = await Case.find(
            {"province": province, "status": CaseStatus.ADVERTISE}
        ).to_list()

        if not cases:
            await query.edit_message_text(
                get_text(user_id, "no_case_found_in_province", "start-complaints").format(
                    province=province
                ),
                parse_mode="Markdown",
            )
            return State.START_CHOOSE_PROVINCE

        # Save case list in context for pagination
        context.user_data["cases"] = cases
        context.user_data["page"] = 1

        # Paginate cases
        paginated_cases, total_pages = paginate_list(cases, 1)

        # Create keyboard buttons for cases
        keyboard = [
            [
                InlineKeyboardButton(
                    f"{case.name} ({case.person_name})",
                    callback_data=f"case_{str(case.id)}",
                )
            ]
            for case in paginated_cases
        ]

        # Add pagination buttons
        navigation_buttons = []
        if total_pages > 1:
            navigation_buttons.append(
                InlineKeyboardButton(get_text(user_id, "prev", "globals"), callback_data="case_page_previous")
            )
            navigation_buttons.append(
                InlineKeyboardButton(get_text(user_id, "next", "globals"), callback_data="case_page_next")
            )
        if navigation_buttons:
            keyboard.append(navigation_buttons)

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            f"📍 **Cases from {province}:**",
            reply_markup=reply_markup,
            parse_mode="Markdown",
        )
        return State.CASE_DETAILS
    else:
        await query.edit_message_text(
            get_text(user_id, "invalid_choice", "globals"), parse_mode="HTML"
        )
        return State.END






#  Ended Start Command



@catch_async
async def message_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    choice = query.data
    province = context.user_data.get("province", None)
    country = context.user_data.get("country", None)
    city = context.user_data.get("city", None)

    if choice == "create_case":
        await query.edit_message_text(
            get_text(user_id, "create_case_title", "cases"), parse_mode="HTML"
        )
        await query.message.reply_text(get_text(user_id, "enter_person_name", "cases"))
        return State.CREATE_CASE_PERSON_NAME

    elif choice == "find_people":
        # Clearing the province
        await FinderService.update_or_create_finder(
            user_id=user_id,
            province=province,
            city=city,
            country=country,
        )
        context.user_data["province"] = province  # Save province in context

        # Fetch cases from DB where last_seen_location matches province
        cases = await Case.find(
            {"province": province, "status": CaseStatus.ADVERTISE}
        ).to_list()

        if not cases:
            await query.edit_message_text(
                get_text(user_id, "no_case_found_in_province").format(
                    province=province
                ),
                parse_mode="Markdown",
            )
            return State.START_CHOOSE_PROVINCE

        # Save case list in context for pagination
        context.user_data["cases"] = cases
        context.user_data["page"] = 1

        # Paginate cases
        paginated_cases, total_pages = paginate_list(cases, 1)

        # Create keyboard buttons for cases
        keyboard = [
            [
                InlineKeyboardButton(
                    f"{case.name} ({case.person_name})",
                    callback_data=f"case_{str(case.id)}",
                )
            ]
            for case in paginated_cases
        ]

        # Add pagination buttons
        navigation_buttons = []
        if total_pages > 1:
            navigation_buttons.append(
                InlineKeyboardButton(get_text(user_id, "prev", "globals"), callback_data="case_page_previous")
            )
            navigation_buttons.append(
                InlineKeyboardButton(get_text(user_id, "next", "globals"), callback_data="case_page_next")
            )
        if navigation_buttons:
            keyboard.append(navigation_buttons)

        reply_markup = InlineKeyboardMarkup(keyboard)

        # TODO: would be replace later
        await query.edit_message_text(
            f"📍 **Cases from {province}:**",
            reply_markup=reply_markup,
            parse_mode="Markdown",
        )
        return State.CASE_DETAILS

    elif choice == "settings":
        # ✅ Optional: Remove previous inline keyboard
        await query.edit_message_reply_markup(reply_markup=None)

        # ✅ Clear user and chat data
        context.user_data.clear()
        context.chat_data.clear()

        # ✅ Trigger the actual settings command handler
        return await settings_command(update, context)

    elif choice == "help":
        await query.edit_message_text(
            "Need help? Visit: https://t.me/your_other_bot_or_help_page",
            disable_web_page_preview=True,
        )
        return State.HANDLE_REPLY

    elif choice == "go_back":
        return await main_menu(update, context)

    else:
        await query.edit_message_text("❗ Please choose an option using the buttons.")
        return State.HANDLE_REPLY






# handlers/shared.py
@catch_async
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    return ConversationHandler.END


@catch_async
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger = logging.getLogger(__name__)
    logger.error("Exception:", exc_info=context.error)
    if isinstance(update, Update) and update.effective_message:
        user_id = update.effective_user.id if update.effective_user else None
        if user_id:
            await update.effective_message.reply_text(
                get_text(user_id, "invalid_choice", "globals")
            )


async def interrupt_current_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # End any current conversation
    context.user_data.clear()
    return ConversationHandler.END


async def jump_to_command(update, context, command_text: str):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=command_text)
    return ConversationHandler.END


@catch_async
async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id

    create_case_btn = get_text(user_id, "create_case_btn")
    find_people_btn = get_text(user_id, "find_btn")
    settings_btn = get_text(user_id, "btn_language")
    help_btn = get_text(user_id, "help_command")

    keyboard = [
        [InlineKeyboardButton(f"✅ {create_case_btn}", callback_data="create_case")],
        [
            InlineKeyboardButton(f"🕵️ {find_people_btn}", callback_data="find_people"),
            InlineKeyboardButton(f"⚙️ {settings_btn}", callback_data="settings"),
        ],
        [InlineKeyboardButton(f"❓ {help_btn}", url="https://t.me/peopletrace")],
    ]

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Choose an option below to continue:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

    return State.HANDLE_REPLY
