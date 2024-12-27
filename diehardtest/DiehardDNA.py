import numpy as np
from scipy.stats import norm
# I've added the implementation for the Diehard DNA Test, which processes 10-letter words with 2-bit letters (representing C, G, A, T) and calculates p-values based on missing words.
class DiehardDNATest:
    @staticmethod
    def run_test(data, num_words=1048576):
        """
        Runs the Diehard DNA (Overlapping Quadruples Sparse Occupancy) Test.

        :param data: Input data as binary string, bytes, or list of integers.
        :param num_words: Number of 10-letter words (default: 2^20 = 1,048,576).
        :return: Tuple (p_value, result), where p_value is the calculated p-value, and result is "Random" or "Non-Random".
        """
        try:
            # Convert input data into a binary string
            binary_data = DiehardDNATest._prepare_binary_data(data)
            num_bits = len(binary_data)
            required_bits = num_words * 20  # Each word uses 2 bits per letter, 10 letters total

            # Adjust num_words if data is insufficient
            if num_bits < required_bits:
                num_words = num_bits // 20
                if num_words == 0:
                    raise ValueError(f"Insufficient data: {num_bits} bits provided, but at least 20 bits are needed.")

            # Track occupancy of a 4x4x4x4x4x4x4x4x4x4 grid (10 letters from 2-bit alphabet)
            grid_size = 4  # DNA has 4 letters: C, G, A, T
            grid = np.zeros(tuple([grid_size] * 10), dtype=int)

            # Extract 2-bit letters to form 10-letter words
            for i in range(num_words):
                start = i * 20
                word_indices = [int(binary_data[start + (j * 2):start + (j * 2) + 2], 2) for j in range(10)]
                grid[tuple(word_indices)] += 1

            # Count the number of occupied cells
            occupied_cells = np.count_nonzero(grid)

            # Compute expected values based on normal distribution
            mean_missing = 141909
            sigma = 339
            missing_cells = (grid_size ** 10) - occupied_cells
            z_score = (missing_cells - mean_missing) / sigma

            # Calculate p-value
            p_value = 2 * (1 - norm.cdf(abs(z_score)))

            # Determine result based on p-value
            result = "Random" if p_value > 0.01 else "Non-Random"
            return p_value, result
        except Exception as e:
            raise ValueError(f"Error in DNA Test: {e}")

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
    test_data = rng.integers(0, 256, size=131072, dtype=int).tolist()  # Adjusted for available data

    try:
        p_value, result = DiehardDNATest.run_test(test_data)
        print(f"DNA Test: P-Value = {p_value}, Result = {result}")
    except Exception as e:
        print(e)
