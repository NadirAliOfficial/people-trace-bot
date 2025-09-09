def calculate_reward_with_tax(reward: float, tax_rate: float = 0.05) -> float:
    """Calculate the reward after applying a 5% tax."""
    tax = reward * tax_rate
    return reward - tax
