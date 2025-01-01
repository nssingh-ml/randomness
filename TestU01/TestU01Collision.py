# Running the updated collision_test code to validate its functionality

import math
import numpy as np
from collections import Counter

def collision_test(data, space_size= 2**16):
    """
    Implements the Collision Test for randomness.

    Parameters:
        data (list): Sequence of integers to test.
        space_size (int): Size of the range from which integers are drawn (e.g., 0 to space_size-1).

    Returns:
        Tuple: (p_value, result), where p_value is the calculated p-value, and result is "Random" or "Non-Random".
    """
    data  = list(map(int, data))
    n = len(data)
    if n < 2:
        raise ValueError("Data must contain at least two elements.")

    if space_size <= 1:
        raise ValueError("Space size must be greater than 1.")

    if n >= space_size:
        raise ValueError("The number of samples (n) must be significantly smaller than the space size.")

    # Map data to the range [0, space_size)
    mapped_data = [x % space_size for x in data]

    # Count collisions
    counter = Counter(mapped_data)
    collisions = sum(count - 1 for count in counter.values() if count > 1)

    # Calculate expected collisions and variance
    expected_collisions = n - space_size + space_size * ((space_size - 1) / space_size) ** n
    variance_collisions = (
        n * (n - 1) / (2 * space_size)  # Approximation for variance of collisions
    )

    # Check for non-positive variance
    if variance_collisions <= 0:
        raise ValueError("Calculated variance is non-positive, cannot compute z-score.")

    # Calculate the z-score
    z = (collisions - expected_collisions) / math.sqrt(variance_collisions)

    # Convert the z-score to a two-sided p-value
    p_value = 2 * (1 - math.erf(abs(z) / math.sqrt(2)))

    # Determine randomness based on p-value
    result = "Random" if p_value > 0.01 else "Non-Random"

    return p_value, result

# Example usage
def example_collision_test():
    """Example test to check Collision Test functionality."""
    # Generate random test data
    rng = np.random.default_rng()
    test_data = rng.integers(0, 10000, size=1000).tolist()  # Generate sequence of integers in the range [0, 10000)

    try:
        # space_size = 10000
        space_size = 2**16
        p_value, result = collision_test(test_data, space_size)
        return f"Collision Test: P-Value = {p_value}, Result = {result}"
    except Exception as e:
        return f"Error: {e}"

# Run the test and display the result
# print(example_collision_test())
