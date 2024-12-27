import math
import numpy as np

def longest_run_test(data, symbol=1, block_size=10):
    """
    Implements the Longest Run Test for randomness.

    Parameters:
        data (list): Sequence of binary values (0s and 1s).
        symbol (int): The symbol to evaluate (e.g., 0 or 1).
        block_size (int): Size of each block to analyze.

    Returns:
        Tuple: (p_value, result), where p_value is the calculated p-value, and result is "Random" or "Non-Random".
    """
    n = len(data)
    if block_size <= 0 or n < block_size:
        raise ValueError("Block size must be greater than 0 and less than or equal to the data length.")

    # Split data into blocks
    num_blocks = n // block_size
    blocks = [data[i * block_size:(i + 1) * block_size] for i in range(num_blocks)]

    # Find the longest run of the specified symbol in each block
    longest_runs = []
    for block in blocks:
        max_run = 0
        current_run = 0
        for bit in block:
            if bit == symbol:
                current_run += 1
                max_run = max(max_run, current_run)
            else:
                current_run = 0
        longest_runs.append(max_run)

    # Count occurrences of each longest run length
    max_possible_run = block_size
    run_counts = [longest_runs.count(i) for i in range(max_possible_run + 1)]

    # Expected probabilities under randomness (approximation for small block sizes)
    expected_probabilities = [(1 / (2 ** (i + 1))) for i in range(max_possible_run)]
    expected_probabilities[-1] += 1 / (2 ** max_possible_run)  # Adjust for the tail

    # Expected frequencies
    expected_frequencies = [p * num_blocks for p in expected_probabilities]

    # Chi-square statistic
    chi_square = sum(
        (obs - exp) ** 2 / exp for obs, exp in zip(run_counts, expected_frequencies) if exp > 0
    )

    # Degrees of freedom
    degrees_of_freedom = len(expected_frequencies) - 1

    # Calculate p-value
    p_value = 1 - math.gamma(degrees_of_freedom / 2) * math.exp(-chi_square / 2)

    # Determine randomness based on p-value
    result = "Random" if p_value > 0.01 else "Non-Random"

    return p_value, result

# Example usage
def example_longest_run_test():
    """Example test to check Longest Run Test functionality."""
    # Generate random binary test data
    rng = np.random.default_rng()
    test_data = rng.choice([0, 1], size=1000).tolist()  # Generate binary sequence of 0s and 1s

    try:
        symbol = 1  # Symbol to evaluate (e.g., 1)
        block_size = 10  # Size of each block
        p_value, result = longest_run_test(test_data, symbol, block_size)
        print(f"Longest Run Test: P-Value = {p_value}, Result = {result}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    example_longest_run_test()
