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
from services.user_service import get_user_lang, save_user_lang
from utils.error_wrapper import catch_async
from utils.helper import get_city_matches, get_country_matches, paginate_list
from constant.language_constant import LANG_DATA, get_text, user_data_store


@catch_async
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """/start command entry point."""
    user_id = update.message.from_user.id
    user_lang = await get_user_lang(user_id)
    raise Exception("Something went wrong")
    if user_lang:
        user_data_store[user_id] = {"lang": user_lang}
        context.user_data["lang"] = user_lang
        await update.message.reply_text(get_text(user_id, "choose_country"))
        return State.CHOOSE_COUNTRY

    # ✅ Show banner if user doesn't have a language set
    try:
        with open("static/banner.jpg", "rb") as banner:
            await update.message.reply_photo(
                photo=banner,
                caption="👋 Welcome to our bot!\nPlease choose your language below 👇",
            )
    except FileNotFoundError:
        # fallback if the image isn't available
        await update.message.reply_text("👋 Welcome to our bot!\nPlease choose your language below 👇")

    # ⬇️ Language selection buttons
    btns = [
        [
            InlineKeyboardButton(
                LANG_DATA["en"]["lang_button"], callback_data="lang_en"
            ),
            InlineKeyboardButton(
                LANG_DATA["zh"]["lang_button"], callback_data="lang_zh"
            ),
            InlineKeyboardButton(
                LANG_DATA["ms"]["lang_button"], callback_data="lang_ms"
            ),
        ]
    ]

    await update.message.reply_text(
        f"{LANG_DATA['en']['start_msg']}\n\n{LANG_DATA['zh']['start_msg']}",
        reply_markup=InlineKeyboardMarkup(btns),
    )

    return State.SELECT_LANG



#  ----------------------- Language LOGIC ------------------------
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

    await query.edit_message_text(get_text(user_id, "choose_country"))

    return State.CHOOSE_COUNTRY


#  ----------------------- Country LOGIC ------------------------
@catch_async
async def choose_country(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    txt = update.message.text.strip()
    matches = get_country_matches(txt)
    if not matches:
        await update.message.reply_text(
            get_text(user_id, "country_not_found"), parse_mode="HTML"
        )
        return State.CHOOSE_COUNTRY
    if len(matches) == 1:
        context.user_data["country"] = matches[0]
        await update_or_create_case(user_id, country=matches[0])
        await update.message.reply_text(
            f"{get_text(user_id, 'country_selected')} {matches[0]}",
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
                    InlineKeyboardButton("⬅️", callback_data="country_page_0"),
                    InlineKeyboardButton("➡️", callback_data="country_page_2"),
                ]
            )
        markup = InlineKeyboardMarkup(kb)
        await update.message.reply_text(
            get_text(user_id, "country_multi").format(page=1, total=total),
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

        await update.message.reply_text(
            f"{get_text(user_id, 'country_selected')} {country}",
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
                InlineKeyboardButton("⬅️", callback_data=f"country_page_{page_num-1}")
            )
        if page_num < total:
            nav_row.append(
                InlineKeyboardButton("➡️", callback_data=f"country_page_{page_num+1}")
            )
        if nav_row:
            kb.append(nav_row)
        markup = InlineKeyboardMarkup(kb)
        await query.edit_message_text(
            get_text(user_id, "country_multi").format(page=page_num, total=total),
            reply_markup=markup,
            parse_mode="HTML",
        )

        context.user_data["country_page"] = page_num
        return State.CHOOSE_COUNTRY
    else:
        await query.edit_message_text(
            get_text(user_id, "invalid_choice"), parse_mode="HTML"
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
    text = (
        f"{get_text(user_id, 'disclaimer_title')}{get_text(user_id, 'disclaimer_text')}"
    )
    kb = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    get_text(user_id, "agree_btn"), callback_data="agree"
                )
            ],
            [
                InlineKeyboardButton(
                    get_text(user_id, "disagree_btn"), callback_data="disagree"
                )
            ],
        ]
    )
    if update.callback_query:
        await update.callback_query.answer(text, parse_mode="HTML", reply_markup=kb)
    else:
        await update.message.reply_text(text, parse_mode="HTML", reply_markup=kb)
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
        await query.edit_message_text(get_text(user_id, "enter_province"))
        return State.START_CHOOSE_PROVINCE
    else:
        await query.edit_message_text(
            get_text(user_id, "disagree_end"), parse_mode="HTML"
        )
        return State.END


# ----------------------- Province LOGIC ------------------------

