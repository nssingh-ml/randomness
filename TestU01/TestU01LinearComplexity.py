import math
import numpy as np

def linear_complexity_test(data, block_size=500):
    """
    Implements the Linear Complexity Test for randomness.

    Parameters:
        data (list): Sequence of binary values (0s and 1s).
        block_size (int): Size of each block to analyze.

    Returns:
        Tuple: (p_value, result), where p_value is the calculated p-value, and result is "Random" or "Non-Random".
    """
    n = len(data)

    if block_size <= 0 or n < block_size:
        raise ValueError("Block size must be greater than 0 and less than or equal to the data length.")

    # Split data into blocks of size `block_size`
    num_blocks = n // block_size
    blocks = [data[i * block_size:(i + 1) * block_size] for i in range(num_blocks)]

    # Function to calculate linear complexity using the Berlekamp-Massey algorithm
    def berlekamp_massey_algorithm(sequence):
        n = len(sequence)
        c = [0] * n
        b = [0] * n
        c[0], b[0] = 1, 1
        l, m, d = 0, -1, 0

        for i in range(n):
            d = sequence[i]
            for j in range(1, l + 1):
                d ^= c[j] * sequence[i - j]

            if d == 1:
                t = c[:]
                for j in range(i - m, n):
                    if j < len(b):
                        c[j] ^= b[j - (i - m)]
                if l <= i // 2:
                    l = i + 1 - l
                    m = i
                    b = t
        return l

    # Calculate linear complexities for all blocks
    complexities = [berlekamp_massey_algorithm(block) for block in blocks]

    # Expected mean and variance for the linear complexity
    mean = block_size / 2.0 + (9 + (-1) ** block_size) / 36.0 - 1 / 3.0
    variance = block_size * (1 - (1 / 3.0) * (2 ** (-2 * block_size)))

    # Compute test statistic
    t_values = [(lc - mean) / math.sqrt(variance) for lc in complexities]
    chi_square = sum(t ** 2 for t in t_values)

    # Degrees of freedom
    degrees_of_freedom = num_blocks

    # Calculate p-value using the chi-square distribution
    from scipy.stats import chi2
    p_value = chi2.sf(chi_square, degrees_of_freedom)

    # Determine randomness based on p-value
    result = "Random" if p_value > 0.01 else "Non-Random"

    return p_value, result

# Example usage
def example_linear_complexity_test():
    """Example test to check Linear Complexity Test functionality."""
    rng = np.random.default_rng()
    test_data = rng.choice([0, 1], size=10000).tolist()  # Generate binary sequence of 0s and 1s

    try:
        block_size = 500  # Size of each block
        p_value, result = linear_complexity_test(test_data, block_size)
        print(f"Linear Complexity Test: P-Value = {p_value}, Result = {result}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    example_linear_complexity_test()
