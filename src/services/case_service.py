from typing import Optional
from beanie import Link, PydanticObjectId
from models.case_model import Case, CaseStatus
from models.finder_model import Finder, FinderStatus
from models.mobile_number_model import MobileNumber
from models.user_model import User
from models.wallet_model import Wallet
from services.wallet_service import WalletService


async def find_case_by_user_id(user_id: int) -> Optional[Case]:
    """
    Find a case by user ID.

    :param user_id: The user ID to search for.
    :return: The case if found, otherwise None.
    """
    return await Case.find_one(Case.user_id == user_id)


async def get_case_by_id(id: PydanticObjectId, **kwargs) -> Optional[Case]:
    """
    Get a case by its ID.

    :param id: The ID of the case to retrieve.
    :return: The case if found, otherwise None.
    """
    return await Case.get(id=id, **kwargs)


async def add_or_update_case(case_data: dict) -> Case:
    """
    Add a new case or update an existing case based on the user ID.

    :param case_data: The data for the case.
    :return: The added or updated case.
    """
    user_id = case_data.get("user_id")
    existing_case = await find_case_by_user_id(user_id)

    if existing_case:
        # Update the existing case
        for key, value in case_data.items():
            setattr(existing_case, key, value)
        await existing_case.save()
        return existing_case
    else:
        # Create a new case
        new_case = Case(**case_data)
        await new_case.insert()
        return new_case


async def get_drafted_case_by_user(user_id: int) -> Optional[Case]:
    """
    Retrieve a case by user_id. If not found, return None.

    Args:
    - user_id (int): The user ID to search for.

    Returns:
    - case (Optional[Case]): The found case or None if not found.
    """

    return await Case.find_one({"user_id": user_id, "status": CaseStatus.DRAFT})


async def update_or_create_case(user_id: int, **kwargs) -> Case:
    """
    Update an existing case or create a new one if it doesn't exist.

    Args:
    - user_id (int): The user ID for the case to update or create.
    - kwargs (dict): The fields that will be updated or created if not already present.

    Returns:
    - case (Case): The updated or newly created case.
    """
    # Try to find an existing case
    case = await get_drafted_case_by_user(user_id)

    if not case:
        # If no case exists, create a new one
        case = Case(user_id=user_id, status=CaseStatus.DRAFT)

    # Update fields if provided
    for key, value in kwargs.items():
        if value is not None:
            # Ensure the wallet field is assigned properly
            if key == "wallet" and isinstance(value, str):
                wallet = await Wallet.get(PydanticObjectId(value))
                value = wallet  # Directly link the Wallet instance

            # Ensure the mobile field is assigned properly
            elif key == "mobile" and isinstance(value, str):
                # Fetch the MobileNumber reference using the mobile number
                mobile_number = await MobileNumber.find_one({"number": value})
                print("Mobile Number", mobile_number)

                if not mobile_number:
                    # If mobile number doesn't exist, create it
                    user = await User.find_one(
                        {"tl_id": user_id}
                    )  # Fetch the User document
                    if not user:
                        raise ValueError("User not found")

                    mobile_number = MobileNumber(
                        number=value, user=user
                    )  # Link to the actual User document
                    await mobile_number.insert()

                value = mobile_number  # Directly link the MobileNumber instance

            setattr(case, key, value)

    # Save the case (update or create)
    await case.save()
    return case


async def update_case(case_id: PydanticObjectId, **kwargs) -> Case:
    """
    Update a case with the provided data.

    Args:
    - case_id (PydanticObjectId): The ID of the case to update.
    - kwargs (dict): The fields to update.

    Returns:
    - case (Case): The updated case.
    """
    case = await Case.get(case_id)
    if not case:
        raise ValueError("Case not found")

    for key, value in kwargs.items():
        if value is not None:
            setattr(case, key, value)

    await case.save()


async def get_drafted_case_wallet(user_id: int) -> dict:
    try:
        case = await get_drafted_case_by_user(user_id)
        if not case:
            return None

        await case.fetch_all_links()

        if not hasattr(case, "wallet") or case.wallet is None:
            return None

        return case.wallet.model_dump()
    except Exception as e:
        # Log the error or handle it as needed
        print(f"Error: {str(e)}")
        return None


async def get_complaints_by_country_and_province(
    country: str, province: str, user_id: int
) -> list:
    """
    Get all complaints for a given country and province that the user has applied to.

    :param country: The country code.
    :param province: The province code.
    :param user_id: The user ID of the finder.
    :return: A list of complaints.
    """
    # Find all finder entries for the user with status "find"
    applied_finders = await Finder.find(
        {"user_id": user_id, "status": FinderStatus.FIND},
        fetch_links=True,
    ).to_list()

    # Get the list of case IDs the user has applied to
    applied_case_ids = [finder.case.id for finder in applied_finders]

    # Find all cases that match the criteria and have not been applied to by the user
    return await Case.find(
        {
            "country": country,
            "province": province,
            "status": CaseStatus.ADVERTISE,
            "_id": {"$nin": applied_case_ids},
        },
        fetch_links=True,
    ).to_list()
