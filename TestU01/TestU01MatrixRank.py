import numpy as np
import math

def matrix_rank_test(data, rows=3, cols=3 ):
    """
    Implements the Matrix Rank Test for randomness.

    Parameters:
        data (list): Sequence of binary values (0s and 1s).
        rows (int): Number of rows in the matrix.
        cols (int): Number of columns in the matrix.

    Returns:
        Tuple: (p_value, result), where p_value is the calculated p-value, and result is "Random" or "Non-Random".
    """
    data  = list(map(int, data))
    n = len(data)
    rows = max(min(int(math.sqrt(n))//10,32),3)
    cols = rows
    print("n:", n, "rows:",rows)
    matrix_size = rows * cols

    if n < matrix_size:
        raise ValueError("Data length must be at least as large as the matrix size.")

    # Split data into blocks of size `rows * cols`
    num_matrices = n // matrix_size
    matrices = [
        np.array(data[i * matrix_size:(i + 1) * matrix_size]).reshape(rows, cols)
        for i in range(num_matrices)
    ]

    # Calculate ranks of each matrix
    full_rank = min(rows, cols)
    rank_counts = {full_rank: 0, full_rank - 1: 0, full_rank - 2: 0}

    for matrix in matrices:
        rank = np.linalg.matrix_rank(matrix)
        if rank in rank_counts:
            rank_counts[rank] += 1

    # Calculate probabilities for full rank, one less than full rank, and two less
    prob_full_rank = 1 - (1 / (2 ** (rows * cols - rows - cols + 1)))
    prob_one_less = (rows * cols - rows) / (2 ** (rows * cols - rows - cols + 1))
    prob_two_less = 1 - prob_full_rank - prob_one_less

    expected_counts = [
        num_matrices * prob_full_rank,
        num_matrices * prob_one_less,
        num_matrices * prob_two_less
    ]

    observed_counts = [
        rank_counts[full_rank],
        rank_counts[full_rank - 1],
        rank_counts.get(full_rank - 2, 0)
    ]

    # Chi-square statistic
    chi_square = sum(
        (obs - exp) ** 2 / exp for obs, exp in zip(observed_counts, expected_counts) if exp > 0
    )

    # Degrees of freedom
    degrees_of_freedom = 3 - 1

    # Calculate p-value
    p_value = 1 - math.gamma(degrees_of_freedom / 2) * math.exp(-chi_square / 2)

    # Determine randomness based on p-value
    result = "Random" if p_value > 0.01 else "Non-Random"

    return p_value, result

# Example usage
def example_matrix_rank_test():
    """Example test to check Matrix Rank Test functionality."""
    rng = np.random.default_rng()
    test_data = rng.choice([0, 1], size=100).tolist()  # Generate binary sequence of 0s and 1s

    try:
        rows = 3  # Number of rows in the matrix
        cols = 3  # Number of columns in the matrix
        p_value, result = matrix_rank_test(test_data, rows, cols)
        print(f"Matrix Rank Test: P-Value = {p_value}, Result = {result}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    example_matrix_rank_test()
