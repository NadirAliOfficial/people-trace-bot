import os
import base58
from solders.keypair import Keypair
from solana.rpc.api import Client
from solders.pubkey import Pubkey
from telegram import Update
from tronpy import Tron
from tronpy.keys import PrivateKey
from solders.transaction import Transaction
from solders.system_program import transfer
from solana.rpc.types import TxOpts
from telegram.ext import (
    ContextTypes,
)
from config.config_manager import TRON_CLIENT_NETWORK
from constant.language_constant import  user_data_store
from spl.token.client import Token

from constants import WALLETS_DIR

# Initialize Solana client
try:
    SOLANA_NETWORK = "https://api.devnet.solana.com"
    client = Client(SOLANA_NETWORK)
    usdt_client =  Tron(network=TRON_CLIENT_NETWORK)  # Use 'mainnet' for live transactions

except ImportError:
    client = None
    


async def transfer_solana_funds(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    from_wallet: dict,
    to_pubkey: str,
    amount: float,
):
    """Transfer funds from one wallet to another."""
    user_id = update.effective_user.id

    # Extract public key and secret key from wallet
    from_public_key = Pubkey.from_string(from_wallet["public_key"])
    secret_key = base58.b58decode(from_wallet["secret_key"])

    # Create the transaction
    transaction = Transaction()
    transfer_ix = transfer(
        from_pubkey=from_public_key,
        to_pubkey=Pubkey.from_string(to_pubkey),
        lamports=int(amount * 1e9),  # Convert SOL to lamports (1 SOL = 1e9 lamports)
    )
    transaction.add(transfer_ix)

    # Sign the transaction
    try:
        keypair = Keypair.from_secret_key(secret_key)
    except Exception as e:
        await update.message.reply_text(
            f"An error occurred while creating keypair: {str(e)}"
        )
        return
    transaction.sign(keypair)

    # Send the transaction to the network
    try:
        tx_response = client.send_transaction(
            transaction, keypair, opts=TxOpts(skip_preflight=True)
        )
        if tx_response["result"]:
            await update.message.reply_text(
                f"Successfully transferred {amount} SOL to {to_pubkey}!"
            )
        else:
            await update.message.reply_text(f"Failed to transfer {amount} SOL.")
    except Exception as e:
        await update.message.reply_text(
            f"An error occurred during the transfer: {str(e)}"
        )


def create_sol_wallet(wallet_name):
    """Create a SOL wallet with Keypair, store it as JSON, and return its details."""
    if not client:
        return None
    try:
        keypair = Keypair()
        public_key = str(keypair.pubkey())
        secret_key = base58.b58encode(bytes(keypair.to_bytes_array())).decode("utf-8")

        wallet = {
            "name": wallet_name,
            "public_key": public_key,
            "secret_key": secret_key,
        }

        # Fetch balance
        balance_response = client.get_balance(Pubkey.from_string(public_key))
        balance_lamports = balance_response.value if balance_response else 0
        balance_sol = balance_lamports / 1e9
        wallet["balance_sol"] = balance_sol
        return wallet

    except Exception as e:
        print(f"Error creating wallet: {e}")
        return None


from tronpy import Tron
from tronpy.keys import PrivateKey

# Initialize Tron Client
tron = Tron(network="mainnet")  # Use "shasta" for testnet



def load_user_wallet(user_id):
    """Load wallet info from user_data_store or from file if needed."""
    user_wallet = user_data_store[user_id].get("wallet")
    if not user_wallet:
        return None
    # Optionally re-check balance from the chain
    if client:
        pubkey = user_wallet.get("public_key")
        if pubkey:
            balance_response = client.get_balance(Pubkey.from_string(pubkey))
            balance_lamports = balance_response.value if balance_response else 0
            balance_sol = balance_lamports / 1e9
            user_wallet["balance_sol"] = balance_sol
    return user_wallet


def delete_user_wallet(user_id):
    """Remove the user's wallet from memory and optionally from disk."""
    user_wallet = user_data_store[user_id].get("wallet")
    if not user_wallet:
        return False
    # Delete from disk if you want
    pubkey = user_wallet.get("public_key")
    if pubkey:
        wallet_filename = os.path.join(WALLETS_DIR, f"{pubkey}.json")
        if os.path.exists(wallet_filename):
            os.remove(wallet_filename)
    user_data_store[user_id]["wallet"] = None
    return True
