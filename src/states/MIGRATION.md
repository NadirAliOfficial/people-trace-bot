# Migration Guide: From Monolithic State to Separated States

This guide helps you migrate from the old monolithic `State` class to the new separated state classes.

## Before (Old Structure)

```python
from constants import State

# All states were in one class
states = {
    State.LANGUAGE_SELECTED: [...],
    State.CHOOSE_COUNTRY: [...],
    State.WALLETS.WALLET_MENU: [...],
    State.SETTINGS.SETTINGS_MENU: [...],
    State.FINDER.CREATE_CASE_MOBILE: [...],
}
```

## After (New Structure)

```python
from states import StartState, WalletState, SettingsState, FinderState

# States are organized by functionality
states = {
    StartState.LANGUAGE_SELECTED: [...],
    StartState.CHOOSE_COUNTRY: [...],
    WalletState.WALLET_MENU: [...],
    SettingsState.SETTINGS_MENU: [...],
    FinderState.CREATE_CASE_MOBILE: [...],
}
```

## Migration Steps

### 1. Update Imports

**Old:**
```python
from constants import State
```

**New:**
```python
from states import StartState, WalletState, SettingsState, FinderState, StatsState, ListingState, CaseState
```

### 2. Replace State References

#### Start and Case States
```python
# Old
State.LANGUAGE_SELECTED → StartState.LANGUAGE_SELECTED
State.CHOOSE_COUNTRY → StartState.CHOOSE_COUNTRY
State.CREATE_CASE_MOBILE → StartState.CREATE_CASE_MOBILE
State.CASE_DETAILS → StartState.CASE_DETAILS
State.UPLOAD_PROOF → StartState.UPLOAD_PROOF
State.ENTER_LOCATION → StartState.ENTER_LOCATION
State.EXTEND_REWARD → StartState.EXTEND_REWARD
State.CONFIRM_FOUND → StartState.CONFIRM_FOUND
State.ADVERTISER_RESPONSE → StartState.ADVERTISER_RESPONSE
State.FINDER_CHOOSE_WALLET_TYPE → StartState.FINDER_CHOOSE_WALLET_TYPE
State.FINDER_NAME_WALLET → StartState.FINDER_NAME_WALLET
State.FINDER_CONFIRM_TRANSACTION → StartState.FINDER_CONFIRM_TRANSACTION
State.TRANSFER_CONFIRMATION → StartState.TRANSFER_CONFIRMATION
State.CONFIRM_EXTEND → StartState.CONFIRM_EXTEND
State.ENTER_COUNTRY → StartState.ENTER_COUNTRY
State.ENTER_CITY → StartState.ENTER_CITY
State.EDIT_FIELD → StartState.EDIT_FIELD
State.REWARD_TRANSFER_PROCESS → StartState.REWARD_TRANSFER_PROCESS
State.FINISHED → StartState.FINISHED
State.EXTEND_REWARD_CONFIRM → StartState.EXTEND_REWARD_CONFIRM
State.EXTEND_REWARD_FINISHED → StartState.EXTEND_REWARD_FINISHED
State.EXTEND_REWARD_ASK_REASON → StartState.EXTEND_REWARD_ASK_REASON
State.SELECT_WALLET_FOR_EXTEND → StartState.SELECT_WALLET_FOR_EXTEND
State.ENTER_WALLET_NAME → StartState.ENTER_WALLET_NAME
State.SELECT_WALLET_TYPE → StartState.SELECT_WALLET_TYPE
State.CONFIRM_REWARD → StartState.CONFIRM_REWARD
```

#### Wallet States
```python
# Old
State.WALLETS.WALLET_MENU → WalletState.WALLET_MENU
State.WALLETS.SOL_WALLET_DETAIL → WalletState.SOL_WALLET_DETAIL
State.WALLETS.SOL_WALLET_ACTIONS → WalletState.SOL_WALLET_ACTIONS
State.WALLETS.USDT_WALLET_DETAIL → WalletState.USDT_WALLET_DETAIL
State.WALLETS.USDT_WALLET_ACTIONS → WalletState.USDT_WALLET_ACTIONS
State.WALLETS.CONFIRM_PRIVATE_KEY → WalletState.CONFIRM_PRIVATE_KEY
State.WALLETS.SHOW_ADDRESS → WalletState.SHOW_ADDRESS
State.WALLETS.VIEW_HISTORY → WalletState.VIEW_HISTORY
State.WALLETS.SELECT_WALLET_TYPE → WalletState.SELECT_WALLET_TYPE
State.WALLETS.ENTER_WALLET_NAME → WalletState.ENTER_WALLET_NAME
State.WALLETS.CONFIRM_DELETE_WALLET → WalletState.CONFIRM_DELETE_WALLET
State.WALLETS.DELETE_WALLET → WalletState.DELETE_WALLET
State.WALLETS.END → WalletState.END
```

#### Settings States
```python
# Old
State.SETTINGS.SETTINGS_MENU → SettingsState.SETTINGS_MENU
State.SETTINGS.WAITING_FOR_MOBILE → SettingsState.WAITING_FOR_MOBILE
State.SETTINGS.SETTINGS_MOBILE_MANAGEMENT → SettingsState.SETTINGS_MOBILE_MANAGEMENT
State.SETTINGS.MOBILE_VERIFICATION → SettingsState.MOBILE_VERIFICATION
State.SETTINGS.SETTINGS_CREATE_CASE_TAC → SettingsState.SETTINGS_CREATE_CASE_TAC
State.SETTINGS.END → SettingsState.END
```

