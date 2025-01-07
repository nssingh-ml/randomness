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
    # print("variance",variance, num_symbols,n,((num_symbols - 1) / num_symbols) ** n)

    # Ensure variance is positive
    if variance <= 0:
        print("Variance is non-positive. Cannot perform the test.")
        # raise ValueError("Variance is non-positive. Cannot perform the test.")
        return -1,"Nob-Random"

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
    bit_stream = "01010110100000010001001011100000101010000010110110011011100110000111010001010011110000110000010111001101000101100010000011111111111000001011010011010110101101111100110111000100001011011111100110001101010100111101111011111011010111001011111000111010000001111111100010011111110110101101110111000000111100111101101111101001000100001000110001100001010001110011100111011001100111101101001001111001110111101001111111110000011101001101101000011001010111010110110011000011001010110011010001110011001100010110011001011001011111111000001111011101111000000101100000000011001110100011100100101001001101100100101010110000010101110001011011101111100100000000010110000100111000100110011001011100001110000011001010010000010010100010010011101000101110010100110100001000001010111101011111010000110111011001001101111110011001110001000100000000111000111011101011000101101111010111000000101111110101111000101101001111001010000101000001001111100100010110101011101101111100010001001011000100101010110001111101110111101000100011101110011011010010001000111100001111011010011100100111110010111010110101100110111010101011110011101110001000101100011101110001000011001100011010101000001011010000111001101010011111110100011011011010011101011100011101111011110110100101110010100010001101100010101010010001111010010110001100101011101000101110001101010010011000100100100111011100000100001010110111110110001000101000101011000111101001100001011100010000000111011010011010111100000110010100010001010111100011111001100110110100001010011110110100000100100011011010110100010001011011010001000100011000001111000010101001010001111100100000010011101100000101111010111110100111010011111101100110111000000101111011011011000010011011101010111011111100110011000000101100001111001110101101100001000010100011110111011011100101000100100100000010101011001010001011001111100001101111100111001011101011100100000110110010111101010010011100111110001011000011000011011000101111110111000110100110111010000101101111011001000100101010011101000011011000001100101010111000111111000010000111010000010101000110000100111000011011000010101111011001110000010100001001101111100010110110101100010101001100011010101101110110010110100110000110110000010011011000111011101110000010101000001010011001111111111101001011111111011011111001001010001010110011000001100001111011101011110100111010110100001000111000001101110001001001011000110001110101110010111101001001010000101010111010110101000000110110101010011010110010110001011001101011001011101010010001000011011001001010001100100110011110001001010010110100000001111000101100001001010110010110100100101001011011001110111000000111111000001100010111100101011011001011001011010010101000000110000110010011011101111001111011100000011110101101111011111000001011011000000110110100001100011110000001010111101100011101011011010011010110000111000101010101101111001001111001001000111111010011010010011010101111111110010111111001100011110100010001100110011100000000010111000011100010100100010110011000100010011111110101010101001111101101010000100010001101111110100101000011001110111010001101001111100101111010110100100110011010110101110100111101011111101001000011110100111011010100000111111011101101111000010110100011011110011111000000"


    try:
        num_symbols = 2  # Number of distinct symbols
        # print(test_data)
        p_value, result = coupon_collector_test(bit_stream, num_symbols)
        print(f"Coupon Collector's Test: P-Value = {p_value}, Result = {result}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    example_coupon_collector_test()
