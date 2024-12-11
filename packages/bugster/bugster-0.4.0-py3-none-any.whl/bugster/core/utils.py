"""
Bugster utils
"""

import random
import string


def random_string(length=5):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


def random_integer(length=5):
    min_value = 10 ** (length - 1)
    max_value = 10**length - 1
    return str(random.randint(min_value, max_value))
