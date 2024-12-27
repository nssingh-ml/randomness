import math
import numpy as np

def runs_test(data):
    """
    Implements the Runs Test for randomness.

    Parameters:
        data (list): Binary sequence to test (list of 0s and 1s).

    Returns:
        Tuple: (p_value, result), where p_value is the calculated p-value, and result is "Random" or "Non-Random".
    """
    data  = list(map(int, data))
    n = len(data)
    if n < 2:
        raise ValueError("Data must contain at least two elements.")

    # Calculate the number of runs
    runs = 1
    for i in range(1, n):
        if data[i] != data[i - 1]:
            runs += 1

    # Count the number of 0s and 1s
    n0 = data.count(0)
    n1 = data.count(1)

    if n0 == 0 or n1 == 0:
        raise ValueError("Data must contain both 0s and 1s.")

    # Calculate the expected number of runs
    expected_runs = ((2 * n0 * n1) / n) + 1

    # Calculate the variance of the number of runs
    variance_runs = ((2 * n0 * n1) * (2 * n0 * n1 - n)) / (n ** 2 * (n - 1))

    # Calculate the z-score
    z = (runs - expected_runs) / math.sqrt(variance_runs)

    # Convert the z-score to a two-sided p-value
    p_value = 2 * (1 - math.erf(abs(z) / math.sqrt(2)))

    # Determine randomness based on p-value
    result = "Random" if p_value > 0.01 else "Non-Random"

    return p_value, result

# Example usage
def example_test():
    """Example test to check Runs Test functionality."""
    # Generate random test data
    rng = np.random.default_rng()
    test_data = rng.choice([0, 1], size=1000).tolist()  # Generate binary sequence of 0s and 1s

    try:
        # print(type(test_data))
        p_value, result = runs_test(test_data)
        print(f"Runs Test: P-Value = {p_value}, Result = {result}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    example_test()
