import numpy as np
from scipy.stats import chisquare


class DiehardBirthdaySpacings:
    @staticmethod
    def run_test(data, num_bins=10):
        """
        Runs the Birthday Spacings Test on the provided data.

        :param data: Binary data string to be tested
        :param num_bins: Number of bins for chi-square calculation
        :return: Tuple (p_value, result), where p_value is the calculated p-value, and result is "Random" or "Non-Random"
        """
        try:
            # Convert binary string to a list of floats (0 to 1)
            numbers = DiehardBirthdaySpacings._binary_to_numbers(data)

            # Calculate spacings between sorted numbers
            spacings = np.diff(np.sort(numbers))

            # Bin the spacings
            hist, _ = np.histogram(spacings, bins=num_bins, range=(0, 1))

            # Expected uniform distribution
            n = len(spacings)
            expected = [n / num_bins] * num_bins

            # Perform chi-square test
            chi_stat, p_value = chisquare(hist, expected)

            # Determine randomness based on p-value
            result = "Random" if p_value > 0.01 else "Non-Random"
            return p_value, result
        except Exception as e:
            raise ValueError(f"Error in Birthday Spacings Test: {e}")

    @staticmethod
    def _binary_to_numbers(data):
        """
        Converts binary string to a list of normalized float numbers (0 to 1).

        :param data: Binary data string
        :return: List of floats between 0 and 1
        """
        if not data:
            raise ValueError("No data provided for testing.")

        if len(data) % 32 != 0:
            raise ValueError("Binary data length must be a multiple of 32.")

        # Split binary data into 32-bit chunks
        chunks = [data[i:i + 32] for i in range(0, len(data), 32)]

        # Convert each chunk to an integer and normalize to range [0, 1)
        numbers = [int(chunk, 2) / (2**32) for chunk in chunks]
        return numbers



# Example usage
if __name__ == "__main__":
    # Example binary data
    rng = np.random.default_rng()
    binary_data = ''.join(rng.choice(['0', '1'], size=3200))
    # binary_data = "11001100110011001100110011111001111001111111111001100" *32  # Repeat pattern for testing

    try:
        p_value, result = DiehardBirthdaySpacings.run_test(binary_data)
        print(f"Birthday Spacings Test: P-Value = {p_value}, Result = {result}")
    except Exception as e:
        print(e)