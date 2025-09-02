# States Structure

This directory contains separated state constants for different Telegram bot commands. The states have been organized by functionality to improve code maintainability and readability.

## Structure

### `start_states.py`
Contains all states related to the main start command and case creation flow:
- Language selection
- Country/province/city selection
- Case creation steps
- Finder functionality
- General conversation flow

### `wallet_states.py`
Contains states for wallet management:
- Wallet menu navigation
- SOL/USDT wallet details
- Wallet creation/deletion
- Private key management
- Transaction history

### `settings_states.py`
Contains states for user settings:
- Settings menu navigation
- Mobile number management
- TAC verification
- Language settings

### `finder_states.py`
Contains states specific to finder functionality:
- Finder case creation
- Mobile verification
- Country/province selection
- Complaint viewing

### `stats_states.py`
Contains states for statistics and reporting:
- Stats menu navigation
- Unsolved cases by country
- Local statistics
- Personal case history

### `listing_states.py`
Contains states for case listing and management:
- Case details viewing
- Case editing
- Reward management
- Extend reward flow

### `case_states.py`
Contains general case-related states:
- Case creation
- Transfer confirmations
- Mobile verification
- General case management

## Usage

### Importing States
```python
from states import StartState, WalletState, SettingsState, FinderState
from states import StatsState, ListingState, CaseState
```

### Using States in Conversation Handlers
```python
# Instead of State.CHOOSE_COUNTRY
StartState.CHOOSE_COUNTRY

# Instead of State.WALLETS.WALLET_MENU
WalletState.WALLET_MENU

# Instead of State.SETTINGS.SETTINGS_MENU
SettingsState.SETTINGS_MENU
```

### Backward Compatibility
The old `State` class is still available in `constants.py` for backward compatibility, but it's recommended to use the new separated state classes for new code.

## Benefits

1. **Better Organization**: States are grouped by functionality
2. **Easier Maintenance**: Changes to one command's states don't affect others
3. **Improved Readability**: Clear which states belong to which command
4. **Type Safety**: Better IDE support and autocomplete
5. **Modularity**: Each command can manage its own states independently

## Migration

To migrate existing code:

1. Replace `State.SOME_STATE` with the appropriate state class (e.g., `StartState.SOME_STATE`)
2. Update imports to include the specific state classes needed
3. The old `State` class will continue to work for existing code

## Example

```python
# Old way
from constants import State

states = {
    State.CHOOSE_COUNTRY: [...],
    State.WALLETS.WALLET_MENU: [...],
    State.SETTINGS.SETTINGS_MENU: [...],
}

# New way
from states import StartState, WalletState, SettingsState

states = {
    StartState.CHOOSE_COUNTRY: [...],
    WalletState.WALLET_MENU: [...],
    SettingsState.SETTINGS_MENU: [...],
}
```