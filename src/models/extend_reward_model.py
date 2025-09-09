from datetime import datetime
from typing import Optional
from beanie import Document, Link
from pydantic import  Field
from enum import Enum
from models.case_model import Case


class ExtendRewardStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ExtendReward(Document):
    case: Link[Case] = Field(default=None)
    user_id: int
    status: ExtendRewardStatus = Field(default=ExtendRewardStatus.PENDING)
    reason: Optional[str] = None
    extend_reward_amount: Optional[float] = None
    deleted: Optional[bool] = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)    
    