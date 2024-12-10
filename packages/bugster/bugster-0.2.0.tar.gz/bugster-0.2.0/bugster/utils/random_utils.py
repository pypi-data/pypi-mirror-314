import random
import string


def random_string(length=5):
    return "".join(random.choices(string.ascii_lowercase, k=length))


def random_int(length=5):
    # Generates a random integer of given digit length
    min_val = 10 ** (length - 1)
    max_val = (10**length) - 1
    return str(random.randint(min_val, max_val))


def random_float(length=3, decimal_places=2):
    min_val = 10 ** (length - 1)
    max_val = (10**length) - 1
    integer_part = random.randint(min_val, max_val)
    decimal_part = random.randint(0, (10**decimal_places) - 1)
    return f"{integer_part}.{decimal_part:0{decimal_places}}"


def random_char(length=5):
    # Alphanumeric random string
    chars = string.ascii_lowercase + string.digits
    return "".join(random.choices(chars, k=length))
