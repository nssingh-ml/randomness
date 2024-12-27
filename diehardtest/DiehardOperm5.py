import numpy as np
from scipy.stats import chi2

class DiehardOPERM5:
    @staticmethod
    def run_test(data, samples=1000000, overlap=True):
        """
        Runs the Diehard OPERM5 test on the provided data.

        :param data: Input data as binary string, bytes, or list of integers.
        :param samples: Number of 5-permutation samples to use (default: 1,000,000).
        :param overlap: Whether to use overlapping samples (default: True).
        :return: Tuple (p_value, result), where p_value is the calculated p-value, and result is "Random" or "Non-Random".
        """
        try:
            # Convert input to numerical format if necessary
            numerical_data = DiehardOPERM5._prepare_data(data)

            # Ensure enough data for the required samples
            if len(numerical_data) < 5:
                raise ValueError("Insufficient data length. At least 5 integers are required.")

            # Count occurrences of each permutation
            counts = np.zeros(120, dtype=float)
            if overlap:
                for i in range(samples):
                    indices = numerical_data[i % len(numerical_data): i % len(numerical_data) + 5]
                    perm_index = DiehardOPERM5._perm_index(indices)
                    counts[perm_index] += 1
            else:
                for i in range(0, samples * 5, 5):
                    if i + 5 <= len(numerical_data):
                        indices = numerical_data[i:i + 5]
                        perm_index = DiehardOPERM5._perm_index(indices)
                        counts[perm_index] += 1

            # Expected counts for uniform distribution
            expected = np.full(120, samples / 120)

            # Calculate chi-square statistic
            chi_square = np.sum(((counts - expected) ** 2) / expected)

            # Degrees of freedom for overlapping vs non-overlapping
            ndof = 96 if overlap else 119

            # Calculate p-value
            p_value = chi2.sf(chi_square, ndof)

            # Determine result based on p-value
            result = "Random" if p_value > 0.01 else "Non-Random"
            return p_value, result
        except Exception as e:
            raise ValueError(f"Error in OPERM5 Test: {e}")

    @staticmethod
    def _perm_index(v):
        """
        Computes the permutation index of a vector of 5 integers.

        :param v: List of 5 integers.
        :return: Permutation index (0 to 119).
        """
        w = list(v)
        p_index = 0
        for i in range(4, 0, -1):
            max_idx = max(range(i + 1), key=w.__getitem__)
            p_index = (i + 1) * p_index + max_idx
            w[i], w[max_idx] = w[max_idx], w[i]
        return p_index

    @staticmethod
    def _prepare_data(data):
        """
        Converts input data into a list of integers.

        :param data: Input data as binary string, bytes, or list.
        :return: List of integers.
        """
        if isinstance(data, str):
            return [ord(char) for char in data]
        elif isinstance(data, (bytes, bytearray)):
            return list(data)
        elif isinstance(data, list):
            return data
        else:
            raise ValueError("Unsupported data type. Provide binary string, bytes, or list of integers.")

# Example usage
if __name__ == "__main__":
    # Generate random test data
    rng = np.random.default_rng()
    test_data = rng.integers(0, 256, size=1000005, dtype=int).tolist()
    # rng = np.random.default_rng()
    # binary_data = rng.integers(0, 256, size=10000, dtype=int).tolist()

    try:
        p_value, result = DiehardOPERM5.run_test(test_data)
        print(f"OPERM5 Test: P-Value = {p_value}, Result = {result}")
    except Exception as e:
        print(e)
