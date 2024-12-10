# mypackage/decorator.py

import time
from functools import wraps
from contextlib import ContextDecorator

# Define the decorator


def timeit(func=None, *, min_seconds=0):
    # If used without parentheses
    if func and callable(func):
        @wraps(func)
        def wrapper(*args, debug=False, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time

            if debug and elapsed_time > min_seconds:
                print(
                    f"Time taken by {
                        func.__name__}: {
                        elapsed_time:.6f} seconds")
            return result
        return wrapper

    # If used with parentheses
    def decorator(func):
        @wraps(func)
        def wrapper(*args, debug=False, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time

            if debug and elapsed_time > min_seconds:
                print(
                    f"Time taken by {
                        func.__name__}: {
                        elapsed_time:.6f} seconds")
            return result
        return wrapper

    return decorator


# Create the timeit class as both context manager and decorator
class timeit(ContextDecorator):
    def __init__(self, min_seconds=0):
        self.min_seconds = min_seconds

    # Entry point for the context manager
    def __enter__(self):
        self.start_time = time.time()
        return self

    # Exit point for the context manager
    def __exit__(self, *exc):
        self.end_time = time.time()
        self.elapsed_time = self.end_time - self.start_time
        if self.elapsed_time > self.min_seconds:
            print(f"Time taken: {self.elapsed_time:.6f} seconds")

    # The __call__ method makes it work as a decorator
    def __call__(self, func):
        def wrapped_func(*args, **kwargs):
            with self:  # Using the context manager functionality
                return func(*args, **kwargs)
        return wrapped_func


# Example functions to test
@timeit(min_seconds=1)
def slow_function():
    """This is a slow function that simulates a long task."""
    time.sleep(1.5)
    print("Slow function executed.")


@timeit(min_seconds=1)
def fast_function():
    """This is a fast function."""
    time.sleep(0.5)
    print("Fast function executed.")


# Test functions using if __name__ == "__main__"
if __name__ == "__main__":
    print("Testing the decorator with min_seconds=1:")

    # Testing fast_function (this will not print the time as it is below 1
    # second)
    fast_function()

    # Testing slow_function (this will print the time as it exceeds 1 second)
    slow_function()

    print("\nTesting the context manager:")

    # Using timeit as a context manager
    with timeit(min_seconds=1):
        time.sleep(1.5)  # Simulate a slow operation

    # Example function calls with the debug flag
    print("\nTesting decorator with debug=True:")
    # This should not print the time as it's less than 1 second
    fast_function(debug=True)
    # This will print the time as it's greater than 1 second
    slow_function(debug=True)



