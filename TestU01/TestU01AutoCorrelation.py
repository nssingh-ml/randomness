import math
import numpy as np

def auto_correlation_test(data, lag=5):
    """
    Implements the Auto-Correlation Test for randomness.

    Parameters:
        data (list): Sequence of binary values (0s and 1s).
        lag (int): The lag value for auto-correlation.

    Returns:
        Tuple: (p_value, result), where p_value is the calculated p-value, and result is "Random" or "Non-Random".
    """
    n = len(data)

    if lag <= 0 or lag >= n:
        raise ValueError("Lag must be greater than 0 and less than the length of the data.")

    # Calculate the number of valid overlapping pairs
    valid_pairs = n - lag

    # Compute the auto-correlation
    correlation = sum(data[i] == data[i + lag] for i in range(valid_pairs))

    # Calculate the test statistic
    p_hat = correlation / valid_pairs
    test_statistic = (p_hat - 0.5) * math.sqrt(valid_pairs) / math.sqrt(0.25)

    # Convert the test statistic to a two-sided p-value
    from scipy.stats import norm
    p_value = 2 * (1 - norm.cdf(abs(test_statistic)))

    # Determine randomness based on p-value
    result = "Random" if p_value > 0.01 else "Non-Random"

    return p_value, result

# Example usage
def example_auto_correlation_test():
    """Example test to check Auto-Correlation Test functionality."""
    rng = np.random.default_rng()
    test_data = rng.choice([0, 1], size=10000).tolist()  # Generate binary sequence of 0s and 1s

    try:
        lag = 5  # Lag value for auto-correlation
        p_value, result = auto_correlation_test(test_data, lag)
        print(f"Auto-Correlation Test: P-Value = {p_value}, Result = {result}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    example_auto_correlation_test()
