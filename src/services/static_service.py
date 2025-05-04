# services/stats_service.py

from models.case_model import Case, CaseStatus
from datetime import timedelta


class StatsService:
    @staticmethod
    async def get_global_stats():
        total = await Case.count()

        # ✅ Use .value for enums in DB queries
        solved = await Case.find({"status": CaseStatus.COMPLETED.value}).count()
        unsolved = await Case.find({"status": CaseStatus.ADVERTISE.value}).count()

        # Average reward
        avg_reward_pipeline = [
            {"$match": {"reward": {"$gt": 0}}},
            {"$group": {"_id": None, "avg": {"$avg": "$reward"}}}
        ]
        avg_reward_result = await Case.aggregate(avg_reward_pipeline).to_list(length=1)
        avg_reward = round(avg_reward_result[0]["avg"], 2) if avg_reward_result else 0

        # Highest reward
        highest_pipeline = [
            {"$match": {"reward": {"$gt": 0}}},
            {"$sort": {"reward": -1}},
            {"$limit": 1}
        ]
        highest_result = await Case.aggregate(highest_pipeline).to_list(length=1)
        highest_reward = highest_result[0]["reward"] if highest_result else 0

        # Fastest case solved (in days)
        fastest_pipeline = [
            {
                "$match": {
                    "status": CaseStatus.COMPLETED.value,
                    "created_at": {"$exists": True},
                    "updated_at": {"$exists": True}
                }
            },
            {
                "$addFields": {
                    "days_to_solve": {
                        "$divide": [
                            {"$subtract": ["$updated_at", "$created_at"]},
                            1000 * 60 * 60 * 24  # milliseconds to days
                        ]
                    }
                }
            },
            {"$sort": {"days_to_solve": 1}},
            {"$limit": 1}
        ]
        fastest_result = await Case.aggregate(fastest_pipeline).to_list(length=1)
        fastest_days = round(fastest_result[0]["days_to_solve"], 1) if fastest_result else 0

        # Top active region
        top_region_pipeline = [
            {"$match": {"country": {"$exists": True}, "city": {"$exists": True}}},
            {
                "$group": {
                    "_id": {"country": "$country", "city": "$city"},
                    "count": {"$sum": 1}
                }
            },
            {"$sort": {"count": -1}},
            {"$limit": 1}
        ]
        top_region_result = await Case.aggregate(top_region_pipeline).to_list(length=1)
        top_region = (
            f"{top_region_result[0]['_id']['city']}, {top_region_result[0]['_id']['country']}"
            if top_region_result else "N/A"
        )

        # Common demographic
        demographics_pipeline = [
            {"$match": {"gender": {"$in": ["male", "female", "other"]}, "age": {"$type": "number", "$gte": 0}}},

            {
                "$bucket": {
                    "groupBy": "$age",
                    "boundaries": [0, 18, 25, 35, 50, 65, 100],
                    "output": {
                        "males": {
                            "$sum": {"$cond": [{"$eq": ["$gender", "male"]}, 1, 0]}
                        },
                        "females": {
                            "$sum": {"$cond": [{"$eq": ["$gender", "female"]}, 1, 0]}
                        },
                        "others": {
                            "$sum": {"$cond": [{"$eq": ["$gender", "other"]}, 1, 0]}
                        }
                    }
                }
            },
            {
                "$addFields": {
                    "index": {"$toInt": "$_id"}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "range": {
                        "$arrayElemAt": [["0-17", "18-24", "25-34", "35-49", "50-64", "65+"], "$index"]
                    },
                    "males": 1,
                    "females": 1,
                    "others": 1
                }
            }
        ]

        demographics_result = await Case.aggregate(demographics_pipeline).to_list()

        max_count = 0
        top_gender = ""
        top_age_range = ""

        for entry in demographics_result:
            if "range" not in entry:
                continue  # Skip invalid entries

            for gender_key in ["males", "females", "others"]:
                count = entry.get(gender_key, 0)
                if count > max_count:
                    max_count = count
                    top_gender = gender_key.replace("males", "Male").replace("females", "Female").replace("others", "Other")
                    top_age_range = entry.get("range", "Unknown")

        top_demographic = f"{top_gender}, aged {top_age_range}" if max_count else "N/A"

        # Countries and cities covered
        location_pipeline = [
            {"$match": {"country": {"$exists": True}, "city": {"$exists": True}}},
            {
                "$group": {
                    "_id": None,
                    "countries": {"$addToSet": "$country"},
                    "cities": {"$addToSet": "$city"}
                }
            },
            {
                "$project": {
                    "country_count": {"$size": "$countries"},
                    "city_count": {"$size": "$cities"}
                }
            }
        ]
        location_result = await Case.aggregate(location_pipeline).to_list(length=1)

        countries = location_result[0]["country_count"] if location_result else 0
        cities = location_result[0]["city_count"] if location_result else 0

        return {
            "total_cases": total,
            "solved": solved,
            "unsolved": unsolved,
            "avg_reward": avg_reward,
            "highest": highest_reward,
            "fastest": fastest_days,
            "top_region": top_region,
            "top_demo": top_demographic,
            "countries": countries,
            "cities": cities,
        }

    @staticmethod
    async def get_unsolved_by_country():
        result = await Case.aggregate([
            {"$match": {"status": CaseStatus.ADVERTISE.value}},
            {"$group": {"_id": "$country", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]).to_list()
        return [{"name": r["_id"], "count": r["count"]} for r in result]

    @staticmethod
    async def get_unsolved_cases_by_country(country: str):
        return await Case.find({"country": country, "status": CaseStatus.ADVERTISE.value}).to_list()