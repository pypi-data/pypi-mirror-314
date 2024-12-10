import os  # code number 4


class Division:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print(f"Exception occurred: {exc_value}")
        return True  # Suppress exception

    def divide(self, dividend, divisors):
        for divisor in divisors:  # Use a generator to iterate over divisors
            try:
                yield dividend / divisor
            except ZeroDivisionError:
                yield f"Division by zero is not allowed for divisor {divisor}"


# Example usage for Division class
dividends = [10]  # List of dividends to divide
divisors = [2, 0, 5]  # List of divisors including a zero

with Division() as d:
    for dividend in dividends:
        for result in d.divide(dividend, divisors):
            print(result)


def has_three_consecutive(lst):
    return any(lst[i] == lst[i + 1] == lst[i + 2] for i in range(len(lst) - 2))


lst = [1, 2, 2, 2, 3, 4, 5]
print(has_three_consecutive(lst))  # Example list

my_dict = {'a': [1, 2], 'b': [3, 4], 'c': [5, 6]}  # code number 3
combined_values = [val for sublist in my_dict.values() for val in sublist]
print(combined_values)


def count_lines_of_code(directory_path):
    total_lines = 0
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".py"):  # Process only Python files
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:  # Ensure UTF-8 encoding
                        total_lines += len(f.readlines())
                except UnicodeDecodeError as e:
                    # Handle decoding errors
                    print(f"Error reading {file_path}: {e}")
    return total_lines


# Example usage:
# Using raw string
directory_path = r'C:\Users\HP\Desktop\Jupyter_files\Lab_11\mypackage_davidattiah'
print(f"Total lines of code: {count_lines_of_code(directory_path)}")

# V. Генераторы словарей
dict1 = {'a': 1, 'b': 2, 'c': 3}  # code number 1
dict2 = {1: 'яблоко', 2: 'банан', 3: 'вишня'}

# Combine the two dictionaries
result = {key: dict2[value] for key, value in dict1.items()}
print(result)

# code number 2
words = [
    "Create",
    "Character",
    "a",
    "as",
    "and",
    "dictionary",
    "with",
    "words",
    "key",
    "first",
    "Value",
    "starting",
    "that"]

# Create the result dictionary using a generator expression
result = {
    first_char: [word for word in words if word.strip()[0].upper()
                 == first_char]
    for first_char in {word.strip()[0].upper() for word in words}
}

# Print the result dictionary
print(result)

# List of dictionaries  # code number 3
dict_list = [{'K': 'value1', 'L': 'value2'},
             {'K': '', 'L': 'value3'},
             {'K': 'value4', 'L': 'value5'},
             {'K': '', 'L': 'value6'},
             {'K': 'value7', 'L': 'value8'}]

# Extract dictionaries where the value of 'K' is an empty string
result = [d for d in dict_list if d.get('K') == '']
print(result)

# Генераторы-функции
# Task 1: Fibonacci generator


def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Task 2: Geometric progression generator


def geometric_progression(start, ratio):
    current = start
    while True:
        yield current
        current *= ratio

# Task 3: Countdown generator


def countdown(n):
    while n >= 0:
        yield n
        n -= 1


# Main section to test everything when the module is run directly
if __name__ == "__main__":
    print("Testing Division class:")
    dividends = [10]
    divisors = [2, 0, 5]
    with Division() as d:
        for dividend in dividends:
            for result in d.divide(dividend, divisors):
                print(result)

    print("\nTesting has_three_consecutive function:")
    lst = [1, 2, 2, 2, 3, 4, 5]
    print(has_three_consecutive(lst))  # Example list

    print("\nTesting combined values from dictionary:")
    my_dict = {'a': [1, 2], 'b': [3, 4], 'c': [5, 6]}
    combined_values = [val for sublist in my_dict.values() for val in sublist]
    print(combined_values)

    print("\nCounting lines of code in a directory (adjust the path):")
    directory_path = '/path/to/python/files'  # Replace with your actual directory
    print(f"Total lines of code: {count_lines_of_code(directory_path)}")

    print("\nTesting dictionary combination:")
    dict1 = {'a': 1, 'b': 2, 'c': 3}
    dict2 = {1: 'яблоко', 2: 'банан', 3: 'вишня'}
    result = {key: dict2[value] for key, value in dict1.items()}
    print(result)

    print("\nCreating a dictionary from words:")
    words = [
        "Create",
        "Character",
        "a",
        "as",
        "and",
        "dictionary",
        "with",
        "words",
        "key",
        "first",
        "Value",
        "starting",
        "that"]
    result = {
        first_char: [word for word in words if word.strip()[0].upper()
                     == first_char]
        for first_char in {word.strip()[0].upper() for word in words}
    }
    print(result)

    print("\nFiltering dictionaries with empty values for 'K':")
    dict_list = [{'K': 'value1', 'L': 'value2'},
                 {'K': '', 'L': 'value3'},
                 {'K': 'value4', 'L': 'value5'},
                 {'K': '', 'L': 'value6'},
                 {'K': 'value7', 'L': 'value8'}]
    result = [d for d in dict_list if d.get('K') == '']
    print(result)

    print("\nTesting Fibonacci generator:")
    fib_gen = fibonacci()
    for _ in range(10):
        print(next(fib_gen))

    print("\nTesting Geometric Progression generator:")
    geo_gen = geometric_progression(2, 3)
    for _ in range(5):
        print(next(geo_gen))

    print("\nTesting Countdown generator:")
    countdown_gen = countdown(5)
    for num in countdown_gen:
        print(num)