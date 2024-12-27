import numpy as np
from scipy.stats import chi2

class DiehardMinimumDistance:
    @staticmethod
    def run_test(data, num_points=10000, num_trials=100):
        """
        Runs the Diehard Minimum Distance (2D Circle) Test on the provided data.

        :param data: Input data as binary string, bytes, or list of integers.
        :param num_points: Number of points to generate per trial (default: 10,000).
        :param num_trials: Number of trials to run (default: 100).
        :return: Tuple (p_value, result), where p_value is the calculated p-value, and result is "Random" or "Non-Random".
        """
        try:
            # Convert input data to numerical values in the range [0, 1)
            numerical_data = DiehardMinimumDistance._prepare_numerical_data(data)

            # Adjust the number of trials based on available data
            total_points = len(numerical_data) // 2  # Each point needs 2 values (x, y)
            max_trials = total_points // num_points
            if num_trials > max_trials:
                num_trials = max_trials

            if num_trials == 0:
                raise ValueError(f"Insufficient data: {len(numerical_data)} values provided, but at least {num_points * 2} needed.")

            min_distances = []

            # Perform trials
            for trial in range(num_trials):
                start_idx = trial * num_points * 2
                end_idx = (trial + 1) * num_points * 2
                points = numerical_data[start_idx:end_idx]
                points = np.array(points).reshape(-1, 2)

                # Calculate the minimum distance for this trial
                min_distance = DiehardMinimumDistance._calculate_min_distance(points)
                min_distances.append(min_distance)

            # Compute the chi-square statistic based on the distances
            bins = np.linspace(0, np.sqrt(2), 11)  # 10 bins require 11 edges
            counts, _ = np.histogram(min_distances, bins=bins)
            expected = np.full(len(counts), num_trials / len(counts))

            # Avoid division by zero in chi-square calculation
            expected[expected == 0] = 1e-10

            chi_square = np.sum(((counts - expected) ** 2) / expected)
            ndof = len(counts) - 1

            # Calculate p-value
            p_value = chi2.sf(chi_square, ndof)

            # Determine result based on p-value
            result = "Random" if p_value > 0.01 else "Non-Random"
            return p_value, result
        except Exception as e:
            raise ValueError(f"Error in Minimum Distance Test: {e}")

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

    @staticmethod
    def _calculate_min_distance(points):
        """
        Calculates the minimum distance between points in a 2D space.

        :param points: Array of points with shape (num_points, 2).
        :return: Minimum distance between any two points.
        """
        from scipy.spatial import distance

        # Compute pairwise distances and return the minimum distance
        dist_matrix = distance.cdist(points, points, 'euclidean')
        np.fill_diagonal(dist_matrix, np.inf)  # Ignore self-distances
        return np.min(dist_matrix)

# Example usage
if __name__ == "__main__":
    # Generate random test data
    rng = np.random.default_rng()
    test_data = rng.integers(0, 256, size=200000, dtype=int).tolist()

    try:
        p_value, result = DiehardMinimumDistance.run_test(test_data)
        print(f"Minimum Distance Test: P-Value = {p_value}, Result = {result}")
    except Exception as e:
        print(e)
