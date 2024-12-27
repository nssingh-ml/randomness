import math
import numpy as np

def gap_test(data, symbol=1, max_gap=10):
    """
    Implements the Gap Test for randomness.

    Parameters:
        data (list): Sequence of symbols (e.g., binary values or integers) to test.
        symbol (int): The symbol to evaluate gaps between (e.g., 0 or 1 in a binary sequence).
        max_gap (int): Maximum gap size to consider.

    Returns:
        Tuple: (p_value, result), where p_value is the calculated p-value, and result is "Random" or "Non-Random".
    """
    gaps = []
    current_gap = 0
    data  = list(map(int, data))
    # Collect gaps between occurrences of the specified symbol
    for value in data:
        if value == symbol:
            if current_gap > 0:
                gaps.append(current_gap)
            current_gap = 0
        else:
            current_gap += 1

    if not gaps:
        raise ValueError("No gaps found for the given symbol in the data.")

    # Count gaps by size
    gap_counts = [gaps.count(i) for i in range(max_gap + 1)]

    # Total number of gaps
    total_gaps = sum(gap_counts)

    # Expected frequencies under uniform randomness
    expected_counts = [total_gaps * ((1 - 0.5) ** gap) * 0.5 for gap in range(max_gap + 1)]

    # Chi-square test statistic
    chi_square = sum((obs - exp) ** 2 / exp for obs, exp in zip(gap_counts, expected_counts) if exp > 0)

    # Degrees of freedom
    degrees_of_freedom = max_gap

    # Calculate p-value using the chi-square distribution
    p_value = 1 - math.gamma(degrees_of_freedom / 2) * math.exp(-chi_square / 2)

    # Determine randomness based on p-value
    result = "Random" if p_value > 0.01 else "Non-Random"

    return p_value, result

# Example usage
def example_gap_test():
    """Example test to check Gap Test functionality."""
    # Generate random binary test data
    rng = np.random.default_rng()
    test_data = rng.choice([0, 1], size=1000).tolist()  # Generate binary sequence of 0s and 1s

    try:
        symbol = 1  # Evaluate gaps between occurrences of 1
        max_gap = 10  # Consider gaps up to size 10
        p_value, result = gap_test(test_data, symbol, max_gap)
        print(f"Gap Test: P-Value = {p_value}, Result = {result}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    example_gap_test()
