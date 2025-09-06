from datetime import datetime
from typing import Optional, List
from beanie import PydanticObjectId
from models.extend_reward_model import ExtendReward
from models.finder_model import Finder, FinderStatus, RewardExtensionStatus
from models.case_model import Case, CaseStatus
from models.wallet_model import Wallet
from utils.logger import logger


class FinderService:
    @staticmethod
    async def create_finder(
        user_id: int,
        case_id: PydanticObjectId,
        reported_location: str,
        proof_url: Optional[str] = None,
        country: Optional[str] = None,
        city: Optional[str] = None,
    ) -> Finder:
        """
        Create a new Finder document.
        """
        finder = Finder(
            user_id=user_id,
            case=case_id,
            reported_location=reported_location,
            proof_url=proof_url,
            country=country,
            city=city,
            status=FinderStatus.DRAFT,
        )
        await finder.insert()
        logger.info(f"Created new Finder for user {user_id} on case {case_id}")
        return finder

    @staticmethod
    async def get_finder_by_id(finder_id: PydanticObjectId) -> Optional[Finder]:
        """
        Retrieve a Finder document by its ID.
        """
        return await Finder.get(finder_id)

    @staticmethod
    async def get_finders_by_user(user_id: int) -> List[Finder]:
        """
        Retrieve all Finder documents for a specific user.
        """
        return await Finder.find(Finder.user_id == user_id).to_list()

    @staticmethod
    async def get_finders_by_case(case_id: PydanticObjectId) -> List[Finder]:
        """
        Retrieve all Finder documents for a specific case.
        """
        return await Finder.find(Finder.case == case_id).to_list()

    @staticmethod
    async def update_finder_proof(
        finder_id: PydanticObjectId, proof_url: str
    ) -> Optional[Finder]:
        """
        Update the proof URL for a Finder document.
        """
        finder = await Finder.get(finder_id)
        if finder:
            finder.proof_url = proof_url
            await finder.save()
            logger.info(f"Updated proof URL for Finder {finder_id}")
        return finder

    @staticmethod
    async def request_reward_extension(
        finder_id: PydanticObjectId, demanded_reward: float
    ) -> Optional[Finder]:
        """
        Request an extended reward for a Finder document.
        """
        finder = await Finder.get(finder_id)
        if finder:
            finder.extended_reward_requested = demanded_reward
            finder.extended_reward_status = RewardExtensionStatus.PENDING
            finder.extended_reward_timestamp = datetime.utcnow()
            await finder.save()
            logger.info(f"Requested reward extension for Finder {finder_id}")
        return finder

    @staticmethod
    async def respond_to_reward_extension(
        finder_id: PydanticObjectId, accepted: bool
    ) -> Optional[Finder]:
        """
        Respond to a reward extension request (accept or reject).
        """
        finder = await Finder.get(finder_id)
        if finder:
            finder.extended_reward_status = (
                RewardExtensionStatus.ACCEPTED
                if accepted
                else RewardExtensionStatus.REJECTED
            )
            finder.extended_reward_response_timestamp = datetime.utcnow()
            await finder.save()
            logger.info(f"Responded to reward extension for Finder {finder_id}")
        return finder

    @staticmethod
    async def complete_reward_extension(
        finder_id: PydanticObjectId,
    ) -> Optional[Finder]:
        """
        Mark a reward extension as completed (after successful transfer).
        """
        finder = await Finder.get(finder_id)
        if finder:
            finder.extended_reward_status = RewardExtensionStatus.COMPLETED
            finder.extended_reward_completed_timestamp = datetime.utcnow()
            await finder.save()
            logger.info(f"Completed reward extension for Finder {finder_id}")
        return finder

    @staticmethod
    async def delete_finder(finder_id: PydanticObjectId) -> bool:
        """
        Delete a Finder document by its ID.
        """
        finder = await Finder.get(finder_id)
        if finder:
            await finder.delete()
            logger.info(f"Deleted Finder {finder_id}")
            return True
        return False

    @staticmethod
    async def get_pending_reward_extension_requests() -> List[Finder]:
        """
        Retrieve all Finder documents with pending reward extension requests.
        """
        return await Finder.find(
            Finder.extended_reward_status == RewardExtensionStatus.PENDING
        ).to_list()

    @staticmethod
    async def get_drafted_finder_by_user(user_id: int) -> Optional[Finder]:
        """
        Retrieve a finder by user_id. If not found, return None.

        Args:
        - user_id (int): The user ID to search for.

        Returns:
        - finder (Optional[Finder]): The found finder or None if not found.
        """
        return await Finder.find_one({"user_id": user_id, "status": FinderStatus.DRAFT})

    @staticmethod
    async def update_or_create_finder(user_id: int, **kwargs) -> Finder:

        finder = await FinderService.get_drafted_finder_by_user(user_id)

        if not finder:
            # If no case exists, create a new one
            finder = Finder(user_id=user_id, status=FinderStatus.DRAFT)

        # Update fields if provided
        for key, value in kwargs.items():
            if value is not None:
                if key == "wallet" and isinstance(value, str):
                    wallet = await Wallet.get(PydanticObjectId(value))
                    setattr(finder, key, wallet)
                elif key == "case" and (
                    isinstance(value, str) or isinstance(value, PydanticObjectId)
                ):
                    case_id = PydanticObjectId(value) if isinstance(value, str) else value
                    case = await Case.get(case_id)
                    setattr(finder, key, case)
                elif key == "extend_reward_ref" and isinstance(value, str):
                    extend_reward = await ExtendReward.get(PydanticObjectId(value))
                    if finder.extend_reward_ref is None:
                        finder.extend_reward_ref = []
                    finder.extend_reward_ref.append(extend_reward)
                else:
                    setattr(finder, key, value)

        # Save the case (update or create)
        await finder.save()
        return finder
