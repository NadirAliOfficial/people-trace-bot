from beanie import PydanticObjectId
from bson import ObjectId
import datetime
import os
import requests
from models.case_model import Case, CaseStatus
from models.user_model import User
from services.case_service import get_complaints_by_country_and_province, update_or_create_case
# import telegram

from telegram.ext import (
    ContextTypes,
)

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from config.config_manager import OWNER_TELEGRAM_ID
from constant.language_constant import ITEMS_PER_PAGE
from models.case_model import Case, CaseStatus
from handlers.listing_handler import logger
from models.extend_reward_model import ExtendReward, ExtendRewardStatus
from models.finder_model import FinderStatus, RewardExtensionStatus
from models.wallet_model import Wallet
from services.case_service import get_case_by_id
from services.wallet_service import WalletService
from utils.cloudinary import CloudinaryError, upload_image, upload_video
from utils.error_wrapper import catch_async
# from utils.get_network import get_network
from utils.get_network import get_network
from utils.helper import get_username, paginate_list
from utils.province_util import get_provinces_for_country
from utils.wallet import load_user_wallet
from constants import State
from constant.language_constant import get_text, user_data_store
from services.finder_service import FinderService
from models.user_model import User


async def get_available_countries() -> list[str]:
    """Fetch distinct countries from active cases."""
    countries = await Case.distinct(
        "country",
        {"status": {"$in": [CaseStatus.ADVERTISE.value]}}
    )
    return sorted(c for c in countries if c)  # filter out None

# db/queries.py or similar
async def get_provinces_by_country(country: str) -> list[str]:
    """Fetch distinct provinces for a given country from active cases."""
    provinces = await Case.distinct(
        "province",
        {
            "country": country,
            "status": {"$in": [CaseStatus.ADVERTISE.value]},
            "province": {"$ne": None, "$ne": ""}  # avoid null/empty
        }
    )
    # Return sorted, unique list (distinct already ensures uniqueness)
    return sorted(p for p in provinces if p)


# //NOTE - This the codebase for finder country selection

@catch_async
async def finder_choose_country(update: Update, context: ContextTypes.DEFAULT_TYPE, replace: bool = False) -> int:
    """Show paginated list of countries for user to select."""
    user_id = update.effective_user.id
    page_num = 1
    context.user_data["country_page"] = page_num

    countries = await get_available_countries()
    paginated, total_pages = paginate_list(countries, page_num, ITEMS_PER_PAGE)

    kb = [[InlineKeyboardButton(c, callback_data=f"country_select_{c}")]
          for c in paginated]

    # Pagination buttons
    if total_pages > 1:
        nav_row = [
            InlineKeyboardButton(
                get_text(user_id, "next", "globals"),
                callback_data=f"country_page_{page_num+1}",
            )
        ]
        kb.append(nav_row)

    markup = InlineKeyboardMarkup(kb)

    # Decide whether to replace disclaimer OR send fresh
    if replace and update.callback_query:
        await update.callback_query.edit_message_text(
            "🌍 Please select your country to begin browsing cases:\n",
            reply_markup=markup,
            parse_mode="HTML",
        )
    elif update.message:
        await update.message.reply_text(
            "🌍 Please select your country to begin browsing cases:\n",
            reply_markup=markup,
            parse_mode="HTML",
        )
    else:
        await update.callback_query.message.reply_text(
            "🌍 Please select your country to begin browsing cases:\n",
            reply_markup=markup,
            parse_mode="HTML",
        )

    return State.FINDER.CHOOSE_COUNTRY


