from datetime import datetime
from beanie import Document, Link
from pydantic import Field

from models.user_model import User


class MobileNumber(Document):
    number: str = Field(unique=True)  # Ensure uniqueness
    user: Link[User]  # Linking to User
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "mobile_numbers"
