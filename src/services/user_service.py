from typing import List

from beanie import PydanticObjectId
from models.mobile_number_model import MobileNumber
from models.user_model import User


async def get_user_lang(user_id: int) -> str:
    """Get the user's language preference from the database."""
    user = await User.find_one(User.tl_id == user_id)
    return user.lang if user else None


async def save_user_lang(user_id: int, lang: str):
    """Save the user's language preference to the database."""
    user = await User.find_one(User.tl_id == user_id)
    if user:
        user.lang = lang
        await user.save()
    else:
        user = User(tl_id=user_id, lang=lang)
        await user.insert()


async def save_user_mobiles(user_id: int, new_mobile: str):
    """
    Save a new mobile number for a user while ensuring uniqueness.
    """
    # Check if the number already exists
    existing_number = await MobileNumber.find_one({"number": new_mobile})
    if existing_number:
        raise ValueError("This mobile number is already registered.")

    # Get the user
    user = await User.find_one({"tl_id": user_id})
    if not user:
        user = User(tl_id=user_id, lang="en")
        await user.save()

    # Create a new mobile entry linked to the user
    mobile_entry = MobileNumber(
        number=new_mobile, user=user
    )  # Use user ID for reference
    await mobile_entry.insert()


from beanie import PydanticObjectId


async def get_user_mobiles(user_id: PydanticObjectId):
    """
    Retrieve all mobile numbers linked to a user.
    """
    user = await User.find_one(User.tl_id == user_id)

    print("user is in get user mobiles", user)
    if not user:
        user = User(tl_id=user_id, lang="en")
        await user.save()

    mobile_numbers = await MobileNumber.find({"user.$id": user.id}).to_list()

    print("These are the numbers", mobile_numbers)
    return [mobile.number for mobile in mobile_numbers]  # Extract numbers


async def delete_user_mobile(user_id: int, mobile_number: str):
    """
    Delete a mobile number linked to a user.
    """
    # Get the user
    user = await User.find_one({"tl_id": user_id})
    if not user:
        raise ValueError("User not found.")

    # Get the mobile number
    mobile = await MobileNumber.find_one({"number": mobile_number})
    if not mobile:
        raise ValueError("Mobile number not found.")

    # Delete the mobile number
    await mobile.delete()


def validate_mobile(mobile: str) -> bool:
    # Add your validation logic here. For example, checking format or length.
    # Simple validation example for mobile number format.
    import re

    pattern = r"^\+?[1-9]\d{1,14}$"  # E.164 format
    return bool(re.match(pattern, mobile))