@catch_async
async def finder_country_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle country selection or pagination."""
    print("DEBUG: finder_country_callback_inside")
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id

    print("Country ", data)

    if data.startswith("country_select_"):
        country = data.replace("country_select_", "")
        context.user_data["finder_country"] = country
        await FinderService.update_or_create_finder(user_id, country=country)

        await query.edit_message_text(
            f"✅ {get_text(user_id, 'country_selected', 'start-complaints')} {country}\n\n"
            f"🌍 {get_text(user_id, 'enter_province', 'start-complaints')}",
            parse_mode="HTML",
        )

        return State.FINDER.CHOOSE_PROVINCE

    elif data.startswith("country_page_"):
        try:
            page_num = int(data.replace("country_page_", ""))
        except ValueError:
            page_num = 1

        context.user_data["country_page"] = page_num
        countries = await get_available_countries()

        paginated, total_pages = paginate_list(countries, page_num, ITEMS_PER_PAGE)

        kb = [[InlineKeyboardButton(c, callback_data=f"country_select_{c}")]
              for c in paginated]

        nav_row = []
        if page_num > 1:
            nav_row.append(
                InlineKeyboardButton(get_text(user_id, "prev", "globals"),
                                     callback_data=f"country_page_{page_num-1}")
            )
        if page_num < total_pages:
            nav_row.append(
                InlineKeyboardButton(get_text(user_id, "next", "globals"),
                                     callback_data=f"country_page_{page_num+1}")
            )
        if nav_row:
            kb.append(nav_row)

        await query.edit_message_text(
            "🌍 Please select your country to begin browsing cases:\n",
            reply_markup=InlineKeyboardMarkup(kb),
            parse_mode="HTML",
        )

        return State.FINDER.CHOOSE_COUNTRY

    else:
        await query.edit_message_text(
            get_text(user_id, "invalid_choice", "globals"), parse_mode="HTML"
        )
        return State.FINDER.END


#  //NOTE - This the codebase for finder state/province selection
async def finder_choose_province(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handles province selection: show list of valid provinces for the country."""
    user_id = update.effective_user.id
    txt = update.message.text.strip()

    # Get country from user_data
    country = context.user_data.get("finder_country")
    if not country:
        await update.message.reply_text(
            get_text(user_id, "country_not_found", "start-complaints"),
            parse_mode="HTML",
        )
        return State.FINDER.CHOOSE_PROVINCE

    # Fetch actual provinces from DB for this country
    provinces = await get_provinces_by_country(country)

    if not provinces:
        await update.message.reply_text(
            get_text(user_id, "no_provinces_available", "start-complaints"),
            parse_mode="HTML",
        )
        return State.FINDER.CHOOSE_PROVINCE

    # Check if user input matches any province
    matched = [p for p in provinces if txt.lower() in p.lower()]

    if len(matched) == 1:
        province = matched[0]
        context.user_data["finder_province"] = province
        await FinderService.update_or_create_finder(user_id, province=province)

        await update.message.reply_text(
            f"{get_text(user_id, 'selected', 'globals')} {province}.",
            parse_mode="HTML",
        )
        complaints = await get_complaints_by_country_and_province(
            country, province, user_id
        )

        if not complaints:
            await update.message.reply_text(f"❌ No cases found in {province}, {country}.")
            return State.FINDER.END

        context.user_data["finder_complaints"] = complaints
        context.user_data["complaint_index"] = 0  # Add this line to initialize the index
        await show_complaint(user_id, update, context)
        return State.FINDER.VIEW_COMPLAINTS

    elif len(matched) == 0:
        # Show full list instead of saying "not found"
        context.user_data["province_matches"] = provinces
        context.user_data["province_page"] = 1

        paginated, total_pages = paginate_list(provinces, 1, ITEMS_PER_PAGE)

        kb = [
            [InlineKeyboardButton(p, callback_data=f"province_select_{p}")]
            for p in paginated
        ]

        nav_row = []
        if total_pages > 1:
            if 1 < total_pages:
                nav_row.append(
                    InlineKeyboardButton(
                        get_text(user_id, "next", "globals"),
                        callback_data="province_page_2",
                    )
                )
            kb.append(nav_row)

        markup = InlineKeyboardMarkup(kb)
        await update.message.reply_text(
            get_text(user_id, "province_list", "start-complaints").format(
                country=country, page=1, total=total_pages
            ),
            reply_markup=markup,
            parse_mode="HTML",
        )
        return State.FINDER.CHOOSE_PROVINCE

    else:
        # Multiple matches — show them
        context.user_data["province_matches"] = matched
        context.user_data["province_page"] = 1

        paginated, total_pages = paginate_list(matched, 1, ITEMS_PER_PAGE)

        kb = [
            [InlineKeyboardButton(p, callback_data=f"province_select_{p}")]
            for p in paginated
        ]

        if total_pages > 1:
            kb.append([
                InlineKeyboardButton(
                    get_text(user_id, "next", "globals"),
                    callback_data="province_page_2",
                )
            ])

        markup = InlineKeyboardMarkup(kb)
        await update.message.reply_text(
            get_text(user_id, "province_multi", "start-complaints").format(
                page=1, total=total_pages
            ),
            reply_markup=markup,
            parse_mode="HTML",
        )
        return State.FINDER.CHOOSE_PROVINCE


async def finder_province_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = update.effective_user.id

    if data.startswith("province_select_"):
        province = data.replace("province_select_", "")
        context.user_data["finder_province"] = province
        await FinderService.update_or_create_finder(user_id, province=province)

        # Fetch complaints for selected country + province
        country = context.user_data.get("finder_country")
        complaints = await get_complaints_by_country_and_province(
            country, province, user_id
        )

        if not complaints:
            await query.edit_message_text(f"❌ No cases found in {province}, {country}.")
            return State.FINDER.END

        context.user_data["finder_complaints"] = complaints
        context.user_data["complaint_index"] = 0  # Add this line to initialize the index
        await show_complaint(user_id, update, context)
        return State.FINDER.VIEW_COMPLAINTS

    elif data.startswith("province_page_"):
        try:
            page_num = max(1, int(data.replace("province_page_", "")))
        except ValueError:
            page_num = 1

        matches = context.user_data.get("province_matches", [])
        paginated, total = paginate_list(matches, page_num)

        kb = [
            [InlineKeyboardButton(p, callback_data=f"province_select_{p}")]
            for p in paginated
        ]

        nav_row = []
        if page_num > 1:
            nav_row.append(
                InlineKeyboardButton(
                    get_text(user_id, "prev", "globals"),
                    callback_data=f"province_page_{page_num - 1}",
                )
            )
        if page_num < total:
            nav_row.append(
                InlineKeyboardButton(
                    get_text(user_id, "next", "globals"),
                    callback_data=f"province_page_{page_num + 1}",
                )
            )
        if nav_row:
            kb.append(nav_row)

        markup = InlineKeyboardMarkup(kb)
        await query.edit_message_text(
            get_text(user_id, "province_multi", "start-complaints").format(
                page=page_num, total=total
            ),
            reply_markup=markup,
            parse_mode="HTML",
        )

        context.user_data["province_page"] = page_num
        return State.FINDER.CHOOSE_PROVINCE

    else:
        await query.edit_message_text(
            get_text(user_id, "invalid_choice", "globals"), parse_mode="HTML"
        )
        return State.FINDER.END


async def show_complaint(user_id, update, context):
    complaints = context.user_data["finder_complaints"]
    index = context.user_data["complaint_index"]
    total = len(complaints)
    c = complaints[index]

    chat = await context.bot.get_chat(c.user_id)


    text = (
        f"🔍 Case {index+1}/{total}\n"
        f"👤 Name: {c.person_name}\n"
        f"📍 Last Seen: {c.last_seen_location}\n"
        f"📅 Date: {c.created_at.strftime('%d %B %Y')}\n"
        f"🎂 Age: {c.age}\n"
        f"💰 Reward: {c.reward} USDT\n"
        f"🧾 Posted by: @{get_username(chat)}"
    )

    # ✅ Build buttons dynamically
    kb = [
        [InlineKeyboardButton("🧩 I Have a Lead", callback_data=f"lead_{index}")]
    ]

    nav_row = []
    if index > 0:  # Show Back only if not first
        nav_row.append(
            InlineKeyboardButton("◀️ Back", callback_data=f"complaint_back_{index}")
        )
    if index < total - 1:  # Show Next only if not last
        nav_row.append(
            InlineKeyboardButton("▶️ Next", callback_data=f"complaint_next_{index}")
        )
    if nav_row:
        kb.append(nav_row)

    kb.append(
        [InlineKeyboardButton("📬 Request Higher Reward", callback_data=f"reward_{index}")]
    )

    message = update.message or update.callback_query.message

    if c.case_photo:
        await message.reply_photo(
            c.case_photo,
            caption=text,
            reply_markup=InlineKeyboardMarkup(kb),
            parse_mode="HTML",
        )
    else:
        await message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(kb),
            parse_mode="HTML",
        )


