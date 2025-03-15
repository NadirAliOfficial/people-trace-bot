from tronpy import Tron
from tronpy.keys import PrivateKey

# # Connect to Shasta Testnet
client = Tron(network="shasta")

# # Generate a new wallet
# wallet = client.generate_address()
# print("Wallet Address: %s" % wallet["base58check_address"])
# print("Private Key: %s" % wallet["private_key"])


print(
    f"Sender Private Address: {"d0d489047b8262d3d489c8dcdaaad9079500825918661c31d1370052d4f93524"}"
)

print(f"Receiver Address: {'TT38SuQptmHEo37BxGwDnkn8jLNjEum1G6'}")


# Your funded test wallet details:
# Replace with your private key (hex string, without a '0x' prefix) from your test wallet.
sender_private_key = PrivateKey(
    bytes.fromhex("2f60abed403a9a68426fe106774dd8f19f91ed1e1b8534d12a970c0911ffdeb3")
)
sender_address = sender_private_key.public_key.to_base58check_address()

# Destination address for the transaction (another test wallet)
destination_address = "TFnwSQg6gZcgGCQdLGayp9KWRGid3dndKR"

# Define the transfer amount in Sun (1 TRX = 1,000,000 Sun)
amount_in_sun = 1_000_000

# Build the transfer transaction
txn = client.trx.transfer(sender_address, destination_address, amount_in_sun).build()

# Sign the transaction with the sender's private key
signed_txn = txn.sign(sender_private_key)

# Broadcast the transaction to the network
result = signed_txn.broadcast()

print("Transaction broadcast result:")
print(result)
