from constant.case_constant import CASE_CONSTANT
from constant.finder_constant import FINDER_CONSTANT
from constant.settings_constant import SETTINGS_CONSTANT
from constant.start_constant import START_LANG_DATA
from constant.stats_constant import STATS_CONSTANT
from constant.wallet_constant import WALLET_LANG_DATA
from constant.wallet_menu_constant import WALLET_MENU_CONSTANT
from constant.listing_constant import LISTING_CONSTANT


def merge_lang_data(lang_data, *new_constants):
    for new_data in new_constants:  # Loop through each constant
        for lang, entries in new_data.items():
            if lang in lang_data:
                lang_data[lang].update(entries)  # Merge into existing language
            else:
                lang_data[lang] = entries  # Add new language section if missing
    return lang_data


LANG_DATA = merge_lang_data(
    START_LANG_DATA,
    WALLET_LANG_DATA,
    SETTINGS_CONSTANT,
    CASE_CONSTANT,
    WALLET_MENU_CONSTANT,
    FINDER_CONSTANT,
    LISTING_CONSTANT,
    STATS_CONSTANT
)

USDT_MINT_ADDRESS = "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB"


user_data_store = {}


def get_text(user_id, key):
    """Get the localized text for a given key based on user language."""
    lang = user_data_store.get(user_id, {}).get("lang", "en")
    return LANG_DATA.get(lang, LANG_DATA["en"]).get(key, f"Undefined text for {key}")


# def get_text(user_id, key, **kwargs):
#     """Fetches the text for the given key based on the user's language."""
#     user_lang = context.user_data.get("lang", "en")  # Default to English
#     text = SETTINGS_CONSTANT[user_lang].get(key, f"Missing translation for '{key}'")
#     return text.format(**kwargs)


# Pagination Constants
ITEMS_PER_PAGE = 5  # Number of items per page for pagination
