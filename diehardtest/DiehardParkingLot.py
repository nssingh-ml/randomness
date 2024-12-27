import numpy as np
from scipy.stats import norm

class DiehardParkingLotTest:
    @staticmethod
    def run_test(data, num_attempts=12000, square_size=100, circle_radius=1):
        """
        Runs the Diehard Parking Lot Test.
 
        :param data: Input data as binary string, bytes, or list of integers.
        :param num_attempts: Number of attempts to park circles (default: 12,000).
        :param square_size: Size of the square (default: 100x100).
        :param circle_radius: Radius of each circle to park (default: 1).
        :return: Tuple (p_value, result), where p_value is the calculated p-value, and result is "Random" or "Non-Random".
        """
        try:
            # Convert input data into numerical values in the range [0, 1)
            numerical_data = DiehardParkingLotTest._prepare_numerical_data(data)

            # Ensure enough data for the required number of attempts
            if len(numerical_data) < num_attempts * 2:
                raise ValueError(f"Insufficient data: {len(numerical_data)} values provided, but {num_attempts * 2} needed.")

            parked_circles = []
            successful_parks = 0

            # Perform attempts to park circles
            for attempt in range(num_attempts):
                x, y = numerical_data[attempt * 2] * square_size, numerical_data[attempt * 2 + 1] * square_size
                
                # Check for collisions with already parked circles
                if DiehardParkingLotTest._is_valid_parking(x, y, parked_circles, circle_radius):
                    parked_circles.append((x, y))
                    successful_parks += 1

            # Compare the number of successful parks to the expected normal distribution
            mean = 3523
            sigma = 21.9
            z_score = (successful_parks - mean) / sigma
            p_value = 2 * (1 - norm.cdf(abs(z_score)))

            # Debugging information
            print(f"Successful Parks: {successful_parks}")
            print(f"Z-Score: {z_score}, Mean: {mean}, Sigma: {sigma}")
            print(f"P-Value: {p_value}")

            # Determine result based on p-value
            result = "Random" if p_value > 0.01 else "Non-Random"
            return p_value, result
        except Exception as e:
            raise ValueError(f"Error in Parking Lot Test: {e}")

    @staticmethod
    def _is_valid_parking(x, y, parked_circles, radius, epsilon=1e-6):
        """
        Checks if a circle can be parked at the given coordinates without overlapping others.

        :param x: X-coordinate of the circle's center.
        :param y: Y-coordinate of the circle's center.
        :param parked_circles: List of coordinates of already parked circles.
        :param radius: Radius of the circle.
        :return: True if the circle can be parked, False otherwise.
        """
        for px, py in parked_circles:
            distance = np.sqrt((x - px) ** 2 + (y - py) ** 2)
            if distance < (2 * radius-epsilon):  # Overlapping if closer than diameter
                return False
        return True

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

# Example usage
if __name__ == "__main__":
    # Generate random test data
    rng = np.random.default_rng(seed= 42)
    test_data = rng.integers(0, 256, size=24000, dtype=int).tolist()  # Enough data for 12000 attempts * 2 coordinates

    try:
        p_value, result = DiehardParkingLotTest.run_test(test_data)
        print(f"Parking Lot Test: P-Value = {p_value}, Result = {result}")
    except Exception as e:
        print(e)
