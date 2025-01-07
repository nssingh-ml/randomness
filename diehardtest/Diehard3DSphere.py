import numpy as np
from scipy.stats import expon, kstest

class Diehard3DSphereTest:
    @staticmethod
    def run_test(data, num_points=4000, num_trials=20):
        """
        Runs the Diehard 3D Sphere Test on the provided data.

        :param data: Input data as binary string, bytes, or list of integers.
        :param num_points: Number of points to generate per trial (default: 4000).
        :param num_trials: Number of trials to run (default: 20).
        :return: Tuple (p_value, result), where p_value is the calculated p-value, and result is "Random" or "Non-Random".
        """
        try:
            # Convert input data to numerical values in the range [0, 1)
            numerical_data = Diehard3DSphereTest._prepare_numerical_data(data)

            # Ensure enough data for the required number of trials and points
            total_values_needed = num_points * 3 * num_trials  # Each point needs 3 coordinates (x, y, z)
            if len(numerical_data) < total_values_needed:
                raise ValueError(f"Insufficient data: {len(numerical_data)} values provided, but {total_values_needed} needed.")

            radii = []

            # Perform trials
            for trial in range(num_trials):
                start_idx = trial * num_points * 3
                end_idx = (trial + 1) * num_points * 3
                points = numerical_data[start_idx:end_idx]
                points = np.array(points).reshape(-1, 3)

                # Calculate minimum radius for spheres touching the nearest neighbor
                radius = Diehard3DSphereTest._calculate_min_radius(points)
                radii.append(radius)

            # Fit radii to exponential distribution and calculate p-value using KS test
            scale = np.mean(radii) 
            if scale <= 0:
                raise ValueError("Invalid scale parameter for exponential distribution.")
            ks_statistic, p_value = kstest(radii, 'expon', args=(0, scale))

            # Determine result based on p-value
            result = "Random" if p_value > 0.01 else "Non-Random"
            return p_value, result
        except Exception as e:
            # raise ValueError(f"Error in 3D Sphere Test: {e}")
            print(f"Error in 3D Sphere Test: {e}")
            return -1, "Non-Random"

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
    def _calculate_min_radius(points):
        """
        Calculates the minimum radius of spheres touching the nearest neighbor in a 3D space.

        :param points: Array of points with shape (num_points, 3).
        :return: Minimum radius.
        """
        from scipy.spatial import distance

        # Compute pairwise distances and ignore self-distances
        dist_matrix = distance.cdist(points, points, 'euclidean')
        np.fill_diagonal(dist_matrix, np.inf)

        # Find the minimum distance for each point (to its nearest neighbor)
        min_distances = np.min(dist_matrix, axis=1)

        # Return the minimum radius (half of the minimum distance)
        return np.min(min_distances) / 2

# Example usage
if __name__ == "__main__":
    # Generate random test data
    rng = np.random.default_rng()
    test_data = rng.integers(0, 256, size=240000, dtype=int).tolist()  # Adjusted for 4000 points * 3 coords * 20 trials

    try:
        p_value, result = Diehard3DSphereTest.run_test(test_data)
        print(f"3D Sphere Test: P-Value = {p_value}, Result = {result}")
    except Exception as e:
        print(e)
