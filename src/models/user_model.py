from datetime import datetime
from typing import List
from beanie import Document
from pydantic import Field


class User(Document):
    tl_id: int = Field(...)
    lang: str = Field(...)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
