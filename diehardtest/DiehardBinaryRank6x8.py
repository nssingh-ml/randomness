import numpy as np
from scipy.stats import chisquare

class Diehard6x8BinaryRank:
    @staticmethod
    def run_test(data):
        """
        Runs the Diehard 6x8 Binary Rank test on the provided data.

        :param data: Input data as binary string, bytes, list of integers, or file path.
        :return: Tuple (p_value, result), where p_value is the calculated p-value, and result is "Random" or "Non-Random".
        """
        try:
            # Handle input and convert it to binary format
            matrices = Diehard6x8BinaryRank._prepare_matrices(data)

            # Perform rank calculations
            rank_counts = Diehard6x8BinaryRank._calculate_rank_counts(matrices)

            # Expected proportions for 6x8 binary rank test
            total_matrices = len(matrices)
            expected_counts = [
                total_matrices * 0.00171,  # Full rank (6)
                total_matrices * 0.146,    # Rank 5
                total_matrices * 0.85229   # Rank <= 4
            ]

            # Perform chi-square test
            chi_stat, p_value = chisquare(rank_counts, expected_counts)

            # Determine result based on p-value
            result = "Random" if p_value > 0.01 else "Non-Random"
            return p_value, result
        except Exception as e:
            raise ValueError(f"Error in 6x8 Binary Rank Test: {e}")

    @staticmethod
    def _prepare_matrices(data):
        """
        Converts the input data into a list of 6x8 binary matrices.

        :param data: Input data as binary string, bytes, list of integers, or file path.
        :return: List of 6x8 numpy matrices.
        """
        if isinstance(data, str):
            if data.endswith(".txt"):
                # Read text file content
                with open(data, "r") as file:
                    content = file.read()
                binary_data = ''.join(f"{ord(char):08b}" for char in content)
            else:
                # Assume input is a binary string
                binary_data = ''.join(f"{ord(char):08b}" for char in data)
        elif isinstance(data, (bytes, bytearray)):
            binary_data = ''.join(f"{byte:08b}" for byte in data)
        elif isinstance(data, list):
            binary_data = ''.join(f"{num:08b}" for num in data)
        else:
            raise ValueError("Unsupported data type. Provide binary string, bytes, list of integers, or file path.")

        # Ensure enough data for at least one 6x8 matrix
        if len(binary_data) < 6 * 8:
            raise ValueError("Insufficient data length. At least 48 bits are required.")

        # Split binary data into 6x8 matrices
        matrices = []
        for i in range(0, len(binary_data) - 48 + 1, 48):
            matrix_data = binary_data[i:i + 48]
            matrix = np.array([list(map(int, matrix_data[j:j + 8])) for j in range(0, 48, 8)], dtype=int)
            matrices.append(matrix)

        return matrices

    @staticmethod
    def _calculate_rank_counts(matrices):
        """
        Calculates the rank counts for a list of 6x8 matrices.

        :param matrices: List of 6x8 numpy matrices.
        :return: List of counts [full_rank, rank_5, rank_4_or_less].
        """
        full_rank = 0
        rank_5 = 0
        rank_4_or_less = 0

        for matrix in matrices:
            rank = np.linalg.matrix_rank(matrix)
            if rank == 6:
                full_rank += 1
            elif rank == 5:
                rank_5 += 1
            else:
                rank_4_or_less += 1

        return [full_rank, rank_5, rank_4_or_less]

# Example usage
if __name__ == "__main__":
    # Example binary data
    rng = np.random.default_rng()
    binary_data = rng.integers(0, 256, size=4096, dtype=int).tolist()

    try:
        p_value, result = Diehard6x8BinaryRank.run_test(binary_data)
        print(f"6x8 Binary Rank Test: P-Value = {p_value}, Result = {result}")
    except Exception as e:
        print(e)
