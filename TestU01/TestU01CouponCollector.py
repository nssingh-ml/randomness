import math
import numpy as np

def coupon_collector_test(data, num_symbols=2):
    """
    Implements the Coupon Collector's Test for randomness.

    Parameters:
        data (list): Sequence of integers to test.
        num_symbols (int): Total number of distinct symbols expected in the data.

    Returns:
        Tuple: (p_value, result), where p_value is the calculated p-value, and result is "Random" or "Non-Random".
    """
    data  = list(map(int, data))
    n = len(data)
    if num_symbols <= 1:
        raise ValueError("Number of symbols must be greater than 1.")

    # Count occurrences of each symbol
    symbol_counts = [data.count(symbol) for symbol in range(num_symbols)]

    # Check if all symbols are represented
    if any(count == 0 for count in symbol_counts):
        raise ValueError("Not all symbols are present in the data.")

    # Calculate observed and expected values
    observed = sum(count > 0 for count in symbol_counts)
    expected = num_symbols * (1 - ((num_symbols - 1) / num_symbols) ** n)

    # Calculate variance
    variance = num_symbols * (1 - ((num_symbols - 1) / num_symbols) ** n) * ((num_symbols - 1) / num_symbols) ** n

    # Ensure variance is positive
    if variance <= 0:
        raise ValueError("Variance is non-positive. Cannot perform the test.")

    # Calculate z-score
    z = (observed - expected) / math.sqrt(variance)

    # Convert z-score to p-value
    p_value = 2 * (1 - math.erf(abs(z) / math.sqrt(2)))

    # Determine randomness based on p-value
    result = "Random" if p_value > 0.01 else "Non-Random"

    return p_value, result

# Example usage
def example_coupon_collector_test():
    """Example test to check Coupon Collector's Test functionality."""
    # Generate random test data
    rng = np.random.default_rng()
    test_data = rng.integers(0, 10, size=1000).tolist()  # Generate sequence of integers with symbols in range [0, 10)
    bit_stream = "110010111011011001010101110010100111001011100101011011001011001111100101110110110010101011100101001110010111001010110110010110011111001011101101100101010111001010011100101110010101101100101100111110010111011011001010101110010100111001011100101011011001011001111100101110110110010101011100101001110010111001010110110010110011111001011101101100101010111001010011100101110010101101100101100111110010111011011001010101110010100111001011100101011011001011001111100101110110110010101011100101001110010111001010110110010110011111001011101101100101010111001010011100101110010101101100101100111"


    try:
        num_symbols = 2  # Number of distinct symbols
        # print(test_data)
        p_value, result = coupon_collector_test(bit_stream, num_symbols)
        print(f"Coupon Collector's Test: P-Value = {p_value}, Result = {result}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    example_coupon_collector_test()
