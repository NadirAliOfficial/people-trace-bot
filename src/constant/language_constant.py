from constant.case_constant import CASE_CONSTANT
from constant.finder_constant import FINDER_CONSTANT
from constant.global_constant import GLOBAL_CONSTANT
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


LANG_DATA = {"settings": SETTINGS_CONSTANT, "globals": GLOBAL_CONSTANT, "wallets": WALLET_LANG_DATA, "start-complaints": START_LANG_DATA}

# LANG_DATA = merge_lang_data(
#     START_LANG_DATA, # ** DONE
#     WALLET_LANG_DATA, # ** DONE
#     SETTINGS_CONSTANT, # ** DOING
#     CASE_CONSTANT, # !DOING
#     WALLET_MENU_CONSTANT, # ** DONE
#     FINDER_CONSTANT, # ** DONE
#     LISTING_CONSTANT, # ** DONE
#     STATS_CONSTANT # ** DONE
# )

USDT_MINT_ADDRESS = "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB"


user_data_store = {}


LANG_CODE_MAP = {
    "en": "english",
    "zh": "chinese",
    "ms": "malay",
    "id": "indonesian",
    "th": "thai",
    "vi": "vietnamese",
    "km": "khmer",
    "ja": "japanese",
    "ko": "korean",
    "ur": "urdu",
}


def get_text(user_id, key, handler_constant):
    """
    Get the localized text for a given key from a specific handler constant.

    Args:
        user_id (int): The ID of the user.
        key (str): The key for the desired text (e.g., "btn_language").
        handler_constant (str): The name of the constant set (e.g., "settings").

    Returns:
        str: The localized text string.
    """
    # 1. Get the user's preferred language code (e.g., 'en', 'zh'), default to 'en'.
    user_lang_code = user_data_store.get(user_id, {}).get("lang", "en")

    # 2. Map the code to the full language name used in APP_CONSTANTS (e.g., 'english').
    lang_name = LANG_CODE_MAP.get(user_lang_code, "english")

    # 3. Get the dictionary for the specified handler (e.g., APP_CONSTANTS['settings']).
    #    Fallback to an empty dict if the handler doesn't exist.
    handler_data = LANG_DATA.get(handler_constant, {})

    # 4. Get the specific language dictionary from the handler data.
    #    Fallback to the English dictionary if the user's language is not found.
    english_fallback = handler_data.get("english", {})
    lang_dict = handler_data.get(lang_name, english_fallback)

    # 5. Return the requested text by key.
    #    Fallback to a helpful message if the key is not defined.
    return lang_dict.get(key, f"Undefined text for key '{key}' in '{handler_constant}'")


# def get_text(user_id, key, **kwargs):
#     """Fetches the text for the given key based on the user's language."""
#     user_lang = context.user_data.get("lang", "en")  # Default to English
#     text = SETTINGS_CONSTANT[user_lang].get(key, f"Missing translation for '{key}'")
#     return text.format(**kwargs)


# Pagination Constants
ITEMS_PER_PAGE = 5  # Number of items per page for pagination
