import logging
from datetime import datetime
from beanie import PydanticObjectId
from config.config_manager import (
    OWNER_TELEGRAM_ID,
    STAKE_WALLET_PRIVATE_KEY,
    STAKE_WALLET_PUBLIC_KEY,
    TAX_COLLECT_PUBLIC_KEY,
    TRON_TAX_COLLECT_PUBLIC_KEY,
    TRON_WALLET_PRIVATE_KEY,
)
from constant.language_constant import get_text, user_data_store
from constants import State
from models.case_model import Case, CaseStatus
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, error
from telegram.ext import (
    ContextTypes,
)
from bson import ObjectId, errors
import traceback
from models.extend_reward_model import ExtendReward
from models.finder_model import Finder, FinderStatus
from models.wallet_model import Wallet
from services.case_service import update_case
from services.finder_service import FinderService
from services.tron_wallet_service import TronWallet
from services.user_service import get_user_lang
from services.wallet_service import WalletService
from utils.logger import logger
from utils.error_wrapper import catch_async
from utils.helper import get_city_matches, get_country_matches, paginate_list


@catch_async
async def listing_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handler for the /listing command."""
    user_id = update.effective_user.id
    logger.info(f"User {user_id} issued /listing command")
    all_cases = (
        await Case.find({"status": CaseStatus.ADVERTISE, "deleted": False})
        .sort(-Case.created_at)  # Sorting in descending order
        .to_list()
    )

    logger.info(f"Fetched {len(all_cases)} ADVERTISE cases from the database")
    user_lang = await get_user_lang(user_id)
    if user_lang:
        user_data_store[user_id] = {"lang": user_lang}
        context.user_data["lang"] = user_lang
    if not all_cases:
        if update.message:
            await update.message.reply_text(get_text(user_id, "no_advertise_cases"))
        elif update.callback_query:
            await update.callback_query.message.edit_text(
                get_text(user_id, "no_advertise_cases")
            )
        return State.END
    context.user_data["page"] = 1
    context.user_data["cases"] = all_cases
    paginated_cases, total_pages = paginate_list(all_cases, 1)
    keyboard = []
    for case in paginated_cases:
        row = [
            InlineKeyboardButton(
                f"Case {case.case_no} - {case.person_name}",
                callback_data=f"case_{str(case.id)}",
            )
        ]
        finder_exist = await Finder.find(
            {"case.$id": PydanticObjectId(case.id), "status": FinderStatus.FIND}
        ).to_list()

        if case.user_id == user_id and len(finder_exist) == 0:
            row.append(
                InlineKeyboardButton(
                    get_text(user_id, "edit_button"),
                    callback_data=f"edit_{str(case.id)}",
                )
            )
            row.append(
                InlineKeyboardButton(
                    get_text(user_id, "delete_button"),
                    callback_data=f"delete_{str(case.id)}",
                )
            )

        print(user_id, OWNER_TELEGRAM_ID)

        if str(user_id) == str(OWNER_TELEGRAM_ID) and finder_exist:
            row.append(
                InlineKeyboardButton(
                    # get_text(user_id, "reward_button"),
                    "Reward Finder",
                    callback_data=f"reward_{str(case.id)}",
                )
            )
        keyboard.append(row)

        # In the listing_command function, after checking for edit/delete buttons:
        extend_reward = await ExtendReward.find_one(
            {"case.$id": PydanticObjectId(case.id)}
        )
        print(extend_reward)
        if case.status == CaseStatus.ADVERTISE and extend_reward:
            if case.user_id == user_id:  # Ensure only the owner sees the button
                row.append(
                    InlineKeyboardButton(
                        get_text(user_id, "extend_reward_button"),
                        callback_data=f"extend_reward_{str(case.id)}",
                    )
                )

    navigation_buttons = []
    current_page = context.user_data["page"]
    if current_page > 1:
        navigation_buttons.append(
            InlineKeyboardButton(
                get_text(user_id, "previous_button"), callback_data="page_previous"
            )
        )
    if current_page < total_pages:
        navigation_buttons.append(
            InlineKeyboardButton(
                get_text(user_id, "next_button"), callback_data="page_next"
            )
        )
    if navigation_buttons:
        keyboard.append(navigation_buttons)
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        if update.message:
            await update.message.reply_text(
                get_text(user_id, "select_case_details"),
                reply_markup=reply_markup,
                parse_mode="Markdown",
            )
        elif update.callback_query:
            await update.callback_query.message.edit_text(
                get_text(user_id, "select_case_details"),
                reply_markup=reply_markup,
                parse_mode="Markdown",
            )
    except error.BadRequest as e:
        if "Message is not modified" in str(e):
            await update.callback_query.answer(
                "Cases are already updated.", show_alert=True
            )

    return State.CASE_DETAILS


@catch_async
async def case_details_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handler for displaying case details when a button is clicked."""
    user_id = update.effective_user.id
    query = update.callback_query
    await query.answer()

    try:
        case_id = query.data.removeprefix("case_")  # Extract case ID
        case = await Case.find_one(
            {"_id": PydanticObjectId(case_id), "deleted": False}, fetch_links=True
        )
        print("THIS IS THE CASE", case)

        if not case:
            await query.message.edit_text(get_text(user_id, "case_not_found"))
            return State.END  # Terminate the conversation

        # Fetch wallet and mobile number details if they exist

        # Format the case details using the constant template
        proof_text = (
            f"[Proof]({case.case_photo})"
            if case.case_photo and case.case_photo.startswith("http")
            else "No proof available"
        )

        case_message = get_text(
            user_id,
            "case_details_template",
        ).format(
            person_name=case.person_name,
            last_seen_location=case.last_seen_location,
            reward=case.reward or "None",
            reward_type=case.reward_type or "None",
            wallet="wallet",  # TODO: its remains
            gender=case.gender,
            age=case.age,
            height=case.height,
        )

        case_message += f"\n\n**Proof:** {proof_text}"

        keyboard = []
        if case.user_id == user_id:
            row = [
                InlineKeyboardButton(
                    get_text(user_id, "edit_button"),
                    callback_data=f"edit_{str(case.id)}",
                ),
                InlineKeyboardButton(
                    get_text(user_id, "delete_button"),
                    callback_data=f"delete_{str(case.id)}",
                ),
            ]
            keyboard.append(row)

        reply_markup = InlineKeyboardMarkup(keyboard)

        # Edit the message to show case details
        await query.message.edit_text(
            case_message.strip(),
            reply_markup=reply_markup,
            parse_mode="Markdown",
        )
        if case.user_id == user_id:
            return State.CASE_DETAILS

        return State.END  # Terminate the conversation

    except Exception as e:
        logger.error(
            f"Error in case_details_callback: {str(e)}\n{traceback.format_exc()}"
        )
        await query.message.edit_text(get_text(user_id, "error_fetching_case_details"))
        return State.END  # Terminate the conversation


