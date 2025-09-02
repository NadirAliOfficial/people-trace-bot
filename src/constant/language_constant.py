# Placeholder for language constants
from constant.case_constant import CASE_CONSTANT

def get_text(user_id, key, category=""):
    """Get localized text for the user."""
    # Default to English for now - you can implement user language detection here
    language = "english"  
    
    if category == "cases":
        return CASE_CONSTANT.get(language, {}).get(key, f"Missing: {key}")
    
    # Add other categories as needed
    return f"Missing: {key} in {category}"