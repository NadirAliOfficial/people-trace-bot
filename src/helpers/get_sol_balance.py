from solana.rpc.async_api import AsyncClient  # Use AsyncClient instead of Client
from solders.pubkey import Pubkey
import asyncio
from constants import solana_client


async def get_sol_balance(
    public_key_str: str,
) -> float:
    """
    Get the balance of a Solana account in SOL.

    :param public_key_str: The public key of the Solana account as a string.
    :param rpc_url: The RPC URL to connect to the Solana network (default is mainnet).
    :return: The balance of the account in SOL.
    """

    public_key = Pubkey.from_string(public_key_str)

    response = await solana_client.get_balance(public_key)

    if response.value is None:
        raise ValueError(
            "Failed to retrieve balance. Check the public key and RPC URL."
        )

    balance_sol = response.value / 1e9

    return balance_sol
