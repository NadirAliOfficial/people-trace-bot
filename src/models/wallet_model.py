import enum
from typing import Optional
from beanie import Document
from solana.rpc.api import Client
from solders.pubkey import Pubkey
from solana.rpc.types import TokenAccountOpts


class WalletType(enum.Enum):
    SOL = "SOL"
    USDT = "USDT"


class Wallet(Document):
    public_key: str
    private_key: str
    wallet_type: str
    name: str
    user_id: int
    deleted: bool = False

    class Settings:
        name = "wallets"
