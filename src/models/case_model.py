from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, validator
from beanie import Document, Link
from enum import Enum

from models.mobile_number_model import MobileNumber
from models.wallet_model import Wallet


class CaseStatus(Enum):
    DRAFT = "draft"
    ADVERTISE = "advertise"
    COMPLETED = "completed"


class Case(Document):
    user_id: int
    country: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    wallet: Link[Wallet] = None
    status: CaseStatus = Field(default=CaseStatus.DRAFT)
    case_no: Optional[str] = None
    name: Optional[str] = None
    mobile: Link[MobileNumber] = None
    person_name: Optional[str] = None
    relationship: Optional[str] = None
    case_photo: Optional[str] = None
    last_seen_location: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    hair_color: Optional[str] = None
    eye_color: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    distinctive_features: Optional[str] = None
    reward_type: Optional[str] = None
    reward: Optional[float] = None
    reason: Optional[str] = None
    deleted: Optional[bool] = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "cases"  # The name of the collection in MongoDB

    @validator("gender", check_fields=False)
    def validate_gender(cls, v):
        if v and v not in ["male", "female", "other"]:
            raise ValueError("Invalid gender")
        return v

    @validator("age", check_fields=False)
    def validate_age(cls, v):
        if v and v < 0:
            raise ValueError("Age must be a positive integer")
        return v

    @validator("height", "weight", check_fields=False)
    def validate_positive(cls, v):
        if v and v <= 0:
            raise ValueError("Height and weight must be positive values")
        return v