@catch_async
async def pagination_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handler for the pagination (Next/Previous) buttons."""
    query = update.callback_query
    await query.answer()

    try:
        # Get current page and case list from user data
        current_page = context.user_data.get("page", 1)
        cases = context.user_data.get("cases", [])
        user_id = update.effective_user.id

        # Determine navigation action (next or previous)
        if query.data == "page_next":
            new_page = current_page + 1
        elif query.data == "page_previous":
            new_page = current_page - 1
        else:
            new_page = current_page

        # Paginate the case list based on the new page
        paginated_cases, total_pages = paginate_list(cases, new_page)

        # Save the new page in context
        context.user_data["page"] = new_page

        # Create the inline keyboard with case buttons
        keyboard = []
        for case in paginated_cases:

            row = [
                InlineKeyboardButton(
                    f"Case {case.case_no} - {case.name}",
                    callback_data=f"case_{str(case.id)}",
                )
            ]

            finder_exist = await Finder.find(
                {"case.$id": PydanticObjectId(case.id), "status": FinderStatus.FIND}
            ).to_list()
            print(f"Finder exist: {finder_exist}")
            if case.user_id == update.effective_user.id and len(finder_exist) == 0:

                row.append(
                    InlineKeyboardButton(
                        get_text(user_id, "edit_button"),
                        callback_data=f"edit_{str(case.id)}",
                    )
                )
                row.append(
                    InlineKeyboardButton(
                        get_text(user_id, "delete_button"),
                        callback_data=f"delete_{str(case.id)}",
                    )
                )

            #
            keyboard.append(row)

        # Add navigation buttons
        navigation_buttons = []
        if new_page > 1:
            navigation_buttons.append(
                InlineKeyboardButton(
                    get_text(user_id, "previous_button"), callback_data="page_previous"
                )
            )
        if new_page < total_pages:
            navigation_buttons.append(
                InlineKeyboardButton(
                    get_text(user_id, "next_button"), callback_data="page_next"
                )
            )
        if navigation_buttons:
            keyboard.append(navigation_buttons)

        reply_markup = InlineKeyboardMarkup(keyboard)

        # Edit the message with the updated case list
        await query.message.edit_text(
            get_text(user_id, "select_case_details"),
            reply_markup=reply_markup,
            parse_mode="Markdown",
        )
        return State.CASE_DETAILS
    except Exception as e:
        logger.error(
            f"Error in pagination_callback: {str(e)}\n{traceback.format_exc()}"
        )
        await query.message.edit_text(get_text(user_id, "error_paginating_cases"))
        return State.END


@catch_async
async def edit_case_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handler for editing a case."""
    query = update.callback_query
    await query.answer()

    # Extract case_id from callback data
    case_id = query.data.removeprefix("edit_")
    if "_" in case_id:
        case_id = case_id.split("_", maxsplit=1)[-1]  # Extract only the case ID

    print(f"Extracted case_id: {case_id}")

    # Validate case_id
    try:
        case_id = ObjectId(case_id)
    except errors.InvalidId:
        await query.message.edit_text(get_text(user_id, "invalid_case_id"))
        return State.END

    # Fetch the case from the database
    case = await Case.find_one({"_id": case_id})
    if not case:
        await query.message.edit_text(get_text(user_id, "case_not_found"))
        return State.END

    user_id = update.effective_user.id
    if case.user_id != user_id:
        await query.message.edit_text(get_text(user_id, "not_authorized_edit"))
        return State.END

    # Fetch editable fields based on the user's language
    editable_fields = get_text(user_id, "editable_fields")

    # Group buttons in rows of 2
    keyboard = [
        [
            InlineKeyboardButton(f"{k1}", callback_data=f"edit_field_{v1}_{case_id}"),
            InlineKeyboardButton(f"{k2}", callback_data=f"edit_field_{v2}_{case_id}"),
        ]
        for (k1, v1), (k2, v2) in zip(
            list(editable_fields.items())[::2], list(editable_fields.items())[1::2]
        )
    ]

    # If there's an odd number of fields, add the last button separately
    if len(editable_fields) % 2 != 0:
        last_key, last_value = list(editable_fields.items())[-1]
        keyboard.append(
            [
                InlineKeyboardButton(
                    f"{last_key}", callback_data=f"edit_field_{last_value}_{case_id}"
                )
            ]
        )

    # Add cancel button
    keyboard.append(
        [
            InlineKeyboardButton(
                get_text(user_id, "cancel_edit_button"), callback_data="cancel_edit"
            )
        ]
    )

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.edit_text(
        get_text(user_id, "edit_field_prompt"),
        reply_markup=reply_markup,
        parse_mode="Markdown",
    )
    return State.CASE_DETAILS