@catch_async
async def finder_complaint_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    data = query.data
    index = context.user_data.get("complaint_index", 0)
    complaints = context.user_data.get("finder_complaints", [])
    total = len(complaints)

    if data.startswith("complaint_next_") and index + 1 < total:
        context.user_data["complaint_index"] += 1

    elif data.startswith("complaint_back_") and index > 0:
        context.user_data["complaint_index"] -= 1

    elif data.startswith("lead_"):
        # Extract index from callback_data
        selected_index = int(data.split("_")[1])
        selected_complaint = complaints[selected_index]

        # Store selected complaint in user_data
        context.user_data["selected_complaint"] = selected_complaint

        # Continue lead flow
        if query.message.photo:
            await query.edit_message_caption(get_text(user_id, "proof_upload", "finder"))
        else:
            await query.edit_message_text(get_text(user_id, "proof_upload", "finder"))

        return State.UPLOAD_PROOF

    elif data.startswith("reward_"):
        selected_index = int(data.split("_")[1])
        selected_complaint = complaints[selected_index]
        context.user_data["selected_complaint"] = selected_complaint
        wallet_type = selected_complaint.wallet.wallet_type

        new_text = (
            f"The current reward amount is <b>{selected_complaint.reward} {wallet_type}</b>.\n"
            f"Please enter the new reward amount you want to set:"
        )

        if query.message.photo:
            await query.edit_message_caption(new_text, parse_mode="HTML")
        else:
            await query.edit_message_text(new_text, parse_mode="HTML")

        return State.EXTEND_REWARD_AMOUNT

    else:
        return State.FINDER.END

    await query.message.delete()
    await show_complaint(query.from_user.id, update, context)
    return State.FINDER.VIEW_COMPLAINTS


@catch_async
async def handle_proof(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles uploaded proof (image or video) and uploads it to Cloudinary."""
    print("handle_proof")
    user_id = update.effective_user.id
    selected_case = context.user_data.get("selected_complaint")
    # Ensure 'proofs' directory exists
    os.makedirs("proofs", exist_ok=True)
    file_id = None
    file_extension = None
    file_size = None
    is_video = False  # Flag to check if the file is a video
    # Check for photo or video
    if update.message.photo:
        file_id = update.message.photo[-1].file_id
        file_extension = "jpg"  # Telegram sends images in JPG format
    elif update.message.video:
        file_id = update.message.video.file_id
        file_extension = update.message.video.mime_type.split("/")[
            1
        ]  
        # Get video format (e.g., mp4, mov, etc.)
        file_size = update.message.video.file_size  # File size in bytes
        is_video = True  # Mark this as a video upload
    else:
        await update.message.reply_text(get_text(user_id, "error_upload_proof" , "finder"))
        return State.UPLOAD_PROOF
    # Define supported formats for both images and videos
    supported_image_formats = ["jpg", "jpeg", "png"]
    supported_video_formats = ["mp4", "mov", "avi", "mkv", "webm"]
    # Validate the file format
    if is_video:
        if file_extension not in supported_video_formats:
            await update.message.reply_text(
                "Unsupported video format. Please upload a valid video (mp4, mov, avi, mkv, webm)."
            )
            return State.UPLOAD_PROOF
        # Check video file size (5MB max)
        if file_size and file_size > 5 * 1024 * 1024:
            await update.message.reply_text(
                "The file is too large. Please upload a video smaller than 5 MB."
            )
            return State.UPLOAD_PROOF
    else:
        if file_extension not in supported_image_formats:
            await update.message.reply_text(
                "Unsupported image format. Please upload a valid image (jpg, jpeg, png)."
            )
            return State.UPLOAD_PROOF
    # Generate unique filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"proof_{user_id}_{selected_case.case_no}_{timestamp}.{file_extension}"
    file_path = os.path.join("proofs", filename)
    # Download file
    file = await context.bot.get_file(file_id)
    await file.download_to_drive(file_path)
    # Upload to Cloudinary
    try:
        if is_video:
            upload_result = await upload_video(file_path)
        else:
            upload_result = await upload_image(file_path)
        print(f"Uploaded File URL: {upload_result}")
    except CloudinaryError as e:
        print(f"Cloudinary upload error: {e}")
        await update.message.reply_text(
            "There was an error uploading the file. Please try again."
        )
        return State.END
    await FinderService.update_or_create_finder(user_id, proof_url=[upload_result])
    # Store proof path in context
    context.user_data["proof_path"] = file_path
    await update.message.reply_text(get_text(user_id, "proof_received",  "finder"))
    return State.ENTER_LOCATION


@catch_async
async def handle_enter_location(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Notify the advertiser and ask them to confirm the reward transfer."""
    user_id = update.effective_user.id
    location = update.message.text.strip()
    context.user_data["finder_location"] = location

    await FinderService.update_or_create_finder(user_id, reported_location=location)
    await update.message.reply_text(
        "Do you want to extend the reward?",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Yes", callback_data="yes_extend"),
                    InlineKeyboardButton("No", callback_data="no_extend"),
                ],
            ]
        ),
    )
    return State.EXTEND_REWARD


# -----------------------------------------------------------------------------------------------------------

def get_province_matches(query, country):
    """Geting the province match with query and inside the country which provided"""
    query = query.lower()
    provinces = get_provinces_for_country(country)
    return [province for province in provinces if query in province.lower()]


async def fetch_cases_by_province(location):
    """
    Fetch cases from the database based on the province.
    """
    # Implement this function
    case = await Case.find(
        {"province": location, "status": CaseStatus.ADVERTISE}
    ).to_list()
    print(f"These are the cases for {location}: {case}")

    return case


async def fetch_case_by_number(case_no):
    """
    Fetch a case from the database based on the case number.
    """
    # Implement this function
    case = await Case.find_one({"_id": ObjectId(case_no)})
    return case

