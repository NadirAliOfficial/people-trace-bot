from tronpy import Tron
from tronpy.keys import PrivateKey
from tronpy.contract import Contract


class TronWallet:
    """
    Service for managing TRON wallets and transactions, including USDT (TRC20) operations.
    """

    # USDT TRC20 Contract Address (Mainnet)
    USDT_CONTRACT = "TXLAQ63Xg1NAzckPwKHvzw7CSEmLMEqcdj"

    # Initialize Tron Client
    client = Tron(network="shasta")  # Use "shasta" for testnet

    @staticmethod
    def create_wallet(wallet_name):
        """
        Creates a new TRON Wallet and returns its details.
        """
        private_key = PrivateKey.random()
        address = private_key.public_key.to_base58check_address()

        return {
            "private_key": private_key.hex(),  # Keep this secret!
            "public_key": address,
            "name": wallet_name,
        }

    @staticmethod
    def get_trx_balance(address):
        """
        Fetches the TRX balance of a TRON wallet.
        """
        try:
            return TronWallet.client.get_account_balance(address)  # Balance is in TRX
        except Exception:
            return 0  # Wallet may be new and unfunded

    @staticmethod
    async def get_usdt_balance(address):
        try:
            balance = TronWallet.client.get_account_balance(address)
            # real_balance = balance / 10**6  # Convert from SUN to TRX
            # print(f"Balance: {real_balance} TRX")
            # return real_balance  # Balance is in TRX
            return balance
        except Exception:
            return 0  # Wallet may be new and unfunded

    @staticmethod
    def transfer_trx(sender_private_key, recipient_address, amount_in_trx):
        """
        Transfers TRX from one wallet to another.
        """
        try:
            sender_private_key = PrivateKey(bytes.fromhex(sender_private_key))
            sender_address = sender_private_key.public_key.to_base58check_address()

            # Convert TRX to Sun (1 TRX = 1,000,000 Sun)
            amount_in_sun = int(amount_in_trx * 1_000_000)

            txn = (
                TronWallet.client.trx.transfer(
                    sender_address, recipient_address, amount_in_sun
                )
                .build()
                .sign(sender_private_key)
            )

            return txn.broadcast()
        except Exception as e:
            print(f"Error sending TRX: {e}")
            return None

    @staticmethod
    async def transfer_usdt(sender_private_key, recipient_address, amount_in_usdt):
        """
        Transfers USDT from one wallet to another.
        """
        try:
            print(
                f"DEBUG - 1: {sender_private_key} {recipient_address} {amount_in_usdt}"
            )

            sender_private_key = PrivateKey(bytes.fromhex(sender_private_key))
            sender_address = sender_private_key.public_key.to_base58check_address()

            destination_address = recipient_address

            print(
                f"DEBUG - 2: {sender_private_key} {recipient_address} {amount_in_usdt}"
            )

            amount_in_sun = int(1_000_000 * amount_in_usdt)

            print(
                f"DEBUG - 3: {sender_private_key} {recipient_address} {amount_in_usdt}"
            )

            # Convert the USDT amount to SUN (6 decimal places)
            txn = TronWallet.client.trx.transfer(
                sender_address, destination_address, amount_in_sun
            ).build()

            print(
                f"DEBUG - 4: {sender_private_key} {recipient_address} {amount_in_usdt}"
            )

            signed_txn = txn.sign(sender_private_key)

            print(f"DEBUG - 5: {signed_txn}")

            result = signed_txn.broadcast()

            print(f"DEBUG - 6: {result}")

            return result
        except Exception as e:
            print(f"Error sending USDT: {e}")
            return None

    def create_usdt_wallet(wallet_name):
        """
        Creates a new USDT wallet and returns its details.
        """
        private_key = PrivateKey.random()
        address = private_key.public_key.to_base58check_address()

        try:
            balance = TronWallet.get_usdt_balance(address)
        except Exception as e:
            print(f"Error creating wallet: {e}")
            balance = 0

        return {
            "private_key": private_key.hex(),  # Keep this secret!
            "public_key": address,
            "name": wallet_name,
            "balance": balance,
        }
