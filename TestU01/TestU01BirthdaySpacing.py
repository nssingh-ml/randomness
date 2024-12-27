import math
from collections import Counter

def birthday_spacing_test(data, m=1000, n=10):
    """
    Implements the Birthday Spacings Test from TestU01.

    Parameters:
        data (list): Sequence of random numbers (integers) to test.
        m (int): The size of the "birthday space" (range of random values).
        n (int): Number of "birthdays" to pick from the space.

    Returns:
        Tuple: (p_value, result), where p_value is the calculated p-value, and result is "Random" or "Non-Random".
    """
    data = check_bitstream(data)
    if n > m:
        raise ValueError("Number of birthdays (n) cannot exceed the size of the birthday space (m).")

    # Map data to the range [0, m)
    print("len",len(data))
    mapped_data = [x % m for x in data[:n]]
    print(len(mapped_data))
    # Sort the mapped data to compute spacings
    sorted_data = sorted(mapped_data)
    print(len(sorted_data))
    # Calculate spacings between consecutive birthdays
    spacings = [(sorted_data[i + 1] - sorted_data[i]) for i in range(n - 1)]
    spacings.append((sorted_data[0] + m) - sorted_data[-1])  # Wraparound spacing

    # Count occurrences of spacings
    spacing_counts = Counter(spacings)

    # Compute the test statistic
    statistic = sum(count ** 2 for count in spacing_counts.values()) - n

    # Normalize the test statistic
    statistic /= n

    # Compute the expected mean and variance under the null hypothesis
    mean = n * (n - 1) / (2 * m)
    variance = n * (n - 1) * (2 * n - 1) / (6 * m ** 2)

    # Compute the z-score
    z = (statistic - mean) / math.sqrt(variance)

    # Convert the z-score to a two-sided p-value
    p_value = 2 * (1 - math.erf(abs(z) / math.sqrt(2)))

    # Determine randomness based on p-value
    result = "Random" if p_value > 0.01 else "Non-Random"

    return p_value, result

def check_bitstream(bit_stream):
    
    if not bit_stream:
        raise ValueError("No data provided for testing.")

    # if len(data) % 32 != 0:
    #     raise ValueError("Binary data length must be a multiple of 32.")
    
    if len(bit_stream) % 32 != 0:
        padding_length = 32 - (len(bit_stream) % 32)
        bit_stream += '0' * padding_length

    # Split binary data into 32-bit chunks
    # chunks = [data[i:i + 32] for i in range(0, len(data), 32)]

    # Convert each chunk to an integer and normalize to range [0, 1)
    # numbers = [int(chunk, 2) / (2**32) for chunk in chunks]
    # return numbers


    # if len(bit_stream) % 32 != 0:
    #     padding_length = 32 - (len(bit_stream) % 32)
    #     bit_stream += '0' * padding_length
    data = [int(bit_stream[i:i+32], 2) for i in range(0, len(bit_stream), 32)]

    return data

if __name__ == "__main__":
    # Example input data
    # test_data = [123, 456, 789, 101, 202, 303, 404, 505, 606, 707]
    m = 1000  # Size of the birthday space
    n = 10    # Number of birthdays
    bit_stream = "110010111011011001010101110010100111001011100101011011001011001111100101110110110010101011100101001110010111001010110110010110011111001011101101100101010111001010011100101110010101101100101100111110010111011011001010101110010100111001011100101011011001011001111100101110110110010101011100101001110010111001010110110010110011111001011101101100101010111001010011100101110010101101100101100111110010111011011001010101110010100111001011100101011011001011001111100101110110110010101011100101001110010111001010110110010110011111001011101101100101010111001010011100101110010101101100101100111"
    # print(len(bit_stream))
    # Ensure bit_stream is a multiple of 32 by padding with zeros if necessary
    if len(bit_stream) % 32 != 0:
        padding_length = 32 - (len(bit_stream) % 32)
        bit_stream += '0' * padding_length
    # data = [int(bit_stream[i:i+32], 2) for i in range(0, len(bit_stream), 32)]

    # try:
    p_value, result = birthday_spacing_test(bit_stream, m, n)
    print("Birthday Spacings Test P-Value:", p_value)
    print("Result:", result)
    # except Exception as e:
        # print(f"Error: {e}")






















