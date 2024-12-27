import numpy as np
from scipy.stats import chisquare

class Diehard32x32BinaryRank:
    @staticmethod
    def run_test(data):
        """
        Runs the Diehard 32x32 Binary Rank test on the provided data.

        :param data: Input data as binary string, bytes, or list of integers.
        :return: Tuple (p_value, result), where p_value is the calculated p-value, and result is "Random" or "Non-Random".
        """
        try:
            # Convert input to binary format and prepare 32x32 matrices
            matrices = Diehard32x32BinaryRank._prepare_matrices(data)

            # Perform rank calculations
            rank_counts = Diehard32x32BinaryRank._calculate_rank_counts(matrices)

            # Expected proportions for 32x32 binary rank test
            total_matrices = len(matrices)
            expected_counts = [
                total_matrices * 0.2888,  # Full rank (32)
                total_matrices * 0.5776,  # Rank 31
                total_matrices * 0.1336   # Rank <= 30
            ]

            # Perform chi-square test
            chi_stat, p_value = chisquare(rank_counts, expected_counts)

            # Determine result based on p-value
            result = "Random" if p_value > 0.01 else "Non-Random"
            return p_value, result
        except Exception as e:
            raise ValueError(f"Error in 32x32 Binary Rank Test: {e}")

    @staticmethod
    def _prepare_matrices(data):
        """
        Converts the input data into a list of 32x32 binary matrices.

        :param data: Input data as binary string, bytes, or list of integers.
        :return: List of 32x32 numpy matrices.
        """
        # if isinstance(data, str):
        #     binary_data = ''.join(f"{ord(char):08b}" for char in data)

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
            raise ValueError("Unsupported data type. Provide binary string, bytes, or list of integers.")

        # Ensure enough data for at least one 32x32 matrix
        if len(binary_data) < 32 * 32:
            raise ValueError("Insufficient data length. At least 1024 bits are required.")

        # Split binary data into 32x32 matrices
        matrices = []
        for i in range(0, len(binary_data) - 1024 + 1, 1024):
            matrix_data = binary_data[i:i + 1024]
            matrix = np.array([list(map(int, matrix_data[j:j + 32])) for j in range(0, 1024, 32)], dtype=int)
            matrices.append(matrix)

        return matrices

    @staticmethod
    def _calculate_rank_counts(matrices):
        """
        Calculates the rank counts for a list of 32x32 matrices.

        :param matrices: List of 32x32 numpy matrices.
        :return: List of counts [full_rank, rank_31, rank_30_or_less].
        """
        full_rank = 0
        rank_31 = 0
        rank_30_or_less = 0

        for matrix in matrices:
            rank = np.linalg.matrix_rank(matrix)
            if rank == 32:
                full_rank += 1
            elif rank == 31:
                rank_31 += 1
            else:
                rank_30_or_less += 1

        return [full_rank, rank_31, rank_30_or_less]

# Example usage
if __name__ == "__main__":
    # Example binary data
    rng = np.random.default_rng()
    binary_data = rng.integers(0, 20056, size=4096, dtype=int).tolist()

    try:
        p_value, result = Diehard32x32BinaryRank.run_test(binary_data)
        print(f"32x32 Binary Rank Test: P-Value = {p_value}, Result = {result}")
    except Exception as e:
        print(e)
