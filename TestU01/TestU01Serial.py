import math
import numpy as np
from collections import Counter

def serial_test(data, block_size=3):
    """
    Implements the Serial Test for randomness.

    Parameters:
        data (list): Sequence of binary values (0s and 1s).
        block_size (int): Size of each block to analyze.

    Returns:
        Tuple: (p_value, result), where p_value is the calculated p-value, and result is "Random" or "Non-Random".
    """
    data  = list(map(int, data))
    n = len(data)

    if block_size <= 0 or n < block_size:
        raise ValueError("Block size must be greater than 0 and less than or equal to the data length.")

    # Count frequencies of all overlapping patterns of length `block_size`
    pattern_counts = Counter(
        tuple(data[i:i + block_size]) for i in range(n - block_size + 1)
    )

    # Total possible patterns of length `block_size`
    total_patterns = 2 ** block_size

    # Frequency of each pattern in data
    observed_counts = [pattern_counts.get(tuple(bin(i)[2:].zfill(block_size)), 0) for i in range(total_patterns)]

    # Expected frequency under uniform randomness
    expected_count = (n - block_size + 1) / total_patterns

    # Chi-square statistic
    chi_square = sum((obs - expected_count) ** 2 / expected_count for obs in observed_counts if expected_count > 0)

    # Degrees of freedom
    degrees_of_freedom = total_patterns - 1

    # Calculate p-value using the chi-square distribution
    from scipy.stats import chi2
    p_value = chi2.sf(chi_square, degrees_of_freedom)

    # Determine randomness based on p-value
    result = "Random" if p_value > 0.01 else "Non-Random"
    print(p_value, result)

    return p_value, result

# Example usage
def example_serial_test():
    """Example test to check Serial Test functionality."""
    rng = np.random.default_rng()
    test_data = rng.choice([0, 1], size=10000).tolist()  # Generate binary sequence of 0s and 1s

    try:
        block_size = 3  # Size of each pattern to evaluate
        p_value, result = serial_test(test_data, block_size)
        print(f"Serial Test: P-Value = {p_value}, Result = {result}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    example_serial_test()