# import math
# from collections import Counter
# import os

# def birthday_spacing_test(data, m, n):
#     """
#     Implements the Birthday Spacings Test from TestU01.

#     Parameters:
#         data (list): Sequence of random numbers (integers) to test.
#         m (int): The size of the "birthday space" (range of random values).3

#         n (int): Number of "birthdays" to pick from the space.

#     Returns:
#         Tuple: (p_value, result), where p_value is the calculated p-value, and result is "Random" or "Non-Random".
#     """
#     if n > m:
#         raise ValueError("Number of birthdays (n) cannot exceed the size of the birthday space (m).")

#     # Map data to the range [0, m)
#     mapped_data = [x % m for x in data[:n]]

#     # Sort the mapped data to compute spacings
#     sorted_data = sorted(mapped_data)

#     # Calculate spacings between consecutive birthdays
#     spacings = [(sorted_data[i + 1] - sorted_data[i]) for i in range(n - 1)]
#     spacings.append((sorted_data[0] + m) - sorted_data[-1])  # Wraparound spacing

#     # Count occurrences of spacings
#     spacing_counts = Counter(spacings)

#     # Compute the test statistic
#     statistic = sum(count ** 2 for count in spacing_counts.values()) - n

#     # Normalize the test statistic
#     statistic /= n

#     # Compute the expected mean and variance under the null hypothesis
#     mean = n * (n - 1) / (2 * m)
#     variance = n * (n - 1) * (2 * n - 1) / (6 * m ** 2)

#     # Compute the z-score
#     z = (statistic - mean) / math.sqrt(variance)

#     # Convert the z-score to a two-sided p-value
#     p_value = 2 * (1 - math.erf(abs(z) / math.sqrt(2)))

#     # Determine randomness based on p-value
#     result = "Random" if p_value > 0.01 else "Non-Random"

#     return p_value, result

# def read_binary_fiead()
#     return [int(byte) for byte in data]

# def read_string_file(filepath):
#     """Reads a binary file and converts it to a list of integers."""
#     with open(filepath, "rb") as f:
#         data = f.rle(filepath):
#     """Reads a file containing space-separated integers."""
#     with open(filepath, "r") as f:
#         data = f.read()
#     return [int(num) for num in data.split()]

# def read_console_input():
#     """Reads binary input from the console."""
#     binary_input = input("Enter a binary string: ")
#     if len(binary_input) % 32 != 0:
#         raise ValueError("Binary input length must be a multiple of 32.")
#     return [int(binary_input[i:i+32], 2) for i in range(0, len(binary_input), 32)]

# if __name__ == "__main__":
#     print("Select input method:")
#     print("1. Binary file")
#     print("2. String file")
#     print("3. Console input (binary numbers)")
#     choice = input("Enter your choice (1/2/3): ")

#     try:
#         if choice == "1":
#             filepath = input("Enter the path to the binary file: ")
#             data = read_binary_file(filepath)
#         elif choice == "2":
#             filepath = input("Enter the path to the string file: ")
#             data = read_string_file(filepath)
#         elif choice == "3":
#             data = read_console_input()
#         else:
#             raise ValueError("Invalid choice. Please select 1, 2, or 3.")

#         m = int(input("Enter the size of the birthday space (m): "))
#         n = int(input("Enter the number of birthdays (n): "))

#         p_value, result = birthday_spacing_test(data, m, n)
#         print("Birthday Spacings Test P-Value:", p_value)
#         print("Result:", result)
#     except Exception as e:
#         print(f"Error: {e}")