@catch_async
async def choose_province(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Let user pick a province only from existing complaints in DB."""
    print("Hello from choose_province")
    user_id = update.effective_user.id
    txt = update.message.text.strip()

    # Get selected country
    country = context.user_data.get("country")
    if not country:
        await update.message.reply_text(
            get_text(user_id, "country_not_found", "start-complaints"), parse_mode="HTML"
        )
        return State.FINDER.CHOOSE_COUNTRY

    # Fetch distinct provinces from DB for this country
    provinces = await Case.find(
        {"country": country, "status": CaseStatus.ADVERTISE}
    ).distinct("province")

    provinces = [p for p in provinces if p]  # remove None
    print(f"Available provinces for {country}: {provinces}")

    # If user typed a province, filter it
    matches = [p for p in provinces if txt.lower() in p.lower()]

    if len(matches) == 1:
        selected_province = matches[0]

        # Update finder info
        await FinderService.update_or_create_finder(
            user_id=user_id,
            province=selected_province,
            country=country,
        )
        context.user_data["province"] = selected_province

        # Fetch cases in this province
        cases = await Case.find(
            {"country": country, "province": selected_province, "status": CaseStatus.ADVERTISE}
        ).to_list()

        if not cases:
            await update.message.reply_text(
                get_text(user_id, "no_case_found_in_province", "start-complaints").format(
                    province=selected_province
                ),
                parse_mode="Markdown",
            )
            return State.FINDER.CHOOSE_PROVINCE

        # Save cases for pagination
        context.user_data["cases"] = cases
        context.user_data["page"] = 1

        paginated_cases, total_pages = paginate_list(cases, 1)

        keyboard = [
            [
                InlineKeyboardButton(
                    f"Case {case.case_no} - {case.person_name}",
                    callback_data=f"case_{str(case.id)}",
                )
            ]
            for case in paginated_cases
        ]

        # Pagination buttons
        nav = []
        if total_pages > 1:
            nav.append(InlineKeyboardButton("⬅️ Previous", callback_data="case_page_previous"))
            nav.append(InlineKeyboardButton("➡️ Next", callback_data="case_page_next"))
        if nav:
            keyboard.append(nav)

        await update.message.reply_text(
            f"📍 Cases from *{selected_province}*: ",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )
        return State.FINDER.CASE_DETAILS

    elif len(matches) == 0:
        # Show all provinces list (first page)
        page = 1
        paginated, total_pages = paginate_list(provinces, page)

        kb = [[InlineKeyboardButton(p, callback_data=f"province_select_{p}")] for p in paginated]

        if total_pages > 1:
            kb.append(
                [
                    InlineKeyboardButton("⬅️", callback_data=f"province_page_{page-1}"),
                    InlineKeyboardButton("➡️", callback_data=f"province_page_{page+1}"),
                ]
            )

        await update.message.reply_text(
            f"📍 Please select your province (page {page}/{total_pages}):",
            reply_markup=InlineKeyboardMarkup(kb),
            parse_mode="HTML",
        )
        return State.FINDER.CHOOSE_PROVINCE


# Function to handle the province selection callback
async def province_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = update.effective_user.id

    if data.startswith("province_select_"):
        province = data.replace("province_select_", "")
        context.user_data["province"] = province  # Save province in context
        await query.edit_message_text(
            f"{get_text(user_id, 'province_selected', "finder")} {province}.",
            parse_mode="HTML",
        )
        # Proceed to the next step (case listing or whatever is next)

        return await show_advertisements(update, context)

    elif data.startswith("province_page_"):
        # Handle pagination for provinces
        page_str = data.replace("province_page_", "")
        try:
            page_num = int(page_str)
            if page_num < 1:
                page_num = 1
        except ValueError:
            page_num = 1

        matches = user_data_store[user_id].get("province_matches", [])
        paginated, total = paginate_list(matches, page_num)
        kb = []
        for p in paginated:
            kb.append([InlineKeyboardButton(p, callback_data=f"province_select_{p}")])

        nav_row = []
        if page_num > 1:
            nav_row.append(
                InlineKeyboardButton("⬅️", callback_data=f"province_page_{page_num-1}")
            )
        if page_num < total:
            nav_row.append(
                InlineKeyboardButton("➡️", callback_data=f"province_page_{page_num+1}")
            )
        if nav_row:
            kb.append(nav_row)

        markup = InlineKeyboardMarkup(kb)
        await query.edit_message_text(
            get_text(user_id, "province_multi", "start-complaints").format(page=page_num, total=total),
            reply_markup=markup,
            parse_mode="HTML",
        )

        user_data_store[user_id]["province_page"] = page_num
        return State.CHOOSE_PROVINCE

    else:
        await query.edit_message_text(
            get_text(user_id, "invalid_choice"), parse_mode="HTML"
        )
        return State.END


        # TODO: Why it has the seperate pagination function - Need to be fixe.


async def show_advertisements(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Show listings of advertisements with pagination"""
    print("\033show_advertisements\033[0m")
    query = update.callback_query
    user_id = update.effective_user.id

    await query.answer() if query else None

    province = context.user_data.get("province")
    if not province:
        await update.effective_message.reply_text(get_text(user_id, "select_province", "finder"))
        return State.CHOOSE_PROVINCE

    try:
        # Get current page from context
        page = context.user_data.get("page", 1)  # Default to page 1
        items_per_page = ITEMS_PER_PAGE

        # Fetch cases from database
        all_cases = await fetch_cases_by_province(province)
        total_cases = len(all_cases)

        if not all_cases:
            await update.effective_message.reply_text(
                get_text(user_id, "case_not_found_in_province", "finder")
            )
            return State.END

        # Pagination calculations
        total_pages = (total_cases + items_per_page - 1) // items_per_page
        start_idx = (page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        cases = all_cases[start_idx:end_idx]

        # Create case buttons
        keyboard = []
        for case in cases:
            case_info = f"{case.name} ({case.person_name})"

            keyboard.append(
                [InlineKeyboardButton(case_info, callback_data=f"case_{case.id}")]
            )

        # Add pagination controls
        pagination_buttons = []
        if page > 1:
            pagination_buttons.append(
                InlineKeyboardButton(
                    "⬅️ Previous", callback_data=f"case_page_{page - 1}"
                )
            )
        if page < total_pages:
            pagination_buttons.append(
                InlineKeyboardButton("Next ➡️", callback_data=f"case_page_{page + 1}")
            )

        if pagination_buttons:
            keyboard.append(pagination_buttons)

        reply_markup = InlineKeyboardMarkup(keyboard)
        text = f"Cases in {province} (Page {page} of {total_pages}):"

        if query:
            await query.edit_message_text(text, reply_markup=reply_markup)
        else:
            await update.effective_message.reply_text(text, reply_markup=reply_markup)

        return State.CASE_DETAILS

    except Exception as e:
        logger.error(f"Error showing advertisements: {e}")
        await update.effective_message.reply_text(
            get_text(user_id, "error_loading_cases") # !SECTION ->  Skipped  
        )
        return State.END


async def handle_pagination(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle pagination for case listings."""
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id

    # Extract page number from callback data
    if query.data.startswith("case_page_"):
        page_str = query.data.replace("case_page_", "")
        try:
            page = int(page_str)
            if page < 1:
                page = 1
        except ValueError:
            page = 1

        # Save updated page in context
        context.user_data["page"] = page

        # Re-fetch and display cases for the updated page
        return await show_advertisements(update, context)

    return State.CASE_DETAILS


async def case_details(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show detailed information about a case"""
    print("case_details_callback")
    query = update.callback_query
    user_id = update.effective_user.id
    await query.answer()

    try:
        print(f"Printing the Query: {query.data}")
        case_id = query.data.split("_")[1]
        print(f"Case ID: {case_id}")
        await FinderService.update_or_create_finder(user_id, case=case_id)
        case = await fetch_case_by_number(case_id)

        if not case:
            await query.edit_message_text(get_text(user_id, "case_not_found", "start-complaints"))
            return State.END

        wallet = await case.wallet.fetch() if case.wallet else None

        proof_text = (
            f"[Proof]({case.case_photo})"
            if case.case_photo and case.case_photo.startswith("http")
            else "No proof available"
        )

        details = (
            f"📌 **Case Details**\n"
            f"👤 **Person Name:** {case.person_name}\n"
            f"📍 **Last Seen Location:** {case.last_seen_location}\n"
            f"💰 **Reward:** {case.reward or 'None'} \n"
            f"👤 **Gender:** {case.gender}\n"
            f"🧒 **Age:** {case.age}\n"
            f"📏 **Height:** {case.height} cm\n"
        )

        details += f"\n\n**Proof:** {proof_text}"

        keyboard = [
            [
                InlineKeyboardButton(
                    get_text(user_id, "mark_as_found", "finder"),
                    callback_data=f"found_{case.id}",
                )
            ],
            [
                InlineKeyboardButton(
                    get_text(user_id, "back_to_list", "finder"), callback_data="back_to_list"
                )
            ],
        ]

        # Send case details
        await query.message.reply_text(
            details, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown"
        )

        return State.CASE_DETAILS

    except Exception as e:
        logger.error(f"Error showing case details: {e}")
        await query.edit_message_text(get_text(user_id, "error_loading_case", "finder"))
        return State.END


# ------------------------------------- FINDER  LOGIC  START ------------------------------------


@catch_async
async def finder_wallet_type_callback(
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
                    get_text(user_id, "create_wallet", "globals"),
                    callback_data="create_new_wallet",
                )
            ]
        )
        await query.edit_message_text(
            get_text(user_id, "choose_existing_or_new_wallet", "start-mobile"),
            reply_markup=InlineKeyboardMarkup(kb),
            parse_mode="HTML",
        )
        return State.FINDER_CHOOSE_WALLET_TYPE
    else:
        msg = get_text(user_id, "wallet_name_prompt", "start-mobile")
        if update.message:
            await update.message.reply_text(msg, parse_mode="HTML")
        elif update.callback_query:
            await update.callback_query.message.reply_text(msg, parse_mode="HTML")

        return State.FINDER_NAME_WALLET


@catch_async
async def finder_wallet_selection_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:

    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    # Extract wallet name and type from callback data
    wallet_id = query.data.replace("wallet_", "")
    wallet_type = context.user_data.get("wallet_type")  # 'sol' or 'usdt'

    case_id = context.user_data.get("found_case_no")
    case = await Case.find_one({"_id": PydanticObjectId(case_id)}, fetch_links=True)

    # Fetch wallet details by name and type
    wallet_details = await WalletService.get_wallet_by_id(wallet_id)

    print(f"Wallet details: {wallet_details}")

    if wallet_details:
        # Fetch balance for the specific wallet type (SOL or USDT)
        print(f"This is the wallet type: {wallet_type}")

        print("\n\n DEBUGGING -001 \n\n")
        total_sol = (
            await WalletService.get_sol_balance(wallet_details["public_key"])
            if wallet_type == "SOL"
            else await WalletService.get_usdt_balance(wallet_details["public_key"])
        )

        print(f"Total {wallet_type}: {total_sol}")

        context.user_data["wallet"] = wallet_details  # Store in memory
        await FinderService.update_or_create_finder(
            user_id, wallet=str(wallet_details["id"])
        )

        print("\n\n DEBUGGING -002 \n\n")

        msg = get_text(user_id, "wallet_create_details_with_balance", "cases").format(
            name=wallet_details["name"],
            public_key=wallet_details["public_key"],
            type=wallet_details["wallet_type"],
            network=get_network(wallet_details["wallet_type"]),
            balance=total_sol,  # For USDT, balance might be different
            wallet_type=wallet_type,
        )

        # Send wallet details as a new message
        await query.message.reply_text(msg, parse_mode="HTML")

        # Send confirmation as a new message
        confirmation_message = (
            f"❗ <b>Reward Confirmation</b> ❗\n\n"
            f"Do you want to <b>request the reward</b> of <b>{case.reward} {wallet_details['wallet_type']}</b> to the wallet below?\n\n"
            f"🔐 <b>Wallet Address:</b>\n<code>{wallet_details['public_key']}</code>\n\n"
            f"By confirming, your request will be sent to the administrator for manual processing."
        )

        keyboard = [
            [
                InlineKeyboardButton("📨 Send Request", callback_data="confirm_transfer"),
                InlineKeyboardButton("❌ Cancel", callback_data="cancel_transfer"),
            ]
        ]

        await query.message.reply_text(
            confirmation_message,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML",
        )

        return State.FINDER_CONFIRM_TRANSACTION

    else:
        await query.message.reply_text(
            get_text(user_id, "wallet_not_found", "settings"), parse_mode="HTML"
        )

@catch_async
async def finder_wallet_type_callback(
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
                    get_text(user_id, "create_wallet", "globals"),
                    callback_data="create_new_wallet",
                )
            ]
        )
        await query.edit_message_text(
            get_text(user_id, "choose_existing_or_new_wallet", "start-mobile"),
            reply_markup=InlineKeyboardMarkup(kb),
            parse_mode="HTML",
        )
        return State.FINDER_CHOOSE_WALLET_TYPE
    else:
        msg = get_text(user_id, "wallet_name_prompt", "start-mobile")
        if update.message:
            await update.message.reply_text(msg, parse_mode="HTML")
        elif update.callback_query:
            await update.callback_query.message.reply_text(msg, parse_mode="HTML")

        return State.FINDER_NAME_WALLET