@catch_async
async def edit_field_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Ask the user to enter a new value for the selected field."""
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id

    # Extract field and case ID from callback data
    callback_data = query.data.removeprefix("edit_field_")
    last_underscore_index = callback_data.rfind("_")
    field_name = callback_data[:last_underscore_index]
    case_id = callback_data[last_underscore_index + 1 :]

    print("Field name:", field_name, "Case ID:", case_id)

    context.user_data["editing_case_id"] = case_id
    context.user_data["editing_field"] = field_name

    # If editing country, prompt for country first
    if field_name == "country":
        await query.message.edit_text("🌍 Please enter your country:")
        return State.ENTER_COUNTRY

    # If editing city, first ensure country is set
    if field_name == "city":
        if "country" not in context.user_data:
            await query.message.edit_text("🌍 Please enter your country first:")
            return State.ENTER_COUNTRY
        await query.message.edit_text("🏙️ Please enter your city:")
        return State.ENTER_CITY

    # For other fields
    await query.message.edit_text(
        get_text(user_id, "enter_new_value").format(
            field_name=field_name.replace("_", " ").title()
        ),
        parse_mode="Markdown",
    )
    return State.EDIT_FIELD


@catch_async
async def update_case_field(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Update the specified field in the case document."""
    print("I'm Calling :smile")
    case_id = context.user_data.get("editing_case_id")
    field_name = context.user_data.get("editing_field")
    user_id = update.effective_user.id
    new_value = update.message.text.strip()

    print(f"CaseId: {case_id}, Field Name: {field_name}, New Value: {new_value}")

    if not case_id or not field_name:
        await update.message.reply_text(get_text(user_id, "invalid_request"))
        return State.END

    # Fetch the case
    case = await Case.find_one({"_id": PydanticObjectId(case_id)})
    if not case:
        await update.message.reply_text(get_text(user_id, "case_not_found"))
        return State.END

    try:
        if field_name == "country":
            country_matches = get_country_matches(new_value)
            if not country_matches:
                raise ValueError("Invalid country. Please provide a valid country.")
            new_value = country_matches[0]
        elif field_name == "city":
            country = context.user_data.get("country")
            if not get_city_matches(country, new_value):
                raise ValueError(f"Invalid city for country {country}.")

        # Update the case document
        setattr(case, field_name, new_value)
        case.updated_at = datetime.utcnow()
        await case.save()

        await update.message.reply_text(
            get_text(
                user_id,
                "field_updated_successfully",
            ).format(
                field_name=field_name.replace("_", " ").title(),
                new_value=new_value,
            ),
            parse_mode="Markdown",
        )
    except ValueError as e:
        await update.message.reply_text(
            get_text(user_id, "invalid_value").format(error_message=str(e))
        )
        return State.EDIT_FIELD

    return State.END


