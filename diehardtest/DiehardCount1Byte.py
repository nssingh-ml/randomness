import numpy as np
from scipy.stats import chi2

class DiehardCountOnesByte:
    @staticmethod
    def run_test(data, samples=1000000):
        """
        Runs the Diehard Count the 1s (byte) test on the provided data.

        :param data: Input data as binary string, bytes, or list of integers.
        :param samples: Number of bytes to test (default: 1,000,000).
        :return: Tuple (p_value, result), where p_value is the calculated p-value, and result is "Random" or "Non-Random".
        """
        try:
            # Convert input data to a list of bytes
            byte_data = DiehardCountOnesByte._prepare_byte_data(data)

            # Adjust samples if insufficient data is available
            if len(byte_data) < samples:
                samples = len(byte_data)

            if samples == 0:
                raise ValueError("Insufficient data length to perform the test.")

            # Count the number of 1s in each byte
            counts = np.zeros(9, dtype=float)  # Bytes have 0 to 8 ones
            for i in range(samples):
                ones_count = bin(byte_data[i]).count('1')
                counts[ones_count] += 1

            # Expected counts for uniform distribution of 1s in bytes
            expected = [samples * (np.math.comb(8, k) / 256) for k in range(9)]

            # Calculate chi-square statistic
            chi_square = np.sum(((counts - expected) ** 2) / expected)

            # Degrees of freedom
            ndof = 8

            # Calculate p-value
            p_value = chi2.sf(chi_square, ndof)

            # Determine result based on p-value
            result = "Random" if p_value > 0.01 else "Non-Random"
            return p_value, result
        except Exception as e:
            raise ValueError(f"Error in Count Ones Byte Test: {e}")

    @staticmethod
    def _prepare_byte_data(data):
        """
        Converts input data into a list of bytes.

        :param data: Input data as binary string, bytes, or list of integers.
        :return: List of integers (each representing a byte).
        """
        try:
            if isinstance(data, str):
                return [ord(char) for char in data]
            elif isinstance(data, (bytes, bytearray)):
                return list(data)
            elif isinstance(data, list):
                return data
            else:
                raise ValueError("Unsupported data type. Provide binary string, bytes, or list of integers.")
        except Exception as e:
            raise ValueError(f"Error preparing byte data: {e}")

# Example usage
if __name__ == "__main__":
    # Generate random test data
    rng = np.random.default_rng()
    test_data = rng.integers(0, 256, size=200000, dtype=int).tolist()

    try:
        p_value, result = DiehardCountOnesByte.run_test(test_data)
        print(f"Count Ones Byte Test: P-Value = {p_value}, Result = {result}")
    except Exception as e:
        print(e)