@catch_async
async def finder_wallet_selection_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:

    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    # Extract wallet name and type from callback data
    wallet_id = query.data.replace("wallet_", "")
    case = context.user_data.get("selected_complaint")
    wallet_type = case.wallet.wallet_type  # 'sol' or 'usdt'

    # Fetch wallet details by name and type
    wallet_details = await WalletService.get_wallet_by_id(wallet_id)

    print(f"Wallet details: {wallet_details}")

    if wallet_details:
        # Fetch balance for the specific wallet type (SOL or USDT)
        print(f"This is the wallet type: {wallet_type}")

        print("\n\n DEBUGGING -001 \n\n")
        total_sol = (
            await WalletService.get_sol_balance(wallet_details["public_key"])
            if wallet_type == "SOL"
            else await WalletService.get_usdt_balance(wallet_details["public_key"])
        )

        print(f"Total {wallet_type}: {total_sol}")

        context.user_data["wallet"] = wallet_details  # Store in memory

        await FinderService.update_or_create_finder(
            user_id, wallet=str(wallet_details["id"])
        )

        print("\n\n DEBUGGING -002 \n\n")

        # Show wallet details
        msg = get_text(user_id, "wallet_create_details_with_balance", "cases").format(
            name=wallet_details["name"],
            public_key=wallet_details["public_key"],
            balance=total_sol,
            wallet_type=wallet_type,
            network=get_network(wallet_type),
        )

        await query.message.reply_text(msg, parse_mode="HTML")

        # Basic reward info
        reward_text = f"<b>{case.reward} {wallet_details['wallet_type']}</b>"

        # Handle extended reward details
        extended_note = ""
        if context.user_data.get("extend_flow", False):
            extended_note = (
                f"\n➕ <b>Extended Reward:</b> <b>{context.user_data['reward_difference'] or 0} {wallet_details['wallet_type']}</b>"
                "\n🔄 <i>Note:</i> The extended reward will be processed separately and transferred after admin approval."
            )

        # Full confirmation message
        confirmation_message = (
            f"❗ <b>Reward Confirmation</b> ❗\n\n"
            f"Do you want to <b>request the reward</b> of {reward_text} to the wallet below?\n\n"
            f"🔐 <b>Wallet Address:</b>\n<code>{wallet_details['public_key']}</code>"
            f"{extended_note}\n\n"
            f"By confirming, your request will be sent to the administrator for manual processing."
        )

        # Inline keyboard
        keyboard = [
            [
                InlineKeyboardButton("📨 Send Request", callback_data="confirm_transfer"),
                InlineKeyboardButton("❌ Cancel", callback_data="cancel_transfer"),
            ]
        ]

        await query.message.reply_text(
            confirmation_message,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML",
        )

        return State.FINDER_CONFIRM_TRANSACTION

    else:
        await query.message.reply_text(
            get_text(user_id, "wallet_not_found", "wallets"), parse_mode="HTML" 
        )
        return State.END

