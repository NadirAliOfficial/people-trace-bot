# Placeholder case model
from enum import Enum

class CaseStatus(Enum):
    DRAFT = "draft"
    ADVERTISE = "advertise"
    ACTIVE = "active"
    COMPLETED = "completed"

class Case:
    @classmethod
    async def find_one(cls, query, fetch_links=False):
        # Placeholder implementation
        return None
    
    async def save(self):
        # Placeholder implementation
        pass