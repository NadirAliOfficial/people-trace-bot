from constant.case_constant import CASE_CONSTANT
from constant.finder_constant import FINDER_CONSTANT
from constant.global_constant import GLOBAL_CONSTANT
from constant.settings_constant import SETTINGS_CONSTANT
from constant.start_constant import START_LANG_DATA
from constant.start_mobile_number_constant import START_MOBILE_NUMBER_CONSTANT
from constant.start_wallet_constant import START_WALLET_CONSTANT
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


LANG_DATA = {
    "settings": SETTINGS_CONSTANT,
    "globals": GLOBAL_CONSTANT,
    "wallets": WALLET_LANG_DATA,
    "start-complaints": START_LANG_DATA,
    "start-mobile": START_MOBILE_NUMBER_CONSTANT,
    "cases": CASE_CONSTANT,
    "start-wallet": START_WALLET_CONSTANT,
    "stats": STATS_CONSTANT,
    "finder": FINDER_CONSTANT,
}

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
    user_lang_code = user_data_store.get(user_id, {}).get("lang", "english")
    
    handler_data = LANG_DATA.get(handler_constant, {})
    
    # Use global english_dict as fallback
    lang_dict = handler_data.get(user_lang_code)
    
    return lang_dict.get(
        key,
        f"Undefined text for key '{key}' in handler '{handler_constant}'"
    )



ITEMS_PER_PAGE = 5
