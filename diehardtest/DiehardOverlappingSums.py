import numpy as np

class DiehardOverlappingSums:
    @staticmethod
    def run_test(data, n=10000, shift=256):
        """
        Implements the Diehard Overlapping Sums test.

        Parameters:
        - data: list, numpy array, or string of binary/character data to be tested.
        - n: int, the number of sums to calculate (default: 10000).
        - shift: int, the number of integers to sum in each overlapping window (default: 256).

        Returns:
        - A dictionary containing the test statistic and p-value.
        """
        try:
            # Convert data to a numeric format if necessary
            if isinstance(data, str):
                data = [ord(char) for char in data]
            elif isinstance(data, (bytes, bytearray)):
                data = list(data)

            data = np.array(data, dtype=int)

            if len(data) < n + shift:
                raise ValueError("Insufficient data length. Ensure len(data) >= n + shift.")

            sums = []

            # Compute the sums for overlapping windows
            for i in range(n):
                current_sum = sum(data[i:i + shift])
                sums.append(current_sum)

            # Normalize the sums
            sums = np.array(sums, dtype=float)
            mean = shift * 0.5
            std_dev = np.sqrt(shift * (1 / 12))
            normalized_sums = (sums - mean) / std_dev

            # Calculate the test statistic (chi-squared test)
            hist, bin_edges = np.histogram(normalized_sums, bins=100, density=True)
            expected_prob = 1 / 100

            chi_squared = sum(((obs - expected_prob) ** 2) / expected_prob for obs in hist)

            # Calculate p-value using chi-squared distribution
            from scipy.stats import chi2

            df = len(hist) - 1
            p_value = chi2.sf(chi_squared, df)


            # Determine result based on p-value
            result = "Random" if p_value > 0.01 else "Non-Random"
            return p_value, result

            # return {
            #     "test_statistic": chi_squared,
            #     "p_value": p_value
            # }
        except Exception as e:
            print(f"Error in  Overlapping Sums Test: {e}")
            return  -1, "Non-Random"
            # raise ValueError(f"Error in  Overlapping Sums Test: {e}")

# def process_input(data):
#     try:
#         result = diehard_overlapping_sums_test(data)
#         return {
#             "status": "success",
#             "result": result
#         }
#     except Exception as e:
#         return {
#             "status": "error",
#             "message": str(e)
#         }


# example_data = np.random.randint(0, 256, size=20000, dtype=np.uint8)  # Simulated random data
# result = DiehardOverlappingSums.run_test(example_data)

# print(result)

# if __name__ == "__main__":
#     import sys
#     import json

#     # Read input data from standard input
#     input_data = sys.stdin.read()

#     # Decode JSON input
#     try:
#         parsed_input = json.loads(input_data)
#         data = parsed_input.get("data", "")
#         if isinstance(data, str):
#             data = [ord(char) for char in data]
#         elif isinstance(data, (bytes, bytearray)):
#             data = list(data)
#     except json.JSONDecodeError:
#         print(json.dumps({"status": "error", "message": "Invalid JSON input."}))
#         sys.exit(1)

#     # Process the input and run the test
#     output = process_input(data)

#     # Output the result as JSON
#     print(json.dumps(output))
