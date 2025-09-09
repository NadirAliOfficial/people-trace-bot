from enum import Enum
from beanie import Document, Link
from typing import List, Optional
from datetime import datetime
from pydantic import Field
from models.case_model import Case
from models.extend_reward_model import ExtendReward
from models.wallet_model import Wallet


class FinderStatus(Enum):
    DRAFT = "draft"
    FIND = "find"
    COMPLETED = "completed"


class RewardExtensionStatus(Enum):
    PENDING = "pending"  # Request sent, awaiting advertiser response
    ACCEPTED = "accepted"  # Advertiser accepted the request
    REJECTED = "rejected"  # Advertiser rejected the request
    COMPLETED = "completed"  # Reward extension processed successfully


class Finder(Document):
    country: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    status: FinderStatus = Field(default=FinderStatus.DRAFT)
    user_id: int  # Telegram user ID of the finder
    case: Optional[Link[Case]] = None  # Reference to the case the finder is reporting
    proof_url: Optional[List[str]] = None  # Uploaded proof image/video URL
    wallet: Optional[Link[Wallet]] = None
    reported_location: Optional[str] = None  # Location where the person was seen
    timestamp: datetime = Field(
        default_factory=datetime.utcnow
    )  # When the report was made

    # Extended Reward Fields
    extended_reward_requested: Optional[float] = None  # Amount requested by the finder
    extended_reward_status: Optional[RewardExtensionStatus] = (
        None  # Status of the reward extension request
    )
    extended_reward_timestamp: Optional[datetime] = (
        None  # When the reward extension was requested
    )
    extended_reward_response_timestamp: Optional[datetime] = (
        None  # When the advertiser responded
    )
    extended_reward_completed_timestamp: Optional[datetime] = (
        None  # When the reward was transferred
    )

    class Settings:
        name = "finders"
