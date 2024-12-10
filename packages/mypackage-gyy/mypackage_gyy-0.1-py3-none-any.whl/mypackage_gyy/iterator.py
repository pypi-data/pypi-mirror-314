# mypackage/iterator.py

import itertools
from itertools import count, repeat

# Task 1: Iterator for numbers from 10 to a given limit


class NumberIterator:
    def __init__(self, limit):
        self.current = 10
        self.limit = limit

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= self.limit:
            result = self.current
            self.current += 1
            return result
        else:
            raise StopIteration

# Task 2(A): Infinite iterator for numbers divisible by 7 and 9


def divisible_by_7_and_9():
    for num in count(0):  # Infinite iterator starting from 0
        if num % 7 == 0 and num % 9 == 0:
            yield num
