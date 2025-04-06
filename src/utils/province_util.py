import requests


def get_provinces_for_country(country):
    """
    Fetch provinces/states for the given country using REST Countries API.
    """
    print(f"Country: {country}")
    url = "https://countriesnow.space/api/v0.1/countries/states"
    data = {"country": country}

    response = requests.post(url, json=data)

    if response.status_code == 200:
        states = response.json()
        print(f"states: {states["data"]["states"]}")
        print([state["name"] for state in states["data"]["states"]])
        return [state["name"] for state in states["data"]["states"]]
    else:
        print("Failed to fetch states:", response.status_code)
        return []
    




def get_province_matches(query, country):
    """Geting the province match with query and inside the country which provided"""
    query = query.lower()
    provinces = get_provinces_for_country(country)
    return [province for province in provinces if query in province.lower()]


async def fetch_cases_by_province(location):
    """
    Fetch cases from the database based on the province.
    """
    # Implement this function
    case = await Case.find(
        {"last_seen_location": location, "status": CaseStatus.ADVERTISE}
    ).to_list()
    print(f"These are the cases for {location}: {case}")

    return case