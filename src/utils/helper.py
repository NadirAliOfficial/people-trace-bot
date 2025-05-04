import logging
import math
import random

import geonamescache
import pycountry

from constant.language_constant import ITEMS_PER_PAGE
from utils.province_util import get_provinces_for_country


def generate_tac():
    """Generate a 6-digit TAC."""
    return str(random.randint(100000, 999999))


def validate_mobile(number):
    """Validate mobile number format."""
    return len(number) >= 10 and number.startswith("+")


async def send_tac_sms(mobile, tac):
    """Simulate sending TAC via SMS."""
    print(f"Sent TAC {tac} to {mobile}")


def save_case_to_db(case_data):
    """Simulate saving case data to a database."""
    print(f"Case saved to DB: {case_data}")


def transfer_to_escrow(wallet, amount):
    """Simulate transferring funds to escrow."""
    print(f"Transferred {amount} SOL to escrow from wallet {wallet}")
    return True  # Simulate success


def get_city_matches(country_name, query):
    return [
        c for c in get_cities_by_country(country_name) if query.lower() in c.lower()
    ]


def get_province_matches(query, country):
    """Geting the province match with query and inside the country which provided"""
    query = query.lower()
    provinces = get_provinces_for_country(country)
    return [province for province in provinces if query in province.lower()]


gc = geonamescache.GeonamesCache()


def paginate_list(items, page, items_per_page=ITEMS_PER_PAGE):
    """Helper to paginate list items."""
    total_pages = max(1, math.ceil(len(items) / items_per_page)) if items else 1
    page = max(1, min(page, total_pages))
    start = (page - 1) * items_per_page
    end = start + items_per_page
    return items[start:end], total_pages


def get_country_matches(query):
    query = query.lower()
    return [c.name for c in pycountry.countries if query in c.name.lower()]


def get_cities_by_country(country_name):
    country = pycountry.countries.get(name=country_name)
    if not country:
        return []
    country_code = country.alpha_2
    all_cities = gc.get_cities().values()
    filtered = [city for city in all_cities if city["countrycode"] == country_code]
    if not filtered:
        return []
    sorted_cities = sorted(filtered, key=lambda x: x["population"], reverse=True)
    return [city["name"] for city in sorted_cities[:50]]


# Setup logging
def setup_logging():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
        handlers=[
            logging.FileHandler("bot.log"),  # Log to a file named bot.log
            logging.StreamHandler(),  # Also log to the console
        ],
    )
    logger = logging.getLogger(__name__)
    logger.info("Logging setup complete.")