@catch_async
async def enter_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ask the user to enter the country."""
    await update.message.reply_text("🌍 Please enter your country:")
    return State.ENTER_COUNTRY


@catch_async
async def process_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process and validate the country. Prompt for city if valid."""
    country = update.message.text.strip()
    country_matches = get_country_matches(country)

    if country_matches:
        context.user_data["country"] = country_matches[0]
        await update.message.reply_text(
            f"✅ You've entered **{country_matches[0]}**. Now, please enter your city:"
        )
        return State.ENTER_CITY
    else:
        await update.message.reply_text(
            "❌ Invalid country. Please enter a valid country from the list:\n"
            "- United States\n- Pakistan\n- Canada\n- United Kingdom"
        )
        return State.ENTER_COUNTRY


@catch_async
async def process_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Validate the city based on the previously entered country."""
    city = update.message.text.strip()
    country = context.user_data.get("country")

    cities = get_city_matches(country, city)

    if cities:
        case_id = context.user_data.get("editing_case_id")
        case = await Case.find_one({"_id": PydanticObjectId(case_id)})

        if case:
            setattr(case, "country", country)
            setattr(case, "city", city)
            case.updated_at = datetime.utcnow()
            await case.save()

        await update.message.reply_text(
            f"✅ Great! You've successfully added:\n\n"
            f"🌍 Country: **{country}**\n"
            f"🏙️ City: **{cities[0]}**"
        )
        return State.END
    else:
        await update.message.reply_text(
            f"❌ The city **{city}** is not valid for **{country}**.\n"
            "Please enter a valid city:"
        )
        return State.ENTER_CITY


@catch_async
async def update_choose_country(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:

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
        # Choose the country
        await update.message.reply_text("Choose a city:")
        return State.CHOOSE_CITY
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

        await query.edit_message_text(
            f"{get_text(user_id, 'country_selected')} {country}.",
            parse_mode="HTML",
        )
        # Choose the country
        await update.message.reply_text("Choose a city:")
        return State.CHOOSE_CITY
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
        await update.message.reply_text(
            f"{get_text(user_id, 'city_selected')} {matches[0]}",
            parse_mode="HTML",
        )
        update.message.reply_text("Updated Successfully")
        return State.END
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


# ------------------------ Delete Case Start ------------------------


@catch_async
async def delete_case_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handler for confirming and soft deleting a case."""
    query = update.callback_query
    await query.answer()

    case_id = query.data.removeprefix("delete_")

    # Extract case ID
    user_id = update.effective_user.id

    # Check if user is confirming deletion
    if case_id.startswith("confirm_"):
        case_id = case_id.removeprefix("confirm_")
        case = await Case.find_one({"_id": PydanticObjectId(case_id)})
        if not case:
            await query.edit_message_text(get_text(user_id, "case_not_found"))
            return State.END
        if case.user_id != user_id:
            await query.edit_message_text(get_text(user_id, "not_authorized_delete"))
            return State.END
        await update_case(case_id=PydanticObjectId(case_id), deleted=True)
        await query.edit_message_text(get_text(user_id, "case_deleted_successfully"))

        return await listing_command(update, context)

    keyboard = [
        [
            InlineKeyboardButton(
                get_text(user_id, "yes"), callback_data=f"delete_confirm_{case_id}"
            ),
            InlineKeyboardButton(
                get_text(user_id, "no"), callback_data="delete_cancel"
            ),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Check if message exists before editing
    if query.message:
        await query.edit_message_text(
            get_text(user_id, "confirm_delete"), reply_markup=reply_markup
        )
    else:
        await context.bot.send_message(
            chat_id=user_id,
            text=get_text(user_id, "confirm_delete"),
            reply_markup=reply_markup,
        )
    return State.CASE_DETAILS


@catch_async
async def cancel_delete_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handler to cancel delete request."""
    query = update.callback_query
    await query.answer()

    print("calling the cancel delete callback button ")
    try:
        if query.message:
            await query.edit_message_text(
                get_text(update.effective_user.id, "delete_cancelled")
            )
        else:
            await context.bot.send_message(
                chat_id=update.effective_user.id,
                text=get_text(update.effective_user.id, "delete_cancelled"),
            )
    except Exception as e:
        logger.error(f"Error in cancel_delete_callback: {str(e)}")

    return State.END


# ------------------------ Delete Case End ------------------------


@catch_async
async def cancel_edit_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handler for canceling the edit process."""
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id

    try:
        # Clear any edit-related data from context
        context.user_data.pop("edit_case_id", None)
        context.user_data.pop("edit_field", None)

        # Return to the case listing
        await query.message.edit_text(get_text(user_id, "edit_canceled"))
        return State.END
    except Exception as e:
        logger.error(
            f"Error in cancel_edit_callback: {str(e)}\n{traceback.format_exc()}"
        )
        await query.message.edit_text(get_text(user_id, "error_canceling_edit"))
        return State.END


# ---------------------------- Reward the Finder By Owner Started ---------------------------
@catch_async
async def reward_case_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handles the reward process when advertiser clicks 'Reward'."""
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    case_id = query.data.removeprefix("reward_")

    try:
        case = await Case.find_one({"_id": ObjectId(case_id)})
        if not case:
            await query.message.edit_text(get_text(user_id, "case_not_found"))
            return State.END

        finders = await Finder.find({"case.$id": PydanticObjectId(case.id)}).to_list()
        if not finders:
            await query.message.edit_text(get_text(user_id, "no_finders_for_case"))
            return State.END

        # Construct case details message
        case_details = get_text(user_id, "case_details_template").format(
            person_name=case.person_name,
            last_seen_location=case.last_seen_location,
            reward=case.reward,
            reward_type=case.reward_type,
            wallet=case.wallet,
            gender=case.gender,
            age=case.age,
            height=case.height,
        )

        # Show finders list below case details
        message = (
            case_details + "\n\n" + get_text(user_id, "finder_list_header") + "\n\n"
        )
        keyboard = []

        for finder in finders:
            keyboard.append(
                [
                    InlineKeyboardButton(
                        f"👤 Finder ID: {finder.user_id}",
                        callback_data=f"finder_details_{finder.user_id}_{case.id}",
                    )
                ]
            )

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text(
            message.strip(),
            reply_markup=reply_markup,
            parse_mode="Markdown",
        )
        return State.CASE_DETAILS

    except Exception as e:
        logger.error(
            f"Error in reward_case_callback: {str(e)}\n{traceback.format_exc()}"
        )
        await query.message.edit_text(get_text(user_id, "error_processing_reward"))
        return State.END


@catch_async
async def finder_details_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Displays details of the selected finder along with case details."""
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    data = query.data.removeprefix("finder_details_")
    finder_id, case_id = data.split("_")

    try:
        case = await Case.find_one({"_id": ObjectId(case_id)})
        finder = await Finder.find_one(
            {"user_id": int(finder_id), "case.$id": PydanticObjectId(case.id)}
        )

        if not case or not finder:
            await query.message.edit_text(get_text(user_id, "case_or_finder_not_found"))
            return State.END

        # Construct case details message
        case_details = get_text(user_id, "case_details_template").format(
            person_name=case.person_name,
            last_seen_location=case.last_seen_location,
            reward=case.reward,
            reward_type=case.reward_type,
            wallet=case.wallet,
            gender=case.gender,
            age=case.age,
            height=case.height,
        )

        # Finder details
        proof_text = (
            "\n".join(f"[Proof]({url})" for url in finder.proof_url)
            if finder.proof_url
            else get_text(user_id, "no_proof_available")
        )
        finder_details = (
            f"👤 *Finder ID:* `{finder.user_id}`\n"
            f"📍 *Location:* {finder.reported_location}\n"
            f"📎 *Proof:* {proof_text}\n"
        )

        message = case_details + "\n\n" + finder_details
        keyboard = [
            [
                InlineKeyboardButton(
                    get_text(user_id, "reward_this_finder"),
                    callback_data=f"send_reward_{finder.user_id}_{case.id}",
                )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text(
            message.strip(),
            reply_markup=reply_markup,
            parse_mode="Markdown",
        )
        return State.CASE_DETAILS

    except Exception as e:
        logger.error(
            f"Error in finder_details_callback: {str(e)}\n{traceback.format_exc()}"
        )
        await query.message.edit_text(get_text(user_id, "error_fetching_finder"))
        return State.END


@catch_async
async def ask_reward_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Asks advertiser how much reward they want to send."""
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    callback_data = query.data.removeprefix("send_reward_")
    finder_id, case_id = callback_data.split("_")

    try:
        case = await Case.find_one({"_id": ObjectId(case_id)})
        finder = await Finder.find_one(
            {"user_id": int(finder_id), "case.$id": PydanticObjectId(case.id)}
        )

        if not case or not finder:
            await query.message.edit_text(get_text(user_id, "case_or_finder_not_found"))
            return State.END

        context.user_data["reward_case_id"] = case.id
        context.user_data["reward_finder_id"] = finder.id

        await query.message.edit_text(
            get_text(user_id, "enter_reward_amount").format(max_amount=case.reward),
            parse_mode="Markdown",
        )
        return State.REWARD_TRANSFER_PROCESS  # Next step: user enters amount

    except Exception as e:
        logger.error(f"Error in ask_reward_amount: {str(e)}\n{traceback.format_exc()}")
        await query.message.edit_text(get_text(user_id, "error_asking_reward_amount"))
        return State.END


# Modify process_reward_transfer to show confirmation:
@catch_async
async def process_reward_transfer(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Shows confirmation before processing reward transfer"""
    user_id = update.effective_user.id
    amount = update.message.text.strip()
    case_id = context.user_data.get("reward_case_id")
    finder_id = context.user_data.get("reward_finder_id")

    try:
        case = await Case.find_one({"_id": ObjectId(case_id)})
        if not case:
            await update.message.reply_text(get_text(user_id, "case_not_found"))
            return State.END

        # Validate amount
        amount = float(amount)
        if amount <= 0 or amount > case.reward:
            raise ValueError("Invalid amount")

        # Store confirmation data
        context.user_data["reward_amount"] = amount

        # Show confirmation buttons
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        get_text(user_id, "confirm_button"),
                        callback_data="confirm_reward",
                    ),
                    InlineKeyboardButton(
                        get_text(user_id, "cancel_button"),
                        callback_data="cancel_reward",
                    ),
                ]
            ]
        )

        await update.message.reply_text(
            get_text(user_id, "reward_confirmation").format(
                amount=amount, finder_id=finder_id, case_no=case.case_no
            ),
            reply_markup=keyboard,
            parse_mode="Markdown",
        )
        return State.CONFIRM_REWARD

    except ValueError:
        await update.message.reply_text(
            get_text(user_id, "invalid_reward_amount").format(max_amount=case.reward)
        )
        return State.EDIT_FIELD


