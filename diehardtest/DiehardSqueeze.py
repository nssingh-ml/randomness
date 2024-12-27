import numpy as np
from scipy.stats import chisquare

class DiehardSqueezeTest:
    @staticmethod
    def run_test(data, num_trials=100000):
        """
        Runs the Diehard Squeeze Test.

        :param data: Input data as binary string, bytes, or list of integers.
        :param num_trials: Number of trials to perform (default: 100,000).
        :return: Tuple (p_value, result), where p_value is the calculated p-value, and result is "Random" or "Non-Random".
        """
        try:
            # Convert input data to numerical values in the range [0, 1)
            numerical_data = DiehardSqueezeTest._prepare_numerical_data(data)

            # Ensure enough data for the required number of trials
            if len(numerical_data) < num_trials:
                raise ValueError(f"Insufficient data: {len(numerical_data)} values provided, but {num_trials} needed.")

            results = []

            for trial in range(num_trials):
                k = 2 ** 31
                count = 0

                while k > 1:
                    count += 1
                    k = np.ceil(k * numerical_data[trial % len(numerical_data)])

                results.append(count)

            # Count occurrences for chi-square test
            counts = [sum(1 for x in results if x == j) for j in range(6, 48)]
            counts.append(sum(1 for x in results if x >= 48))

            # Expected frequencies for each bin
            expected = [num_trials * (np.exp(-j) - np.exp(-(j + 1))) for j in range(6, 48)]
            expected.append(num_trials * np.exp(-48))

            # Perform chi-square test
            chi_stat, p_value = chisquare(counts, expected)

            # Determine randomness based on p-value
            result = "Random" if p_value > 0.01 else "Non-Random"
            return p_value, result

        except Exception as e:
            raise ValueError(f"Error in Squeeze Test: {e}")

    @staticmethod
    def _prepare_numerical_data(data):
        """
        Converts input data into a list of floats in the range [0, 1).

        :param data: Input data as binary string, bytes, or list of integers.
        :return: List of floats in [0, 1).
        """
        try:
            if isinstance(data, str):
                numerical_data = [ord(char) / 256 for char in data]
            elif isinstance(data, (bytes, bytearray)):
                numerical_data = [byte / 256 for byte in data]
            elif isinstance(data, list):
                numerical_data = [num / 256 for num in data]
            else:
                raise ValueError("Unsupported data type. Provide binary string, bytes, or list of integers.")
            return numerical_data
        except Exception as e:
            raise ValueError(f"Error preparing numerical data: {e}")

# Example usage
if __name__ == "__main__":
    # Generate random test data
    rng = np.random.default_rng(seed=42)
    test_data = rng.integers(0, 256, size=100000, dtype=int).tolist()  # Sufficient data for 100,000 trials

    try:
        p_value, result = DiehardSqueezeTest.run_test(test_data)
        print(f"Squeeze Test: P-Value = {p_value}, Result = {result}")
    except Exception as e:
        print(e)
