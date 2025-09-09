from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc.api import Client
from solders.system_program import transfer, TransferParams
from solders.transaction import Transaction
from solders.message import Message

# Create a Solana RPC client
client = Client("https://api.devnet.solana.com")

# Load the sender's private key
sender = Keypair.from_base58_string(
    "3zGLwBKciRezgUfChoQSLmCeYxv7rrBSGg4tpFUXsPyEfpCqYrWsruBF6d5QTrn4E6MjUziVebmwkpwv3oC3fPoc"
)

# Load the recipient's public key
to_pubkey = Pubkey.from_string("8RjkX9qRpwE3zaXPzvo88veZeCRUKAqanUChEXGhJG9o")

# Create a transfer instruction
instruction = transfer(
    TransferParams(
        from_pubkey=sender.pubkey(),
        to_pubkey=to_pubkey,
        lamports=1_000_000,  # Amount in lamports
    )
)

# Get the latest blockhash
blockhash_response = client.get_latest_blockhash()
recent_blockhash = blockhash_response.value.blockhash

# Create a message and transaction
message = Message(instructions=[instruction], payer=sender.pubkey())
transaction = Transaction(
    from_keypairs=[sender], message=message, recent_blockhash=recent_blockhash
)

# Sign the transaction
transaction.sign([sender], recent_blockhash=recent_blockhash)

# Send the transaction
send_response = client.send_transaction(transaction)
print(f"Transaction sent! Transaction signature: {send_response}")