#### Finder States
```python
# Old
State.FINDER.CREATE_CASE_MOBILE → FinderState.CREATE_CASE_MOBILE
State.FINDER.MOBILE_MANAGEMENT → FinderState.MOBILE_MANAGEMENT
State.FINDER.CREATE_CASE_TAC → FinderState.CREATE_CASE_TAC
State.FINDER.FINDER_DISCLAIMER → FinderState.FINDER_DISCLAIMER
State.FINDER.CHOOSE_COUNTRY → FinderState.CHOOSE_COUNTRY
State.FINDER.CHOOSE_PROVINCE → FinderState.CHOOSE_PROVINCE
State.FINDER.VIEW_COMPLAINTS → FinderState.VIEW_COMPLAINTS
State.FINDER.END → FinderState.END
```

#### Stats States
```python
# Old
State.SHOW_STATS_MENU → StatsState.SHOW_STATS_MENU
State.SHOW_UNSOLVED_COUNTRIES → StatsState.SHOW_UNSOLVED_COUNTRIES
State.SHOW_MY_CASES → StatsState.SHOW_MY_CASES
State.ASK_LOCAL_PROVINCE_CITY → StatsState.ASK_LOCAL_PROVINCE_CITY
```

#### Listing States
```python
# Old
State.CASE_DETAILS → ListingState.CASE_DETAILS
State.ENTER_COUNTRY → ListingState.ENTER_COUNTRY
State.ENTER_CITY → ListingState.ENTER_CITY
State.EDIT_FIELD → ListingState.EDIT_FIELD
State.CONFIRM_EXTEND → ListingState.CONFIRM_EXTEND
State.SELECT_WALLET_FOR_EXTEND → ListingState.SELECT_WALLET_FOR_EXTEND
State.REWARD_TRANSFER_PROCESS → ListingState.REWARD_TRANSFER_PROCESS
State.CHOOSE_COUNTRY → ListingState.CHOOSE_COUNTRY
State.CHOOSE_CITY → ListingState.CHOOSE_CITY
State.CONFIRM_REWARD → ListingState.CONFIRM_REWARD
State.CHOOSE_WALLET_TYPE → ListingState.CHOOSE_WALLET_TYPE
State.NAME_WALLET → ListingState.NAME_WALLET
```

#### Case States
```python
# Old
State.ENTER_PRIVATE_KEY → CaseState.ENTER_PRIVATE_KEY
State.ENTER_PUBLIC_KEY → CaseState.ENTER_PUBLIC_KEY
State.CONFIRM_TRANSFER → CaseState.CONFIRM_TRANSFER
State.TRANSFER_CONFIRMATION → CaseState.TRANSFER_CONFIRMATION
State.CREATE_CASE_WALLET_TRANSFER → CaseState.CREATE_CASE_WALLET_TRANSFER
State.CREATE_CASE_CONFIRM_TRANSFER → CaseState.CREATE_CASE_CONFIRM_TRANSFER
State.CREATE_CASE_ASK_REWARD → CaseState.CREATE_CASE_ASK_REWARD
State.WALLET_MENU → CaseState.WALLET_MENU
State.WAITING_FOR_MOBILE → CaseState.WAITING_FOR_MOBILE
State.CREATE_WALLET → CaseState.CREATE_WALLET
State.SELECT_WALLET → CaseState.SELECT_WALLET
State.ADVERTISER_CONFIRMATION → CaseState.ADVERTISER_CONFIRMATION
State.MOBILE_VERIFICATION → CaseState.MOBILE_VERIFICATION
State.SETTINGS_MENU → CaseState.SETTINGS_MENU
State.MOBILE_MANAGEMENT → CaseState.MOBILE_MANAGEMENT
State.HISTORY_MENU → CaseState.HISTORY_MENU
State.ENTER_NUMBER → CaseState.ENTER_NUMBER
State.VERIFY_OTP → CaseState.VERIFY_OTP
State.VIEW_HISTORY → CaseState.VIEW_HISTORY
State.DELETE_WALLET → CaseState.DELETE_WALLET
State.SHOW_ADDRESS → CaseState.SHOW_ADDRESS
State.HANDLER_END → CaseState.HANDLER_END
```

### 3. Update Conversation Handlers

**Old:**
```python
start_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        State.LANGUAGE_SELECTED: [...],
        State.CHOOSE_COUNTRY: [...],
        State.WALLETS.WALLET_MENU: [...],
    },
    # ...
)
```

**New:**
```python
start_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        StartState.LANGUAGE_SELECTED: [...],
        StartState.CHOOSE_COUNTRY: [...],
        WalletState.WALLET_MENU: [...],
    },
    # ...
)
```

### 4. Update Function Parameters

If your handler functions use state constants as parameters:

**Old:**
```python
def some_handler(update, context):
    context.user_data['state'] = State.CHOOSE_COUNTRY
    return State.CHOOSE_COUNTRY
```

**New:**
```python
def some_handler(update, context):
    context.user_data['state'] = StartState.CHOOSE_COUNTRY
    return StartState.CHOOSE_COUNTRY
```

## Backward Compatibility

The old `State` class is still available in `constants.py` for backward compatibility. You can gradually migrate your code without breaking existing functionality.

## Benefits of Migration

1. **Better Code Organization**: States are grouped by functionality
2. **Improved Readability**: Clear which states belong to which command
3. **Easier Maintenance**: Changes to one command's states don't affect others
4. **Better IDE Support**: Autocomplete and type checking
5. **Modularity**: Each command can manage its own states independently

## Testing Migration

After migration, test your bot to ensure:
1. All commands work as expected
2. State transitions are correct
3. No import errors occur
4. All handlers respond properly

## Need Help?

If you encounter issues during migration:
1. Check the import statements
2. Verify state names match exactly
3. Ensure all required state classes are imported
4. Test each command individually