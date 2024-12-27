import numpy as np
from scipy.stats import chi2

class DiehardBitstream:
    @staticmethod
    def run_test(data, bit_length=20, samples=1000000):
        """
        Runs the Diehard Bitstream test on the provided data.

        :param data: Input data as binary string, bytes, or list of integers.
        :param bit_length: Length of the bit blocks to analyze (default: 20).
        :param samples: Number of bit blocks to test (default: 1,000,000).
        :return: Tuple (p_value, result), where p_value is the calculated p-value, and result is "Random" or "Non-Random".
        """
        try:
            # Convert input data to a binary string
            binary_data = DiehardBitstream._prepare_binary_data(data)

            # Adjust samples if insufficient data is available
            max_samples = len(binary_data) // bit_length
            if samples > max_samples:
                samples = max_samples

            if samples == 0:
                raise ValueError("Insufficient data length to perform the test.")

            # Extract bit blocks and count occurrences
            counts = np.zeros(2**bit_length, dtype=float)
            for i in range(samples):
                start = i * bit_length
                end = start + bit_length
                bit_block = binary_data[start:end]
                block_index = int(bit_block, 2)
                counts[block_index] += 1

            # Expected counts for uniform distribution
            expected = np.full(2**bit_length, samples / (2**bit_length))

            # Calculate chi-square statistic
            chi_square = np.sum(((counts - expected) ** 2) / expected)

            # Degrees of freedom
            ndof = (2**bit_length) - 1

            # Calculate p-value
            p_value = chi2.sf(chi_square, ndof)

            # Determine result based on p-value
            result = "Random" if p_value > 0.01 else "Non-Random"
            return p_value, result
        except Exception as e:
            raise ValueError(f"Error in Bitstream Test: {e}")

    @staticmethod
    def _prepare_binary_data(data):
        """
        Converts input data into a binary string.

        :param data: Input data as binary string, bytes, or list of integers.
        :return: Binary string.
        """
        try:
            if isinstance(data, str):
                return ''.join(f"{ord(char):08b}" for char in data)
            elif isinstance(data, (bytes, bytearray)):
                return ''.join(f"{byte:08b}" for byte in data)
            elif isinstance(data, list):
                return ''.join(f"{num:08b}" for num in data)
            else:
                raise ValueError("Unsupported data type. Provide binary string, bytes, or list of integers.")
        except Exception as e:
            raise ValueError(f"Error preparing binary data: {e}")

# Example usage
if __name__ == "__main__":
    # Generate random test data
    rng = np.random.default_rng()
    test_data = rng.integers(0, 256, size=200000, dtype=int).tolist()

    try:
        p_value, result = DiehardBitstream.run_test(test_data)
        print(f"Bitstream Test: P-Value = {p_value}, Result = {result}")
    except Exception as e:
        print(e)