@catch_async
async def finder_wallet_name_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    user_id = update.effective_user.id

    if update.callback_query:
        query = update.callback_query
        await query.answer()

        # Prompt the user to enter a wallet name
        await query.edit_message_text(
            get_text(user_id, "wallet_name_prompt", "settings"), parse_mode="HTML"
        )
        return State.NAME_WALLET

    # If not a callback query, assume it's a message with the wallet name
    if update.message and update.message.text:
        wallet_name = update.message.text.strip()
    else:
        await update.message.reply_text(
            get_text(user_id, "wallet_name_empty", "settings"), parse_mode="HTML"
        )
        return State.FINDER_NAME_WALLET

    case_id = context.user_data.get("found_case_no")
    case = await get_case_by_id(case_id)

    print(f"Wallet name: {wallet_name}")

    if not wallet_name:
        await update.message.reply_text(
            get_text(user_id, "wallet_name_empty", "settings"), parse_mode="HTML"
        )
        return State.FINDER_NAME_WALLET

    wallet_type = context.user_data.get("wallet_type")
    wallet = await WalletService.create_wallet(user_id, wallet_type, wallet_name)

    if wallet:
        if wallet_type == "SOL":
            total_sol = await WalletService.get_sol_balance(wallet.public_key)
        elif wallet_type == "USDT":
            total_sol = await WalletService.get_usdt_balance(wallet.public_key)

        print(f"Total SOL: {total_sol}")
        print(f"This is the wallet type: {wallet_type}")

        context.user_data["wallet"] = wallet

        keyboard = [
            [
                InlineKeyboardButton(
                    "Confirm Transfer", callback_data="confirm_transfer"
                ),
                InlineKeyboardButton("Cancel", callback_data="cancel_transfer"),
            ]
        ]

        print(
            f"Confirm transfer of {case.reward} {wallet.wallet_type} from {wallet.name}?\n"
            f"Wallet address: {wallet.public_key}"
        )

        await update.message.reply_text(
            f"Confirm transfer of {case.reward} {wallet.wallet_type} from {wallet.name}?\n"
            f"Wallet address: {wallet.public_key}",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return State.FINDER_CONFIRM_TRANSACTION

    else:
        await update.message.reply_text(
            get_text(user_id, "wallet_create_err", "settings"), parse_mode="HTML"
        )
        return State.END

@catch_async
async def finder_handle_transaction_confirmation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    print(f"Inside the finder handler confirmation ")
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    case = context.user_data.get("selected_complaint")
    isExtendedFlow = context.user_data.get("extend_flow", False)
    print("Case: ", case)
    wallet = case.wallet
    print(f"Wallet: {wallet}")
    print(f"Case: {case}")

    if case.status == CaseStatus.ADVERTISE:
        if isExtendedFlow:
            extend_reward = ExtendReward(
                user_id=user_id,
                case=case,
                status=ExtendRewardStatus.PENDING,
                extend_reward_amount=context.user_data["reward_difference"],
                reason="Just for the testing Purpose.",
            )
            await extend_reward.save()

        finder = await FinderService.update_or_create_finder(
            user_id,
            case=case.id,
            status=FinderStatus.FIND,
        )

        # Message to the OWNER (Advertiser)
        await context.bot.send_message(
            chat_id=case.user_id,
            text=(
                "📢 <b>Finder Request Submitted!</b> 📢\n\n"
                f"🔎 <b>User ID:</b> <code>{finder.user_id}</code>\n"
                f"📂 <b>Case:</b> Finder has submitted a request for your advertisement (Case ID: <code>#{case.id}</code>)\n"
                f"📞 <b>Finder's Contact Number:</b> <code>{'----'}</code>\n\n"
                "🔔 Please review the details and confirm the reward if everything is accurate.\n"
                "💰 Once confirmed, proceed with the payment.\n\n"
                "📝 Type <b>/listing</b> to view all complaints."
            ),
            parse_mode="HTML"
        )

        # Message to the FINDER (Confirmation)
        await query.edit_message_text(
            "🎯 <b>Request Submitted Successfully!</b> 🎯\n\n"
            "Your finder request has been sent to the advertiser. 🚀\n"
            "They will review the details and you will receive your reward once approved.\n\n"
            "💬 Type <b>/listing</b> to view all cases.",
            parse_mode="HTML"
        )

        # Message to the MODERATOR/ADMIN
        await context.bot.send_message(
            chat_id=OWNER_TELEGRAM_ID,
            text=(
                "🛑 <b>Attention Required!</b> 🛑\n\n"
                "🚨 A new <b>'Finder'</b> request has been submitted.\n"
                f"📂 <b>Case ID:</b> <code>#{case.id}</code>\n"
                f"👤 <b>Finder User ID:</b> <code>{finder.user_id}</code>\n"
                f"📞 <b>Finder's Contact Number:</b> <code>{'----'}</code>\n\n"
                "🔍 Please review the case and assist in the verification process if needed.\n"
                "📝 Type <b>/listing</b> to view all active complaints."
            ),
            parse_mode="HTML"
        )

        return State.END


# ------------------------------- FINDER LOGIC END ------------------------------------

#  ---------------------------- Extend Reward ---------------------------


async def handle_advertiser_response(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "reject_extend":
        await query.edit_message_text("Extension request rejected")
        return State.END

    # Get case details from context
    case_id = context.user_data.get("found_case_no")
    case = await Case.find_one({"_id": PydanticObjectId(case_id)}, fetch_links=True)

    # Get advertiser's wallets
    wallets = (
        await WalletService.get_sol_wallet_of_user(case.user_id)
        if case.wallet.wallet_type == "SOL"
        else await WalletService.get_usdt_wallet_of_user(case.user_id)
    )

    print(f"Wallets: {wallets}")

    if not wallets:
        # No wallets found, prompt to create one
        keyboard = [
            [
                InlineKeyboardButton(
                    "Create New Wallet", callback_data="create_extend_wallet"
                )
            ]
        ]
        await query.edit_message_text(
            "No wallets found. Please create a wallet to proceed:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return State.SELECT_WALLET

    # Show existing wallets
    keyboard = []
    for wallet in wallets:
        print(f"Wallet: {wallet}")
        keyboard.append(
            [
                InlineKeyboardButton(
                    f"{wallet.name}",
                    callback_data=f"select_extend_wallet_{wallet.id}",
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                "Create New Wallet", callback_data="create_extend_wallet"
            )
        ]
    )

    await query.edit_message_text(
        "Select a wallet to use for the transfer:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return State.SELECT_WALLET


@catch_async
async def handle_transfer_confirmation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == "cancel_transfer":
        await query.edit_message_text("Transfer cancelled")
        return State.END

    wallet = context.user_data["selected_wallet"]
    amount = context.user_data["reward_difference"]
    case_id = context.user_data.get("found_case_no")
    case = await get_case_by_id(PydanticObjectId(case_id))

    # Notify both parties
    await context.bot.send_message(
        chat_id=case.user_id,
        text=f"Successfully transferred {amount} {wallet.wallet_type}!\n"
        f"New total reward: {case.reward} {wallet.wallet_type}",
    )
    await context.bot.send_message(
        chat_id=context.user_data["finder_id"],  # Store finder ID earlier
        text=f"Reward extended to {case.reward} {wallet.wallet_type}!\n"
        f"The additional amount has been secured.",
    )
    await query.edit_message_text("Transfer successful! Reward updated.")

async def handle_confirm_found(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id

    if query.data == "confirm_found":
        # Get case details
        case_id = context.user_data.get("found_case_no")
        case = await get_case_by_id(PydanticObjectId(case_id))
        await FinderService.update_or_create_finder(user_id, case=case_id)

        print(f"Inside the found case: {case}")

        if case:
            print(f"Inside the found case: {case}")
            reward_amount = case.reward  # Assuming reward is stored in case
            tax = reward_amount * 0.05
            final_reward = reward_amount - tax

            # Notify the advertiser (the one who posted the case)
            advertiser_message = (
                f"🔔 <b>Case Update</b>\n\n"
                f"Someone has confirmed finding the person in your case!\n\n"
                f"📌 <b>Case Details:</b>\n"
                f"👤 <b>Case ID:</b> {case_id}\n"
                f"💰 <b>Total Reward:</b> {reward_amount} SOL\n"
                f"⚖ <b>Tax (5%):</b> {tax:.2f} SOL\n"
                f"✅ <b>Final Payout:</b> {final_reward:.2f} SOL\n\n"
                f"🚀 The reward is being processed."
            )
            await context.bot.send_message(
                case.user_id, advertiser_message, parse_mode="HTML"
            )

            # Notify the finder (who reported the found person)
            finder_message = (
                f"🎉 <b>Congratulations!</b> 🎉\n\n"
                f"The advertiser has been notified about your confirmation.\n"
                f"💰 Your estimated reward after tax: <b>{final_reward:.2f} SOL</b>\n\n"
                f"Please wait while the payment is processed. 🚀"
            )
            await context.bot.send_message(
                user_id, finder_message, parse_mode="HTML"
            )

            # Notify the owner (admin/platform owner)
            owner_message = (
                f"🔔 <b>Admin Alert</b>\n\n"
                f"A case has been marked as <b>found</b>!\n\n"
                f"📌 <b>Case ID:</b> {case_id}\n"
                f"👤 <b>Advertiser:</b> {case.user_id}\n"
                f"🔎 <b>Finder:</b> {user_id}\n"
                f"💰 <b>Total Reward:</b> {reward_amount} SOL\n"
                f"⚖ <b>Tax (5%):</b> {tax:.2f} SOL\n"
                f"✅ <b>Final Payout:</b> {final_reward:.2f} SOL\n\n"
                f"📢 Please verify and ensure the reward is sent."
            )
            await context.bot.send_message(
                OWNER_TELEGRAM_ID, owner_message, parse_mode="HTML"
            )

            await FinderService.update_or_create_finder(
                user_id,
                extended_reward_status=RewardExtensionStatus.PENDING,
                status=FinderStatus.FIND,
            )

            # Notify user in chat
            await query.message.reply_text(
                "The case owner and advertiser have been notified. Your reward will be sent soon! 💰",
                parse_mode="HTML"
            )
        else:
            await query.message.reply_text("Case not found. Please try again.", parse_mode="HTML")

        return State.END
    else:
        await query.message.reply_text("Okay, let us know if you have any updates.", parse_mode="HTML")
        return State.END


async def handle_found_case(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle 'Found' button clicks from case details"""
    print(f"Inside the handle_found_case function")
    user_id = update.effective_user.id
    query = update.callback_query
    await query.answer()

    try:
        # Extract case number from callback data (format: found_<caseno>)/
        case_no = query.data.split("_")[1]
        context.user_data["found_case_no"] = case_no

        # Ask for proof upload
        await query.edit_message_text(get_text(user_id, "proof_upload", "finder"))
        return State.UPLOAD_PROOF

    except Exception as e:
        logger.error(f"Error handling found case: {e}")
        await query.edit_message_text(get_text(user_id, "error_processing_proof", "finder"))
        return State.END


# ---------------------------- Extend Reward ---------------------------


@catch_async
async def handle_extend_reward_amount(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    print("I'm Inside the Handle Extend Reward Amount ---- 01")

    user_id = update.effective_user.id
    new_reward_str = update.message.text.strip()
    context.user_data["extend_flow"] = True

    demanded_reward = float(new_reward_str)
    case =  context.user_data.get("selected_complaint")
    # print(f"Case: {case}")

    print(f"Demand reward: {demanded_reward}")

    current_reward = float(case.reward)
    print(f"Current Reward: {current_reward}")

    if demanded_reward <= current_reward:
        await update.message.reply_text(
            f"Please enter an amount greater than current reward ({current_reward})"
        )
        return State.EXTEND_REWARD_AMOUNT

    context.user_data["demanded_reward"] = demanded_reward
    context.user_data["reward_difference"] = demanded_reward - current_reward

    wallet_type = case.wallet.wallet_type

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
                    get_text(user_id, "create_wallet", "globals"),
                    callback_data="create_new_wallet",
                )
            ]
        )
        await update.message.reply_text(
            get_text(user_id, "choose_existing_or_new_wallet", "finder"),
            reply_markup=InlineKeyboardMarkup(kb),
            parse_mode="HTML",
        )
        return State.FINDER_CHOOSE_WALLET_TYPE
    else:
        msg = get_text(user_id, "wallet_name_prompt")
        if update.message:
            await update.message.reply_text(msg, parse_mode="HTML")
        elif update.callback_query:
            await update.callback_query.message.reply_text(msg, parse_mode="HTML")

        return State.FINDER_NAME_WALLET


#  ---------------------------- ADVERTISER LOGIC START ---------------------------


async def handle_extend_reward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    case = context.user_data.get("selected_complaint")
    user_id = update.effective_user.id
    if query.data == "yes_extend":
        wallet_type = case.wallet.wallet_type

        await query.message.edit_text(
            f"The current reward amount is <b>{case.reward} {wallet_type}</b>.\n"
            f"Please enter the new reward amount you want to set:",
            parse_mode="HTML"
        )
        return State.EXTEND_REWARD_AMOUNT # Transition to reward amount input
    else:
        #  --------------- If user not extended the  reward ---------------
        # Handle "No" response

        existing_wallets = await WalletService.get_wallet_by_type(
            user_id, case.wallet.wallet_type
        )

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
                        get_text(user_id, "create_wallet", "globals"),
                        callback_data="create_new_wallet",
                    )
                ]
            )
            await query.edit_message_text(
                get_text(user_id, "choose_existing_or_new_wallet", "settings"),
                reply_markup=InlineKeyboardMarkup(kb),
                parse_mode="HTML",
            )
            return State.FINDER_CHOOSE_WALLET_TYPE
        else:
            msg = get_text(user_id, "wallet_name_prompt")
            if update.message:
                await update.message.reply_text(msg, parse_mode="HTML")
            elif update.callback_query:
                await update.callback_query.message.reply_text(msg, parse_mode="HTML")

            return State.FINDER_NAME_WALLET
