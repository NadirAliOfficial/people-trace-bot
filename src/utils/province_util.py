import requests
import pycountry

from models.case_model import Case, CaseStatus

# Cache dictionary to store provinces for countries
province_cache = {}

# CountryStateCity API key and headers
HEADERS = {
    "X-CSCAPI-KEY": "cGk4bW5yQTF3VUg2V0pUS0hwT0FLM2llSWh5ejJ5dmRCbnFRNjlDdw=="
}


def get_country_iso2(country_name):
    """
    Get the ISO2 code for a given country name using pycountry.
    """
    try:
        country = pycountry.countries.get(name=country_name)
        return country.alpha_2 if country else None
    except Exception as e:
        print(f"Error getting ISO2 for {country_name}: {e}")
        return None


def get_provinces_for_country(country_name):
    """
    Fetch provinces/states for the given country using CountryStateCity API,
    with caching to avoid redundant requests.
    """
    print(f"Country: {country_name}")

    # Convert country name to ISO2 code
    iso2 = get_country_iso2(country_name)
    if not iso2:
        print(f"Invalid country name or ISO2 code not found: {country_name}")
        return []

    # Check cache first
    if iso2 in province_cache:
        print(f"Using cached provinces for {iso2}")
        return province_cache[iso2]

    url = f"https://api.countrystatecity.in/v1/countries/{iso2}/states"

    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            states = response.json()
            provinces = [state["name"] for state in states]
            province_cache[iso2] = provinces  # Cache the result
            print(f"Fetched and cached provinces: {provinces}")
            return provinces
        else:
            print("Failed to fetch states:", response.status_code, response.text)
            return []
    except Exception as e:
        print("Exception during API request:", str(e))
        return []


def get_province_matches(query, country_name):
    """
    Get the province match with query and inside the given country.
    """
    query = query.lower()
    provinces = get_provinces_for_country(country_name)
    return [province for province in provinces if query in province.lower()]


async def fetch_cases_by_province(location):
    """
    Fetch cases from the database based on the province.
    """
    case = await Case.find(
        {"last_seen_location": location, "status": CaseStatus.ADVERTISE}
    ).to_list()
    print(f"These are the cases for {location}: {case}")

    return case
