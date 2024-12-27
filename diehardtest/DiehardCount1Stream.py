import numpy as np
from scipy.stats import chi2

class DiehardCountOnes:
    @staticmethod
    def run_test(data, block_size=8, samples=1000000):
        """
        Runs the Diehard Count the 1s (stream) test on the provided data.

        :param data: Input data as binary string, bytes, or list of integers.
        :param block_size: Size of each block in bits (default: 8).
        :param samples: Number of blocks to test (default: 1,000,000).
        :return: Tuple (p_value, result), where p_value is the calculated p-value, and result is "Random" or "Non-Random".
        """
        try:
            # Convert input data to a binary string
            binary_data = DiehardCountOnes._prepare_binary_data(data)

            # Adjust samples if insufficient data is available
            max_samples = len(binary_data) // block_size
            if samples > max_samples:
                samples = max_samples

            if samples == 0:
                raise ValueError("Insufficient data length to perform the test.")

            # Count the number of 1s in each block
            counts = np.zeros(block_size + 1, dtype=float)
            for i in range(samples):
                start = i * block_size
                end = start + block_size
                bit_block = binary_data[start:end]
                ones_count = bit_block.count('1')
                counts[ones_count] += 1

            # Expected counts for uniform distribution of 1s in blocks
            expected = [samples * (np.math.comb(block_size, k) / (2 ** block_size)) for k in range(block_size + 1)]

            # Calculate chi-square statistic
            chi_square = np.sum(((counts - expected) ** 2) / expected)

            # Degrees of freedom
            ndof = block_size

            # Calculate p-value
            p_value = chi2.sf(chi_square, ndof)

            # Determine result based on p-value
            result = "Random" if p_value > 0.01 else "Non-Random"
            return p_value, result
        except Exception as e:
            raise ValueError(f"Error in Count Ones Test: {e}")

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
    rng = np.random.default_rng(seed=42)
    test_data = rng.integers(0, 256, size=200000, dtype=int).tolist()

    try:
        p_value, result = DiehardCountOnes.run_test(test_data)
        print(f"Count Ones Test: P-Value = {p_value}, Result = {result}")
    except Exception as e:
        print(e)
