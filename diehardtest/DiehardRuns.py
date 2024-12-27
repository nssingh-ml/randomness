import numpy as np
from scipy.stats import norm


class DiehardRuns:
    @staticmethod
    def run_test(data):
        """
        Runs the Runs Test on the provided data.

        :param data: Binary data string to be tested
        :return: Tuple (p_value, result), where p_value is the calculated p-value, and result is "Random" or "Non-Random"
        """
        try:
            # Convert binary string to a list of floats (0 to 1)
            numbers = DiehardRuns._binary_to_numbers(data)

            # Perform runs test
            z_stat, p_value = DiehardRuns._calculate_runs(numbers)

            # Determine randomness based on p-value
            result = "Random" if p_value > 0.01 else "Non-Random"
            # return z_stat, p_value, result
            return p_value, result
        except Exception as e:
            raise ValueError(f"Error in Runs Test: {e}")

    @staticmethod
    def _binary_to_numbers(data):
        """
        Converts binary string to a list of normalized float numbers (0 to 1).

        :param data: Binary data string
        :return: List of floats between 0 and 1
        """
        if not data:
            raise ValueError("No data provided for testing.")

        # if len(data) % 32 != 0:
        #     raise ValueError("Binary data length must be a multiple of 32.")

        # # Split binary data into 32-bit chunks
        # chunks = [data[i:i + 32] for i in range(0, len(data), 32)]

        # # Convert each chunk to an integer and normalize to range [0, 1)
        # numbers = [int(chunk, 2) / (2**32) for chunk in chunks]
        # return numbers

        # Ensure the data is divided into 32-bit chunks, handle any remainder bits
        chunk_size = 32
        chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

        # Convert each chunk to an integer and normalize to range [0, 1)
        numbers = [int(chunk.ljust(chunk_size, '0'), 2) / (2**chunk_size) for chunk in chunks]
        return numbers

    @staticmethod
    def _calculate_runs(numbers):
        """
        Calculates the Z-statistic and p-value for the Runs Test.

        :param numbers: List of floats between 0 and 1
        :return: Tuple (z_stat, p_value)
        """
        n = len(numbers)
        runs = 1  # Initialize the number of runs

        # Count the number of runs in the data
        for i in range(1, n):
            if numbers[i] != numbers[i - 1]:
                runs += 1
        # print("n",n)
        # Calculate the expected number of runs and its standard deviation
        expected_runs = (2 * n - 1) / 3
        std_dev_runs = np.sqrt((16 * n - 29) / 90)

        # Calculate the Z-statistic
        z_stat = (runs - expected_runs) / std_dev_runs

        # Calculate the p-value using the cumulative distribution function (CDF)
        p_value = 2 * (1 - norm.cdf(abs(z_stat)))  # Two-tailed test

        return z_stat, p_value



# Correctly adjust random binary data to ensure length is a multiple of 32
# def generate_corrected_random_binary_data(length=10000):
#     adjusted_length = (length + 31) // 32 * 32
#     rng = np.random.default_rng()
#     binary_data = ''.join(rng.choice(['0', '1'], size=adjusted_length))
#     return binary_data


def generate_arbitrary_binary_data(length=10005):  # Not a multiple of 32
    rng = np.random.default_rng()
    binary_data = ''.join(rng.choice(['0', '1'], size=length))
    return binary_data
# Generate corrected binary data
binary_data = generate_arbitrary_binary_data()


# z_stat, p_value, result = DiehardRuns.run_test(binary_data)
# print(z_stat, p_value, result)


# Example usage
if __name__ == "__main__":
    # Example binary data
    binary_data = "10111001111110111000110101010"*2  # Repeat pattern for testing

    try:
        # z_stat, p_value, result =  DiehardRuns.run_test(binary_data)
        # print(f"run Test: P-Value = {p_value}, Result = {result},{z_stat}")
        p_value, result =  DiehardRuns.run_test(binary_data)
        print(f"run Test: P-Value = {p_value}, Result = {result}")
    except Exception as e:
        print(e)
