import numpy as np
from scipy.stats import chisquare
from itertools import permutations


class OverlappingPermutationsTest:
    @staticmethod
    def run_test(data, pattern_length=3):
        """
        Runs the Overlapping Permutations Test on the provided data.

        :param data: Binary data string to be tested
        :param pattern_length: Length of the permutation patterns to analyze
        :return: Tuple (p_value, result), where p_value is the calculated p-value, and result is "Random" or "Non-Random"
        """
        try:
            # Convert binary string to a list of normalized numbers
            numbers = OverlappingPermutationsTest._binary_to_numbers(data)

            # Generate all possible permutations of the given pattern length
            all_permutations = list(permutations(range(pattern_length)))
            num_permutations = len(all_permutations)

            # Count the occurrences of each permutation in the data
            observed_counts = OverlappingPermutationsTest._count_permutations(numbers, pattern_length, all_permutations)

            # Calculate expected frequency for uniform distribution
            total_patterns = len(numbers) - pattern_length + 1

            if total_patterns <= 0 or num_permutations <=0:
                raise ValueError("Not enough data to generate patterns of the given length.")
            
            expected_counts = [total_patterns / num_permutations] * num_permutations

            # Filter out permutations with zero expected frequencies
            observed_counts = np.array(observed_counts)
            expected_counts = np.array(expected_counts)
            valid_indices = expected_counts > 0
            observed_counts = observed_counts[valid_indices]
            expected_counts = expected_counts[valid_indices]

            # Perform chi-square test
            chi_stat, p_value = chisquare(observed_counts, expected_counts)

            # Determine randomness based on p-value
            result = "Random" if p_value > 0.01 else "Non-Random"
            return p_value, result
        except Exception as e:
            raise ValueError(f"Error in Overlapping Permutations Test: {e}")

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

    @staticmethod
    def _count_permutations(numbers, pattern_length, all_permutations):
        """
        Counts the occurrences of each permutation in the data.

        :param numbers: List of normalized floats
        :param pattern_length: Length of the permutation patterns
        :param all_permutations: List of all possible permutations
        :return: List of counts for each permutation
        """
        # Convert numbers to ranks
        ranks = [sorted(numbers[i:i + pattern_length]).index(numbers[i]) for i in range(len(numbers) - pattern_length + 1)]

        # Initialize counts for each permutation
        counts = [0] * len(all_permutations)

        # Count occurrences of each permutation
        for i in range(len(ranks) - pattern_length + 1):
            pattern = tuple(ranks[i:i + pattern_length])
            if pattern in all_permutations:
                index = all_permutations.index(pattern)
                counts[index] += 1

        return counts


# Example integration into main Diehard suite
if __name__ == "__main__":
    binary_data = "11001100110011001100110011001100" * 1000  # Example binary data for testing
    try:
        p_value, result = OverlappingPermutationsTest.run_test(binary_data)
        print(f"Overlapping Permutations Test: P-Value = {p_value}, Result = {result}")
    except Exception as e:
        print(e)
