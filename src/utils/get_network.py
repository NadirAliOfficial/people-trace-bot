def get_network(wallet_type: str) -> str:
    wallet_type = wallet_type.upper()
    if wallet_type == "USDT":
        return "TRC20 (Tron Network)"
    elif wallet_type == "SOL":
        return "Solana Network"
    elif wallet_type == "ETH":
        return "ERC20 (Ethereum Network)"
    # Add more cases as needed
    else:
        return "Unknown Network"
