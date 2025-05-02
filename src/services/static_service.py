# services/stats_service.py

from models.case_model import Case
from bson import ObjectId
from beanie import PydanticObjectId


class StatsService:
    @staticmethod
    async def get_global_stats():
        total = await Case.count()
        solved = await Case.find({"status": "FOUND"}).count()
        unsolved = await Case.find({"status": "ADVERTISE"}).count()
        avg_reward = await Case.aggregate([
            {"$match": {"reward_amount": {"$exists": True}}},
            {"$group": {"_id": None, "avg": {"$avg": "$reward_amount"}}}
        ]).to_list(length=1)
        highest = await Case.find().sort("-reward_amount").limit(1).to_list()
        return {
            "total_cases": total,
            "solved": solved,
            "unsolved": unsolved,
            "avg_reward": round(avg_reward[0]["avg"], 2) if avg_reward else 0,
            "highest": highest[0].reward_amount if highest else 0,
            "fastest": 2,  # TODO: dynamic
            "top_region": "Central Singapore",  # TODO: dynamic
            "top_demo": "Males, aged 25–35",
            "countries": 36,
            "cities": 128,
        }

    @staticmethod
    async def get_unsolved_by_country():
        result = await Case.aggregate([
            {"$match": {"status": "ADVERTISE"}},
            {"$group": {"_id": "$country", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]).to_list()
        return [{"name": r["_id"], "count": r["count"]} for r in result]

    @staticmethod
    async def get_unsolved_cases_by_country(country: str):
        return await Case.find({"country": country, "status": "ADVERTISE"}).to_list()
