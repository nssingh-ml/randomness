import math
import numpy as np
from collections import Counter

def simp_poker_test(data, hand_size=5):
    """
    Implements the Simple Poker Test for randomness.

    Parameters:
        data (list): Sequence of integers to test.
        hand_size (int): Number of elements in each "hand".

    Returns:
        Tuple: (p_value, result), where p_value is the calculated p-value, and result is "Random" or "Non-Random".
    """
    data  = list(map(int, data))
    n = len(data)
    if n < hand_size:
        raise ValueError("The data length must be greater than or equal to the hand size.")

    # Split data into hands
    num_hands = n // hand_size
    hands = [data[i * hand_size:(i + 1) * hand_size] for i in range(num_hands)]

    # Count unique elements in each hand
    hand_counts = [len(set(hand)) for hand in hands]

    # Count occurrences of each unique count
    count_frequencies = Counter(hand_counts)

    # Total number of hands
    total_hands = num_hands

    # Calculate expected frequencies
    expected_frequencies = {}
    for k in range(1, hand_size + 1):
        expected_frequencies[k] = (
            math.comb(hand_size, k) * math.factorial(k) * (1 / len(set(data))) ** k
        ) * total_hands

    # Calculate chi-square statistic
    chi_square = sum(
        (count_frequencies.get(k, 0) - expected_frequencies[k]) ** 2 / expected_frequencies[k]
        for k in expected_frequencies if expected_frequencies[k] > 0
    )

    # Degrees of freedom
    degrees_of_freedom = len(expected_frequencies) - 1

    # Calculate p-value using chi-square distribution
    p_value = 1 - math.gamma(degrees_of_freedom / 2) * math.exp(-chi_square / 2)

    # Determine randomness based on p-value
    result = "Random" if p_value > 0.01 else "Non-Random"

    return p_value, result

# Example usage
def example_simp_poker_test():
    """Example test to check Simple Poker Test functionality."""
    # Generate random test data
    rng = np.random.default_rng()
    test_data = rng.integers(0, 100, size=1000).tolist()  # Generate sequence of integers in the range [0, 100)

    try:
        hand_size = 5  # Size of each "hand"
        p_value, result = simp_poker_test(test_data, hand_size)
        print(f"Simple Poker Test: P-Value = {p_value}, Result = {result}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    example_simp_poker_test()