async def start_choose_province(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles province selection and shows cases for that province."""
    user_id = update.effective_user.id
    txt = update.message.text.strip()

    # Get country from user_data
    country = context.user_data.get("country")
    if not country:
        await update.message.reply_text(
            get_text(user_id, "country_not_found"), parse_mode="HTML"
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
            f"{get_text(user_id, 'province_selected')} {matches[0]}.",
            parse_mode="HTML",
        )
        await update.message.reply_text(
            get_text(user_id, "enter_city"), parse_mode="HTML"
        )
        return State.CHOOSE_CITY

    elif len(matches) == 0:
        await update.message.reply_text(
            get_text(user_id, "province_not_exist"),
            parse_mode="HTML",  # Ensure consistency in parse_mode
        )
        return State.START_CHOOSE_PROVINCE

    else:
        # Multiple matches – show inline keyboard
        context.user_data["province_matches"] = matches
        context.user_data["province_page"] = 1
        paginated, total = paginate_list(matches, 1)

        kb = [[InlineKeyboardButton(p, callback_data=f"start_province_select_{p}")] for p in paginated]

        if total > 1:
            kb.append([
                InlineKeyboardButton("⬅️", callback_data="start_province_page_0"),
                InlineKeyboardButton("➡️", callback_data="start_province_page_2"),
            ])

        markup = InlineKeyboardMarkup(kb)
        await update.message.reply_text(
            get_text(user_id, "province_multi").format(page=1, total=total),
            reply_markup=markup,
            parse_mode="HTML",
        )
        return State.START_CHOOSE_PROVINCE


async def start_province_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = update.effective_user.id

    if data.startswith("start_province_select_"):
        province = data.replace("start_province_select_", "")
        context.user_data["province"] = province
        await query.edit_message_text(
            f"{get_text(user_id, 'province_selected')} {province}.",
            parse_mode="HTML",
        )
        await query.message.reply_text(
            get_text(user_id, "enter_city"), parse_mode="HTML"
        )
        return State.CHOOSE_CITY

    elif data.startswith("start_province_page_"):
        try:
            page_num = max(1, int(data.replace("start_province_page_", "")))
        except ValueError:
            page_num = 1

        matches = context.user_data.get("province_matches", [])
        paginated, total = paginate_list(matches, page_num)

        kb = [[InlineKeyboardButton(p, callback_data=f"start_province_select_{p}")] for p in paginated]

        nav_row = []
        if page_num > 1:
            nav_row.append(InlineKeyboardButton("⬅️", callback_data=f"start_province_page_{page_num - 1}"))
        if page_num < total:
            nav_row.append(InlineKeyboardButton("➡️", callback_data=f"start_province_page_{page_num + 1}"))
        if nav_row:
            kb.append(nav_row)

        markup = InlineKeyboardMarkup(kb)
        await query.edit_message_text(
            get_text(user_id, "province_multi").format(page=page_num, total=total),
            reply_markup=markup,
            parse_mode="HTML",
        )

        context.user_data["province_page"] = page_num
        return State.START_CHOOSE_PROVINCE

    else:
        await query.edit_message_text(
            get_text(user_id, "invalid_choice"), parse_mode="HTML"
        )
        return State.END




@catch_async
async def choose_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    city_input = update.message.text.strip()
    country = context.user_data.get("country")
    if not country:
        await update.message.reply_text(
            get_text(user_id, "invalid_choice"), parse_mode="HTML"
        )
        return State.END
    matches = get_city_matches(country, city_input)
    if not matches:
        await update.message.reply_text(
            get_text(user_id, "city_not_found"), parse_mode="HTML"
        )
        return State.CHOOSE_CITY
    if len(matches) == 1:
        context.user_data["city"] = matches[0]
        await update_or_create_case(user_id, city=matches[0])

        await update.message.reply_text(
            f"{get_text(user_id, 'city_selected')} {matches[0]}",
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
                    InlineKeyboardButton("⬅️", callback_data="city_page_0"),
                    InlineKeyboardButton("➡️", callback_data="city_page_2"),
                ]
            )
        markup = InlineKeyboardMarkup(kb)
        await update.message.reply_text(
            get_text(user_id, "city_multi").format(page=1, total=total),
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
            f"{get_text(user_id, 'city_selected')} {city}", parse_mode="HTML"
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
                InlineKeyboardButton("⬅️", callback_data=f"city_page_{page_num-1}")
            )
        if page_num < total:
            nav_row.append(
                InlineKeyboardButton("➡️", callback_data=f"city_page_{page_num+1}")
            )
        if nav_row:
            kb.append(nav_row)
        markup = InlineKeyboardMarkup(kb)
        await query.edit_message_text(
            get_text(user_id, "city_multi").format(page=page_num, total=total),
            reply_markup=markup,
            parse_mode="HTML",
        )
        context.user_data["city_page"] = page_num
        return State.CHOOSE_CITY
    else:
        await query.edit_message_text(
            get_text(user_id, "invalid_choice"), parse_mode="HTML"
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
                    get_text(user_id, "advertise_btn"), callback_data="advertise"
                ),
                InlineKeyboardButton(
                    get_text(user_id, "find_btn"), callback_data="find_people"
                ),
            ]
        ]
    )
    if update.callback_query:
        await update.callback_query.message.reply_text(
            get_text(user_id, "choose_action"), reply_markup=kb
        )
    else:
        await update.message.reply_text(
            get_text(user_id, "choose_action"), reply_markup=kb
        )
    return State.CHOOSE_ACTION


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
        # From the original code, it goes to CHOOSE_WALLET_TYPE
        kb = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        get_text(user_id, "usdt_wallet"), callback_data="USDT"
                    ),
                    InlineKeyboardButton(
                        get_text(user_id, "sol_wallet"), callback_data="SOL"
                    ),
                ]
            ]
        )
        await query.edit_message_text(
            get_text(user_id, "choose_wallet"), reply_markup=kb
        )
        return State.CHOOSE_WALLET_TYPE
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
                    f"Case {case.person_name} ({case.id})",
                    callback_data=f"case_{str(case.id)}",
                )
            ]
            for case in paginated_cases
        ]

        # Add pagination buttons
        navigation_buttons = []
        if total_pages > 1:
            navigation_buttons.append(
                InlineKeyboardButton("⬅️ Previous", callback_data="case_page_previous")
            )
            navigation_buttons.append(
                InlineKeyboardButton("➡️ Next", callback_data="case_page_next")
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
            get_text(user_id, "invalid_choice"), parse_mode="HTML"
        )
        return State.END


# DEBUGGING FROM START
@catch_async
async def wallet_type_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    # Determine wallet type (SOL or USDT) from callback data
    wallet_type = query.data

    context.user_data["wallet_type"] = wallet_type

    print(f"Wallet type: {wallet_type}")

    existing_wallets = await WalletService.get_wallet_by_type(user_id, wallet_type)

    if existing_wallets:
        kb = [
            [
                InlineKeyboardButton(
                    wallet.name, callback_data=f"wallet_{str(wallet.id)}"
                )
            ]
            for wallet in existing_wallets
        ]
        kb.append(
            [
                InlineKeyboardButton(
                    get_text(user_id, "create_new_wallet"),
                    callback_data="create_new_wallet",
                )
            ]
        )
        await query.edit_message_text(
            get_text(user_id, "choose_existing_or_new_wallet"),
            reply_markup=InlineKeyboardMarkup(kb),
            parse_mode="HTML",
        )
        return State.CHOOSE_WALLET_TYPE
    else:
        msg = get_text(user_id, "wallet_name_prompt").format(wallet_type=wallet_type)
        if update.message:
            await update.message.reply_text(msg, parse_mode="HTML")
        elif update.callback_query:
            await update.callback_query.message.reply_text(msg, parse_mode="HTML")

        return State.NAME_WALLET


@catch_async
async def wallet_selection_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    # Extract wallet name and type from callback data
    wallet_id = query.data.replace("wallet_", "")
    wallet_type = context.user_data.get("wallet_type")  # 'sol' or 'usdt'

    # Fetch wallet details by name and type
    wallet_details = await WalletService.get_wallet_by_id(wallet_id)

    print(f"Wallet details: {wallet_details}")

    if wallet_details:
        # Fetch balance for the specific wallet type (SOL or USDT)
        print(f"This is the wallet type: {wallet_type}")

        total_sol = (
            await WalletService.get_sol_balance(wallet_details["public_key"])
            if wallet_type == "SOL"
            else await TronWallet.get_usdt_balance(wallet_details["public_key"])
        )

        print(f"Total {wallet_type}: {total_sol}")

        context.user_data["wallet"] = wallet_details  # Store in memory
        await update_or_create_case(user_id, wallet=str(wallet_details["id"]))

        msg = get_text(user_id, "wallet_create_details").format(
            name=wallet_details["name"],
            public_key=wallet_details["public_key"],
            # secret_key=wallet_details["private_key"],
            balance=total_sol,  # For USDT, balance might be different
            wallet_type=wallet_type,
        )

        transfer_instructions = get_text(user_id, "transfer_instructions").format(
            wallet_type=wallet_type,
            public_key=wallet_details["public_key"],
        )
        msg += transfer_instructions

        await query.edit_message_text(msg, parse_mode="HTML")


        keyboard = [
            [InlineKeyboardButton("✅ Create Case", callback_data="create_case")],
            [InlineKeyboardButton("🕵️ Find People", callback_data="find_people"),
            InlineKeyboardButton("⚙️ Settings", callback_data="settings")],
            [InlineKeyboardButton("❓ Help", url="https://t.me/peopletrace")]
        ]



      

        await query.message.reply_text(
            "Choose an option below to continue:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return State.HANDLE_REPLY  # Use a custom state if needed
    else:
        await query.edit_message_text(
            get_text(user_id, "wallet_not_found"), parse_mode="HTML"
        )
        return State.END


@catch_async
async def wallet_name_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    query = update.callback_query
    wallet_type = context.user_data.get("wallet_type")  # 'sol' or 'usdt'
    user_id = update.effective_user.id
    if update.callback_query:
        # If it's a callback query, prompt the user to enter a wallet name
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            get_text(user_id, "wallet_name_prompt").format(wallet_type=wallet_type),
            parse_mode="HTML",
        )
        return State.NAME_WALLET

    wallet_name = update.message.text.strip()

    print(f"Wallet name: {wallet_name}")

    if not wallet_name:
        await update.message.reply_text(
            get_text(user_id, "wallet_name_empty"), parse_mode="HTML"
        )
        return State.NAME_WALLET

    print("Hello there how are you doing", wallet_name)

    wallet_type = context.user_data.get("wallet_type")

    print(f"Wallet type: {wallet_type}")

    if await WalletService.check_wallet_name_used_with_type(
        user_id, wallet_name, wallet_type
    ):
        message = (
            "A wallet with this name already exists. Please choose a different name."
        )
        await update.message.reply_text(message)
        return State.NAME_WALLET

    wallet = await WalletService.create_wallet(user_id, wallet_type, wallet_name)
    if wallet:

        if wallet_type == "SOL":
            total_sol = await WalletService.get_sol_balance(wallet.public_key)
        elif wallet_type == "USDT":
            total_sol = await TronWallet.get_usdt_balance(wallet.public_key)

        print(f"Total SOL: {total_sol}")
        print(f"This is the wallet type: {wallet_type}")

        context.user_data["wallet"] = wallet
        await update_or_create_case(user_id, wallet=str(wallet.id))
        msg = get_text(user_id, "wallet_create_details").format(
            name=wallet.name,
            public_key=wallet.public_key,
            # secret_key=wallet.private_key,
            balance=total_sol,  # For USDT, the balance logic will vary
            wallet_type=wallet_type,
        )

        transfer_instructions = get_text(user_id, "transfer_instructions").format(
            wallet_type=wallet_type,
            public_key=wallet.public_key,
        )
        msg += transfer_instructions

        await update.message.reply_text(msg, parse_mode="HTML")

      
       
        # 🎯 Custom Reply Keyboard (FIXED)
        keyboard = [
            [InlineKeyboardButton("✅ Create Case", callback_data="create_case")],
            [InlineKeyboardButton("🕵️ Find People", callback_data="find_people"), InlineKeyboardButton("⚙️ Settings", callback_data="settings")],
            [InlineKeyboardButton("❓ Help", url="https://t.me/peopletrace")]
        ]

     

        await update.message.reply_text(
            "Choose an option below to continue:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        return State.HANDLE_REPLY  # Use a custom state if needed
    else:
        await update.message.reply_text(
            get_text(user_id, "wallet_create_err"), parse_mode="HTML"
        )
        return State.END

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
        await query.edit_message_text(get_text(user_id, "create_case_title"))
        await query.message.reply_text(get_text(user_id, "enter_name"))
        return State.CREATE_CASE_NAME

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
                    f"Case {case.person_name} ({case.id})",
                    callback_data=f"case_{str(case.id)}",
                )
            ]
            for case in paginated_cases
        ]

        # Add pagination buttons
        navigation_buttons = []
        if total_pages > 1:
            navigation_buttons.append(
                InlineKeyboardButton("⬅️ Previous", callback_data="case_page_previous")
            )
            navigation_buttons.append(
                InlineKeyboardButton("➡️ Next", callback_data="case_page_next")
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
            disable_web_page_preview=True
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
                get_text(user_id, "invalid_choice")
            )

            

async def interrupt_current_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # End any current conversation
    context.user_data.clear()
    return ConversationHandler.END



async def jump_to_command(update, context, command_text: str):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=command_text
    )
    return ConversationHandler.END





@catch_async
async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id

    keyboard = [
        [InlineKeyboardButton("✅ Create Case", callback_data="create_case")],
        [InlineKeyboardButton("🕵️ Find People", callback_data="find_people"),
         InlineKeyboardButton("⚙️ Settings", callback_data="settings")],
        [InlineKeyboardButton("❓ Help", url="https://t.me/peopletrace")]
    ]

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Choose an option below to continue:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    return State.HANDLE_REPLY