# New confirmation handler
@catch_async
async def confirm_reward(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Executes the reward transfer after confirmation"""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    try:
        case_id = context.user_data.get("reward_case_id")
        finder_id = context.user_data.get("reward_finder_id")
        amount = context.user_data.get("reward_amount")

        case = await Case.find_one({"_id": ObjectId(case_id)})

        print(f"Case: {case}")

        print(f"Finder Id: {finder_id}")

        print(f"Amount: {amount}")

        finder = await Finder.find_one(
            {"_id": PydanticObjectId(finder_id)},
            fetch_links=True,
        )

        print(f"Finder: {finder}")

        # Perform transfer

        finder_wallet = finder.wallet

        is_transfer_to_finder_successful = (
            await WalletService.send_sol(
                STAKE_WALLET_PRIVATE_KEY, finder_wallet.public_key, amount
            )
            if finder_wallet.wallet_type == "SOL"
            else await TronWallet.transfer_usdt(
                TRON_WALLET_PRIVATE_KEY, finder_wallet.public_key, amount
            )
        )
        is_tax_transfer_successful = (
            await WalletService.send_sol(
                STAKE_WALLET_PRIVATE_KEY,
                TAX_COLLECT_PUBLIC_KEY,
                float(case.reward - amount),
            )
            if finder_wallet.wallet_type == "SOL"
            else await TronWallet.transfer_usdt(
                TRON_WALLET_PRIVATE_KEY,
                TRON_TAX_COLLECT_PUBLIC_KEY,
                float(case.reward - amount),
            )
        )

        print(f"Is transfer to finder successful: {is_transfer_to_finder_successful}")
        print(f"Is tax transfer successful: {is_tax_transfer_successful}")

        finder.status = FinderStatus.COMPLETED
        case.status = CaseStatus.COMPLETED
        await case.save()

        await finder.save()

        await query.message.edit_text(
            get_text(user_id, "reward_success").format(
                amount=amount, finder_id=finder.user_id
            )
        )
        return State.END

    except Exception as e:
        logger.error(f"Reward confirmation error: {str(e)}")
        await query.message.edit_text(get_text(user_id, "error_transferring_reward"))
        return State.END


# New cancellation handler
@catch_async
async def cancel_reward(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels the reward process"""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    context.user_data.pop("reward_case_id", None)
    context.user_data.pop("reward_finder_id", None)
    context.user_data.pop("reward_amount", None)

    await query.message.edit_text(get_text(user_id, "reward_cancelled"))
    return State.END


# ---------------------------- Reward the Finder By Owner Finished ---------------------------


# -------------------------- Extend Reward By Advertiser Start ---------------------------


@catch_async
async def action_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    choice = query.data
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
        await query.edit_message_text("Choose Province")
        return State.CHOOSE_PROVINCE
    else:
        await query.edit_message_text(
            get_text(user_id, "invalid_choice"), parse_mode="HTML"
        )
        return State.END

    # ---------------------------------------- Extend Reward ---------------------------


# DEBUGGING FROM START
@catch_async
async def advertiser_wallet_type_callback(
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
        msg = get_text(user_id, "wallet_name_prompt")
        if update.message:
            await update.message.reply_text(msg, parse_mode="HTML")
        elif update.callback_query:
            await update.callback_query.message.reply_text(msg, parse_mode="HTML")

        return State.NAME_WALLET


@catch_async
async def advertiser_wallet_selection_callback(
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
            else await WalletService.get_usdt_balance(wallet_details["public_key"])
        )

        print(f"Total {wallet_type}: {total_sol}")

        context.user_data["wallet"] = wallet_details  # Store in memory
        await update_or_create_case(user_id, wallet=str(wallet_details["id"]))

        msg = get_text(user_id, "wallet_create_details").format(
            name=wallet_details["name"],
            public_key=wallet_details["public_key"],
            secret_key=wallet_details["private_key"],
            balance=total_sol,  # For USDT, balance might be different
            wallet_type=wallet_type,
        )

        transfer_instructions = get_text(user_id, "transfer_instructions").format(
            wallet_type=wallet_type,
            public_key=wallet_details["public_key"],
        )
        msg += transfer_instructions

        await query.edit_message_text(msg, parse_mode="HTML")

        # Transition to the Create Case flow
        await query.message.reply_text(get_text(user_id, "create_case_title"))
        await query.message.reply_text(get_text(user_id, "enter_name"))
        return State.CREATE_CASE_NAME
    else:
        await query.edit_message_text(
            get_text(user_id, "wallet_not_found"), parse_mode="HTML"
        )
        return State.END


@catch_async
async def advertiser_wallet_name_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    user_id = update.effective_user.id
    if update.callback_query:
        # If it's a callback query, prompt the user to enter a wallet name
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            get_text(user_id, "wallet_name_prompt"), parse_mode="HTML"
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

    wallet = await WalletService.create_wallet(user_id, wallet_type, wallet_name)
    if wallet:

        if wallet_type == "SOL":
            total_sol = await WalletService.get_sol_balance(wallet.public_key)
        elif wallet_type == "USDT":
            total_sol = await WalletService.get_usdt_balance(wallet.public_key)

        print(f"Total SOL: {total_sol}")
        print(f"This is the wallet type: {wallet_type}")

        context.user_data["wallet"] = wallet
        msg = get_text(user_id, "wallet_create_details").format(
            name=wallet.name,
            public_key=wallet.public_key,
            secret_key=wallet.private_key,
            balance=total_sol,  # For USDT, the balance logic will vary
            wallet_type=wallet_type,
        )

        transfer_instructions = get_text(user_id, "transfer_instructions").format(
            wallet_type=wallet_type,
            public_key=wallet.public_key,
        )
        msg += transfer_instructions

        await update.message.reply_text(msg, parse_mode="HTML")

        await update.message.reply_text(get_text(user_id, "create_case_title"))
        await update.message.reply_text(get_text(user_id, "enter_name"))
        return State.CREATE_CASE_NAME
    else:
        await update.message.reply_text(
            get_text(user_id, "wallet_create_err"), parse_mode="HTML"
        )
        return State.END


@catch_async
async def extend_reward_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle the Extend Reward button click."""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    case_id = query.data.removeprefix("extend_reward_")

    # Fetch the case details
    case = await Case.find_one({"_id": PydanticObjectId(case_id)}, fetch_links=True)
    print(f"I am calling the case: {case}")

    # if not case:
    #     await query.message.edit_text(get_text(user_id, "case_not_found"))
    #     return State.END

    print(f"\n\n {case_id} is the case id \n\n")

    # # Fetch the extend reward details
    extend_reward = await ExtendReward.find_one(
        {"case.$id": PydanticObjectId(case_id)},
    )

    print(f"This is the extended reward : {extend_reward}")
    # print(f"This is the extend reward: {extend_reward}")

    # if not extend_reward:
    #     await query.message.edit_text(get_text(user_id, "extend_reward_not_found"))
    #     return State.END

    # # Ensure `case.wallet` exists and is a Wallet instance
    # if not hasattr(case, "wallet") or not case.wallet:
    #     await query.message.edit_text(get_text(user_id, "no_wallet_found"))
    #     return State.END

    # wallet_type = case.wallet.wallet_type
    # print(f"Wallet Type: {wallet_type}")

    # # Get all user wallets of the given type
    # wallets = await Wallet.find(
    #     {"user_id": user_id, "wallet_type": wallet_type, "deleted": False}
    # ).to_list()

    # if not wallets:
    #     await query.message.edit_text(get_text(user_id, "no_wallet_found"))
    #     return State.END

    # # Fetch balance for each wallet
    # wallet_balances = []
    # for wallet in wallets:
    #     if wallet_type == "SOL":
    #         balance = await WalletService.get_sol_balance(wallet.public_key)
    #     else:
    #         balance = await TronWallet.get_usdt_balance(wallet.public_key)

    #     wallet_balances.append((wallet, balance))
    #     print(f"Wallet {wallet.public_key} has balance: {balance}")

    # # Select the wallet with the highest balance
    # wallet_balances.sort(key=lambda x: x[1], reverse=True)
    # best_wallet, best_balance = wallet_balances[0]

    # print(extend_reward)

    # if best_balance < extend_reward.extend_reward_amount:
    #     await query.message.edit_text(get_text(user_id, "insufficient_funds"))
    #     return State.END

    # print(f"Selected Wallet: {best_wallet.public_key} with balance {best_balance}")

    # # Show confirmation
    # keyboard = InlineKeyboardMarkup(
    #     [
    #         [
    #             InlineKeyboardButton(
    #                 get_text(user_id, "confirm"),
    #                 callback_data=f"confirm_extend_{case_id}",
    #             )
    #         ],
    #         [
    #             InlineKeyboardButton(
    #                 get_text(user_id, "cancel"), callback_data="cancel_extend"
    #             )
    #         ],
    #     ]
    # )

    # message = get_text(user_id, "extend_reward_confirmation").format(
    #     amount=extend_reward.extend_reward_amount,
    #     wallet_type=wallet_type,
    #     from_wallet=best_wallet.public_key,
    #     to_wallet=STAKE_WALLET_PUBLIC_KEY,  # Derived from private key
    # )

    # await query.message.edit_text(message, reply_markup=keyboard, parse_mode="Markdown")
    # return State.CONFIRM_EXTEND


@catch_async
async def confirm_extend_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Confirm and process the reward extension."""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    case_id = query.data.removeprefix("confirm_extend_")

    case = await Case.find_one({"_id": PydanticObjectId(case_id)}, fetch_links=True)
    extend_reward = await ExtendReward.find_one({"case.$id": PydanticObjectId(case_id)})
    if not case or not extend_reward:
        await query.message.edit_text(get_text(user_id, "case_or_extend_not_found"))
        return State.END

    wallet_type = case.wallet.wallet_type
    user_wallet = await WalletService.get_wallet_by_type(user_id, wallet_type)

    try:
        if wallet_type == "SOL":
            await WalletService.send_sol(
                user_wallet.private_key, STAKE_WALLET_PUBLIC_KEY, extend_reward.amount
            )
        else:
            await WalletService.send_usdt(
                user_wallet.private_key, STAKE_WALLET_PUBLIC_KEY, extend_reward.amount
            )
    except Exception as e:
        logger.error(f"Transfer failed: {e}")
        await query.message.edit_text(get_text(user_id, "transfer_failed"))
        return State.END

    # Update case and extend reward
    case.reward += extend_reward.amount
    await case.save()
    extend_reward.status = "completed"  # Update status
    await extend_reward.save()

    await query.message.edit_text(get_text(user_id, "extend_success"))
    return State.END


@catch_async
async def cancel_extend_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Cancel the extend reward process."""
    query = update.callback_query
    await query.answer()
    await query.message.edit_text(
        get_text(update.effective_user.id, "extend_cancelled")
    )
    return State.END
