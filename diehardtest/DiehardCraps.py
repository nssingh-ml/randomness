import numpy as np
from scipy.stats import chisquare

class DiehardCraps:
    @staticmethod
    def run_test(data):
        """
        Runs the Diehard Craps test on the provided data.

        :param data: Input data as binary string, bytes, or list of integers.
        :return: Tuple (p_value, result), where p_value is the calculated p-value, and result is "Random" or "Non-Random".
        """
        try:
            # Convert input to numerical format if necessary
            data = DiehardCraps._prepare_data(data)

            if len(data) < 2:
                raise ValueError("Insufficient data length. At least two integers are required.")

            # Simulate craps game using the provided data
            wins, losses = DiehardCraps._simulate_craps(data)

            # Perform chi-square test
            total_games = wins + losses
            expected_wins = total_games * 244 / 495  # Based on theoretical probability of winning a craps game
            expected_losses = total_games * 251 / 495
            observed = [wins, losses]
            expected = [expected_wins, expected_losses]

            chi_stat, p_value = chisquare(observed, expected)

            # Determine result based on p-value
            result = "Random" if p_value > 0.01 else "Non-Random"
            return p_value, result
        except Exception as e:
            raise ValueError(f"Error in Craps Test: {e}")

    @staticmethod
    def _simulate_craps(data):
        """
        Simulates a craps game using the provided data.

        :param data: List of integers.
        :return: Tuple (wins, losses).
        """
        wins = 0
        losses = 0
        index = 0

        while index + 1 < len(data):
            roll1 = data[index] % 6 + 1  # First die roll
            roll2 = data[index + 1] % 6 + 1  # Second die roll
            sum_roll = roll1 + roll2
            index += 2

            if sum_roll in [7, 11]:
                wins += 1
            elif sum_roll in [2, 3, 12]:
                losses += 1
            else:
                point = sum_roll
                while index + 1 < len(data):
                    roll1 = data[index] % 6 + 1
                    roll2 = data[index + 1] % 6 + 1
                    sum_roll = roll1 + roll2
                    index += 2

                    if sum_roll == 7:
                        losses += 1
                        break
                    elif sum_roll == point:
                        wins += 1
                        break

        return wins, losses

    @staticmethod
    def _prepare_data(data):
        """
        Prepares data by converting it to a list of integers.

        :param data: Input data as binary string, bytes, or list.
        :return: List of integers.
        """
        if isinstance(data, str):
            return [ord(char) for char in data]
        elif isinstance(data, (bytes, bytearray)):
            return list(data)
        elif isinstance(data, list):
            return data
        else:
            raise ValueError("Unsupported data type. Provide binary string, bytes, or list of integers.")



# Simulate data for testing
rng = np.random.default_rng()
test_data = rng.integers(0, 256, size=1000, dtype=int).tolist()

# Run the test
try:
    p_value, result = DiehardCraps.run_test(test_data)
    print(p_value, result)
except Exception as e:
    str(e)

# Example usage
if __name__ == "__main__":
    # Example binary data
    rng = np.random.default_rng()
    binary_data = ''.join(rng.choice(['0', '1'], size=3200))
    print(binary_data)
    try:
        p_value, result = DiehardCraps.run_test(binary_data)
        print(f"Craps Test: P-Value = {p_value}, Result = {result}")
    except Exception as e:
        print(e)
