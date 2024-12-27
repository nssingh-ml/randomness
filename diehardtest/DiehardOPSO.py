import numpy as np
from scipy.stats import chi2

class DiehardOPSOTest:
    @staticmethod
    def run_test(data, num_words=1048576):
        """
        Runs the Diehard OPSO (Overlapping Pairs Sparse Occupancy) Test.

        :param data: Input data as binary string, bytes, or list of integers.
        :param num_words: Number of 2-letter words (default: 2^20 = 1,048,576).
        :return: Tuple (p_value, result), where p_value is the calculated p-value, and result is "Random" or "Non-Random".
        """
        try:
            # Convert input data into a binary string
            binary_data = DiehardOPSOTest._prepare_binary_data(data)
            num_bits = len(binary_data)
            required_bits = num_words * 20  # Each word needs 2x10 bits

            # Adjust num_words if data is insufficient
            if num_bits < required_bits:
                num_words = num_bits // 20
                if num_words == 0:
                    raise ValueError(f"Insufficient data: {num_bits} bits provided, but at least 20 bits are needed.")
                required_bits = num_words * 20

            # Track occupancy of a 1024x1024 grid (10-bit letters form a 2-letter word)
            grid_size = 1024
            grid = np.zeros((grid_size, grid_size), dtype=int)

            # Extract 10-bit letters to form 2-letter words
            for i in range(num_words):
                start = i * 20
                letter1 = int(binary_data[start:start + 10], 2)
                letter2 = int(binary_data[start + 10:start + 20], 2)
                grid[letter1, letter2] += 1

            # Count the number of occupied cells
            occupied_cells = np.count_nonzero(grid)

            # Compute chi-square statistic based on sparse occupancy
            expected_occupied = grid_size * grid_size * (1 - np.exp(-num_words / (grid_size * grid_size)))
            variance = expected_occupied * (1 - (1 / (grid_size * grid_size)))
            chi_square = ((occupied_cells - expected_occupied) ** 2) / variance

            # Calculate p-value
            p_value = chi2.sf(chi_square, df=1)

            # Determine result based on p-value
            result = "Random" if p_value > 0.01 else "Non-Random"
            return p_value, result
        except Exception as e:
            raise ValueError(f"Error in OPSO Test: {e}")

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
        p_value, result = DiehardOPSOTest.run_test(test_data)
        print(f"OPSO Test: P-Value = {p_value}, Result = {result}")
    except Exception as e:
        print(e)
